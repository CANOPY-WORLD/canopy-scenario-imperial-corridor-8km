# Canopy · Imperial Corridor data

Public geometry and recorded physics for London's nominal 8 km × 8 km Imperial Corridor Scenario.

**[Open the Scenario in Canopy](https://acse-yl222.github.io/canopy/viewer/3d/?scene=imperial_corridor_8km)** · [Data website](https://acse-yl222.github.io/canopy-scenario-imperial-corridor-8km/) · [Canopy framework](https://github.com/acse-yl222/canopy)

This repository owns the approved presentation data. Canopy owns the shared Models, Viewer, scientific contracts and Scenario configuration. The Viewer reads these files over HTTPS; they are not copied into Canopy's Pages artifact. Opening the Scenario uses the shared Viewer, without a second renderer or solver implementation here.

## Public snapshot

| Property | Value |
| --- | --- |
| Scenario ID | `imperial_corridor_8km` |
| Snapshot | `london-public-20261118` |
| Payloads | 1,477 files; 558,073,283 bytes |
| Manifest | [snapshots/london-public-20261118/manifest.json](snapshots/london-public-20261118/manifest.json) |
| Source | Existing published Canopy exports, relocated without re-encoding |

```text
catalog.json                         # Version index, manifest hashes and viewer link
snapshots/london-public-20261118/
  manifest.json                      # File paths, logical routes, sizes and SHA-256
  scene.json                         # Preserved presentation settings
  models/                            # Building geometry
  physics/                           # Compressed fields, samples and masks
  context/                           # Terrain, roads, landscape and traffic
  tiles/                             # Detailed geometry and textures
  assets/                            # Bird and UAV recordings
  actors/                            # Display models and geometry QA
tools/check_data.py                   # Standalone integrity check
```

Files retain their original GLB/gzip, compressed arrays, replay binaries, JSON, image encodings and provenance. This is a distribution snapshot, not a new physics simulation or a replacement for Canopy's V2 Asset descriptors. Preserve the actual approximately 8.2 km coverage, original coordinates, timestamps, masks and recorded limitations. Public availability does not grant a new blanket license: retain each source's notices and usage restrictions.

Private research bundles, solver intermediates, credentials and recovery histories are excluded. Full numerical research data remains in the existing local retained storage.

## Update and publish

1. Follow the [Canopy publication standard](https://github.com/acse-yl222/canopy/blob/main/visualizer/docs/publishing.md). Select only data explicitly approved for publication.
2. Create a **new** `snapshots/<snapshot_id>/` for changed data. Never modify or silently replace a published snapshot. Preserve all versions referenced by Canopy.
3. Record every payload's relative path, compatibility route, byte count and SHA-256 in its manifest. Add the snapshot and manifest hash to `catalog.json`.
4. Run `python3 tools/check_data.py` with Python 3.11 or newer. Keep the entire Pages site below 1 GB; this checker reserves a 950 MB payload budget. Each ordinary Git file must stay below 100 MiB. If another snapshot will not fit, choose a larger data host before publishing it.
5. Commit and push to `main`. GitHub Pages publishes from **main / (root)**, using `.nojekyll`. Check the successful Pages build and actual served checksums.
6. Only then update Canopy's `scenario/imperial_corridor_8km/publication.json`, pinned repository revision and locked manifest. Run Canopy's remote verification and browser checks before publishing its updated link.

GitHub Pages URLs are versioned by the snapshot directory. The reference in Canopy also pins the source commit and manifest hash. Repository history is preserved; large binary edits can grow Git history even when the latest working tree is small. This per-Scenario site is bounded by [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
