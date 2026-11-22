import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from check_data import check

class ReuseTests(unittest.TestCase):
    def test_reuse_is_immutable_and_stored_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);old=root/'snapshots/old';new=root/'snapshots/new';old.mkdir(parents=True);new.mkdir()
            (old/'a.bin').write_bytes(b'abc')
            record=dict(path='a.bin',viewer_path='scenes/demo/a.bin',bytes=3,sha256=hashlib.sha256(b'abc').hexdigest())
            entries=[]
            def save():
                entries.clear()
                for name,version,r in [('old','1.0.0',record),('new','1.1.0',{**record,'source_snapshot':'old'})]:
                    p=root/'snapshots'/name/'manifest.json';p.write_text(json.dumps(dict(schema_version=version,kind='canopy.publication',scenario_id='demo',snapshot=name,bytes=3,files=[r])))
                    entries.append(dict(id=name,manifest=f'snapshots/{name}/manifest.json',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=3,files=1))
                (root/'catalog.json').write_text(json.dumps(dict(schema_version='1.0.0',kind='canopy.scenario-data',scenario_id='demo',snapshots=entries)))
            save();self.assertEqual(check(root)['bytes'],3)
            # Retirement cannot remove a payload used by the current snapshot.
            c=json.loads((root/'catalog.json').read_text());c['snapshots'][0]['retired_paths']=['a.bin']
            (root/'catalog.json').write_text(json.dumps(c))
            with self.assertRaisesRegex(ValueError,'must be local and removed'):check(root)
            (old/'a.bin').unlink()
            with self.assertRaisesRegex(ValueError,'differs from its immutable source'):check(root)
            # An unreferenced retirement leaves the original manifest intact.
            c['snapshots'].pop();(root/'catalog.json').write_text(json.dumps(c))
            (new/'manifest.json').unlink();new.rmdir()
            self.assertEqual(check(root)['bytes'],0)
            c['snapshots'][0]['retired_paths'].append('missing.bin')
            (root/'catalog.json').write_text(json.dumps(c))
            with self.assertRaisesRegex(ValueError,'not present'):check(root)
            new.mkdir();(old/'a.bin').write_bytes(b'abc');save()
            # A source file edit breaks both references; no silent substitution.
            (old/'a.bin').write_bytes(b'bad')
            with self.assertRaises(ValueError):check(root)
            (old/'a.bin').write_bytes(b'abc')
            p=new/'manifest.json';m=json.loads(p.read_text());m['files'][0]['source_snapshot']='../private';p.write_text(json.dumps(m));entries[1]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
            c=json.loads((root/'catalog.json').read_text());c['snapshots']=entries;(root/'catalog.json').write_text(json.dumps(c))
            with self.assertRaises(ValueError):check(root)
if __name__=='__main__':unittest.main()
