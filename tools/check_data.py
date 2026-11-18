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
        if (manifest.get('schema_version') != '1.0.0' or manifest.get('kind') != 'canopy.publication' or
                manifest.get('scenario_id') != catalog['scenario_id'] or manifest.get('snapshot') != entry['id']):
            raise ValueError('Snapshot identity mismatch')
        names, routes, total = set(), set(), 0
        for record in manifest['files']:
            path = bounded(manifest_path.parent, record['path'])
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
        actual = {p.relative_to(manifest_path.parent).as_posix()
                  for p in manifest_path.parent.rglob('*') if p.is_file()}
        if actual != names | {'manifest.json'} or total != manifest['bytes'] or total != entry['bytes'] or len(names) != entry['files']:
            raise ValueError('Unlisted payloads or incorrect snapshot totals')
        count += len(names)
        size += total
    if {p.name for p in (root / 'snapshots').iterdir()} != snapshots:
        raise ValueError('Unlisted snapshot')
    if size > 950_000_000:
        raise ValueError('Published data exceeds the 950 MB budget; use an appropriate larger store')
    return {'scenario_id': catalog['scenario_id'], 'snapshots': len(snapshots), 'files': count, 'bytes': size}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
