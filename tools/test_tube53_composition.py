"""Keep the complete current London release when adding the Tube contribution."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'snapshots'
BASE = 'london-complete-daylight-20261125'
NEW = 'london-complete-tube53-20261125'

class TubeCompositionTests(unittest.TestCase):
    def test_existing_assets_and_scene_are_preserved(self):
        old = json.loads((ROOT / BASE / 'manifest.json').read_text())
        new = json.loads((ROOT / NEW / 'manifest.json').read_text())
        records = {f['path']: f for f in new['files']}
        for f in old['files']:
            if f['path'] != 'scene.json':
                self.assertEqual((f['sha256'], f['bytes']), (records[f['path']]['sha256'], records[f['path']]['bytes']), f['path'])
        scene = json.loads((ROOT / NEW / 'scene.json').read_text())
        old_scene = json.loads((ROOT / BASE / 'scene.json').read_text())
        underground = scene.pop('underground')
        self.assertEqual(scene, old_scene)
        self.assertEqual(len(underground['stations']['list']), 53)
        self.assertEqual(len({s[0] for s in underground['stations']['list']}), 53)
        for name, declaration in underground['files'].items():
            path = underground['dir'] + '/' + name
            self.assertEqual(declaration['sha256'], records[path]['sha256'])
            self.assertEqual(hashlib.sha256((ROOT / NEW / path).read_bytes()).hexdigest(), declaration['sha256'])
        self.assertEqual(len(new['files']) - len(old['files']), 6)

if __name__ == '__main__':
    unittest.main()
