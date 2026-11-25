"""Regression checks for the composed public London release."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'snapshots'
SNAPSHOT = 'london-complete-20261125'

class CompletePublicationTests(unittest.TestCase):
    def test_scene_keeps_latest_features_and_matching_field_decoders(self):
        scene = json.loads((ROOT / SNAPSHOT / 'scene.json').read_text())
        manifest = json.loads((ROOT / SNAPSHOT / 'manifest.json').read_text())
        records = {r['path']: r for r in manifest['files']}
        def read_record(path):
            record = records[path]
            return json.loads((ROOT / record.get('source_snapshot', SNAPSHOT) / path).read_text())
        physics = read_record('physics/manifest.json')['arrays']
        self.assertIn(scene['interior']['building'], records)
        self.assertIn(scene['interior']['office'], records)
        self.assertIn(scene['corridor_context']['native_traffic'], records)
        self.assertEqual(scene['layers']['poll']['frames'], 100)
        self.assertEqual(physics['poll.npy']['shape'], [100, 1000, 1000])
        current = json.loads((ROOT / 'london-compact-20261122' / 'scene.json').read_text())
        for layer in ('solar', 'flood'):
            self.assertEqual(scene['layers'][layer], current['layers'][layer])
            self.assertEqual(scene['layers'][layer]['frames'], 100)
        for name, transport in scene['protocol_display']['npy_transport'].items():
            for part in transport.get('parts', []):
                self.assertIn('physics/' + part['file'], records, name)
        self.assertEqual(scene['protocol_display']['npy_transport']['flood.npy'],
                         current['protocol_display']['npy_transport']['flood.npy'])

if __name__ == '__main__':
    unittest.main()
