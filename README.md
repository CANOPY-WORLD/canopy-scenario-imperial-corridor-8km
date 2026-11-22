# Canopy · Imperial Corridor data

Public geometry and recorded physics for London's nominal 8 km × 8 km Imperial Corridor Scenario.

**[Open the Scenario in Canopy](https://canopy-world.github.io/canopy/viewer/3d/?scene=imperial_corridor_8km)** · [Data website](https://canopy-world.github.io/canopy-scenario-imperial-corridor-8km/) · [Canopy framework](https://github.com/CANOPY-WORLD/canopy) · [CANOPY-WORLD organization](https://github.com/CANOPY-WORLD)

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

1. Follow the [Canopy publication standard](https://github.com/CANOPY-WORLD/canopy/blob/main/visualizer/docs/publishing.md). Select only data explicitly approved for publication.
2. Create a **new** `snapshots/<snapshot_id>/` for changed data. Never modify or silently replace a published snapshot. Preserve all versions referenced by Canopy.
3. Record every payload's relative path, compatibility route, byte count and SHA-256 in its manifest. Add the snapshot and manifest hash to `catalog.json`.
4. Run `python3 tools/check_data.py` with Python 3.11 or newer. Keep the entire Pages site below 1 GB; this checker reserves a 950 MB payload budget. Each ordinary Git file must stay below 100 MiB. If another snapshot will not fit, choose a larger data host before publishing it.
5. Commit on a feature branch, open a pull request, review the diff and wait for explicit merge approval. After approval, merge through the protected `main` branch. GitHub Pages publishes from **main / (root)**, using `.nojekyll`. Check the successful Pages build and actual served checksums.
6. Only then update Canopy's `scenario/imperial_corridor_8km/publication.json`, pinned repository revision and locked manifest. Run Canopy's remote verification and browser checks before publishing its updated link.

GitHub Pages URLs are versioned by the snapshot directory. The reference in Canopy also pins the source commit and manifest hash. Repository history is preserved; large binary edits can grow Git history even when the latest working tree is small. This per-Scenario site is bounded by [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## Compact snapshot candidate

`london-compact-20261122` contains 1297 payloads totalling 228,692,784 bytes (about 59% less than the original). The original inventory remains immutable; superseded solar payloads are retired below. This reduces the selected viewer download, not repository history or the combined Pages footprint.

The candidate keeps all building details resident, uses lossless Meshopt geometry encoding and half-size ordinary building textures, retains landmark texture quality, selects 47 summer shadow frames and all 47 winter frames at unchanged 8 m / 10 minute sampling, and omits irradiance, static wind, bird replay and unused context copies. Traffic recordings are unchanged. Added zebra crossing paths retain OpenStreetMap identities and attribution; displayed stripe dimensions are illustrative. See [derivation report](snapshots/london-compact-20261122/derivation.json) for original hashes, omissions and compression evidence.

This snapshot must be merged, deployed and verified before Canopy switches its active publication reference.

## Full-day summer solar candidate

`london-solar-small-20261122` replaces the two old solar date selections with 100 newly computed summer-solstice samples from 00:00 BST on 21 June 2026 through the following midnight. It restores irradiance on a fixed 0–950 W/m² colour scale and retains matching shadows. This is a clear-sky model, not observed weather.

The complete selected Scenario is 249,886,035 bytes across 1,405 payloads. Only 30,509,013 bytes are newly stored: approximately 22.23 MB irradiance, 7.99 MB losslessly packed shadows, and masks/provenance. Irradiance uses codes 0–254 with scale 950/254 W/m², with a measured maximum added error of 1.87012 W/m² against the retained float16 8 m display values. No frames, grid cells or masks are removed. Native results remain private and unchanged. The earlier 73 MB local candidate is not included in this repository branch or upload.

Publication manifest 1.1 adds optional `source_snapshot` to each file record. It identifies an earlier immutable snapshot in this repository. Path, route, byte count and hash must match that snapshot's original non-reused record. The data checker rejects unknown sources, transitive reuse, altered records and unlisted files. The catalog byte totals describe complete logical downloads; the capacity check counts physically stored payload bytes once. After the requested solar retirement, the site stores 733,049,655 payload bytes. Original manifest bytes remain unchanged.

Review this candidate with the corresponding Canopy compressed-reader change. Merge and verify this data deployment before publishing the shared viewer reference. Run `python3 tools/check_data.py` and `python3 -m unittest discover -s tools -p test_check_data.py` before publication.

## Solar replacement and retirement

The user explicitly requested replacement and removal of previous sunlight data. The current viewer selects only `london-solar-small-20261122`. All 390 obsolete solar/shadow payloads (84,225,425 bytes) are removed from the current tree and website. Original manifests and Git history remain intact for provenance. Catalog `retired_paths` records the exact removed paths; validation requires their absence and rejects reuse of retired data. Shared geometry and other fields are retained. This explicit retirement supersedes the general snapshot availability policy for these paths only.
