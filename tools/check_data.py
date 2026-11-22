#!/usr/bin/env python3
"""Validate all declared public snapshots before publishing this data website."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def bounded(root, name):
    if (not isinstance(name, str) or not name or name.startswith('/') or
            any(c in name for c in '\\%?#:') or
            any(part in ('', '.', '..') for part in name.split('/'))):
        raise ValueError(f'Invalid snapshot path: {name!r}')
    path = root / name
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Snapshot path escapes its root: {name}')
    return path


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check(root=ROOT):
    catalog = json.loads((root / 'catalog.json').read_bytes())
    if catalog.get('schema_version') != '1.0.0' or catalog.get('kind') != 'canopy.scenario-data':
        raise ValueError('Unsupported Scenario data catalog')
    count, size, snapshots = 0, 0, set()
    inventories = {}
    for entry in catalog['snapshots']:
        if entry['id'] in snapshots or not re.fullmatch('[a-zA-Z0-9][a-zA-Z0-9._-]*', entry['id']):
            raise ValueError('Invalid or duplicate snapshot ID')
        snapshots.add(entry['id'])
        if entry['manifest'] != f"snapshots/{entry['id']}/manifest.json":
            raise ValueError('Snapshot manifest must live in its own directory')
        manifest_path = bounded(root, entry['manifest'])
        if sha256(manifest_path) != entry['sha256']:
            raise ValueError('Snapshot manifest checksum mismatch')
        manifest = json.loads(manifest_path.read_bytes())
        if (manifest.get('schema_version') not in ('1.0.0', '1.1.0') or manifest.get('kind') != 'canopy.publication' or
                manifest.get('scenario_id') != catalog['scenario_id'] or manifest.get('snapshot') != entry['id']):
            raise ValueError('Snapshot identity mismatch')
        retired_list = entry.get('retired_paths', [])
        if not isinstance(retired_list, list) or any(not isinstance(x, str) for x in retired_list):
            raise ValueError('Invalid retired paths')
        retired = set(retired_list)
        if len(retired) != len(retired_list):
            raise ValueError('Duplicate retired paths')
        names, routes, total = set(), set(), 0
        local_names, stored_bytes = set(), 0
        for record in manifest['files']:
            path = bounded(manifest_path.parent, record['path'])
            if record['path'] in retired:
                if 'source_snapshot' in record or path.exists():
                    raise ValueError('Retired payload must be local and removed')
                bounded(root, record['viewer_path'])
                if record['path'] in names or record['viewer_path'] in routes:
                    raise ValueError('Duplicate retired path or route')
                names.add(record['path'])
                routes.add(record['viewer_path'])
                total += record['bytes']
                continue
            if 'source_snapshot' in record:
                source = record['source_snapshot']
                if manifest['schema_version'] != '1.1.0' or not isinstance(source,str) or source not in inventories:
                    raise ValueError('Source snapshot must already be validated')
                original = inventories[source].get(record['path'])
                if not original or 'source_snapshot' in original or any(original[k] != record[k] for k in ('bytes','sha256','viewer_path')):
                    raise ValueError('Reused snapshot record differs from its immutable source')
                path = bounded(root / 'snapshots' / source, record['path'])
            else:
                local_names.add(record['path'])
                stored_bytes += record['bytes']
            bounded(root, record['viewer_path'])
            if record['path'] in names or record['viewer_path'] in routes:
                raise ValueError('Duplicate snapshot file or presentation route')
            names.add(record['path'])
            routes.add(record['viewer_path'])
            if (type(record['bytes']) is not int or record['bytes'] < 0 or
                    record['bytes'] >= 100 * 1024 ** 2 or path.stat().st_size != record['bytes'] or
                    sha256(path) != record['sha256']):
                raise ValueError(f'Snapshot checksum/size mismatch: {path}')
            total += record['bytes']
        if not retired <= names:
            raise ValueError('Retired path not present in original manifest')
        actual = {p.relative_to(manifest_path.parent).as_posix()
                  for p in manifest_path.parent.rglob('*') if p.is_file()}
        if actual != local_names | {'manifest.json'} or total != manifest['bytes'] or total != entry['bytes'] or len(names) != entry['files']:
            raise ValueError('Unlisted payloads or incorrect snapshot totals')
        count += len(names)
        size += stored_bytes
        inventories[entry['id']] = {r['path']:r for r in manifest['files'] if r['path'] not in retired}
    if {p.name for p in (root / 'snapshots').iterdir()} != snapshots:
        raise ValueError('Unlisted snapshot')
    if size > 950_000_000:
        raise ValueError('Published data exceeds the 950 MB budget; use an appropriate larger store')
    return {'scenario_id': catalog['scenario_id'], 'snapshots': len(snapshots), 'files': count, 'bytes': size}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
