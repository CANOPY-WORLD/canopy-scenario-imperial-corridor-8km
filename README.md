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

## Native South Kensington traffic replacement

`london-traffic-native-20261122` selects the exact Exhibition Road review recording (410 samples at 0.1 seconds, simulation times 680.0–720.9). Native road geometry, front-bumper XYZ, dimensions, headings, slopes and recorded signal states travel together. It replaces the older 1-second citywide traffic replay in the selected website; other widgets retain full city geometry. This is a low-load synthetic demonstration, not a validated citywide capacity model. The source run has zero collisions/teleports and three emergency brakes; higher loads are not approved. Original source inputs and full FCD are retained privately. The public derivation gives original hashes and OSM attribution.

The shared viewer defaults solar playback to the 68 daylight frames (21–88, 04:50:54–21:05:27 BST); all 100 unchanged source frames remain available. The selected scene is 239,324,744 bytes; new presentation payloads add 1,121,355 bytes.

## Coupled traffic pollution

`london-pollution-log8-20261122` replaces the selected legacy road tracer with 100 recorded SUMO exhaust PMx increment slices over 0–600 seconds. The exact 8,000 m square uses 1,000 × 1,000 cells at 8 m, with no spatial or temporal resampling. Presentation frames use fixed-range log1p uint8 quantization and per-frame gzip: 38,407,654 bytes for the 100 frames, 39,021,534 newly stored bytes including masks and provenance. The complete selected city download is 273,582,403 bytes. The earlier 76.6 MB float16 candidate was not published and is retained privately rather than duplicated on this site.

The transform is `code = round(log1p(c / 1e-6) / step)` and `c = 1e-6 * expm1(code * step)`, where `step = log1p(80.40364837646484 / 1e-6) / 254`. Zero remains exact; code 255 is reserved for missing values and the invalid-cell mask remains exact. Against native float32, maximum error is 2.58498 µg/m³, RMSE 0.00585769 µg/m³, and maximum relative error for values at or above the display minimum 0.00023500917 µg/m³ is 3.66321%. No high-concentration values are clipped during encoding. This lossy encoding is for visualization only; native float32 volumes remain retained separately for computation and analysis.

The field uses frozen recorded 3D wind and new SUMO emissions; it is not observed total PM2.5 or a Health exposure input. The displayed layer is the 0–8 m voxel mean centred at 4 m. Source omissions, relocation, solver diagnostics, assumptions, timestamps and checksums are retained in `physics/traffic-pmx-provenance.json`. Existing buildings, traffic and other fields are reused unchanged. The shared Canopy viewer decodes the declared log1p transport and supports explicit per-layer dimensions and offsets.

## White City I-HUB concept interior

`london-ihub-interior-20261122` extends the latest pollution snapshot with the retained I-HUB v10 building and concept office. The two aligned GLBs add 3,486,152 bytes using lossless gzip, with unchanged mesh buffers and a recorded geographic root transform. Existing pollution, sunlight, traffic and city payloads are reused by exact checksum. The full selected data download is 277,076,014 bytes.

`scene.interior` declares the indoor widget, intact building shell, restored authored ceiling and 30-second camera journey (arrival indoors at 4 seconds). This is a concept office rather than a surveyed as-built model; the retained geographic fit has a 1.58 m median residual. `interiors/ihub-v10/provenance.json` records source mesh hashes, aligned hashes, placement, vertical-datum policy and inherited layout limits. The original source and scientific Asset remain retained privately.

### Synthetic city Health replay (26 November 2026)

`london-health-replay-20261126` adds a losslessly compressed, explicitly synthetic South Kensington Health recording (668 retained samples), presentation settings and provenance. The shared scene declares the recording; other city resources reuse their exact existing snapshot hashes. The route, modelled crossing waits and native missing values are unchanged. This is a recorded experimental illustration, not participant data or a clinically validated result. Route calculation is not hosted.
