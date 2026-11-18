# Scenario data maintenance

Write documentation in English. This repository contains approved public presentation data for `imperial_corridor_8km` only. Shared Models, solvers, the Viewer and scientific contracts belong to [Canopy](https://github.com/acse-yl222/canopy).

Read `README.md` and the linked Canopy publication standard. Preserve the exact bytes, coordinates, timestamp semantics, missing masks, source notices and provenance. New exports receive new snapshot IDs; never overwrite a published snapshot or remove one referenced by Canopy. Never manufacture missing samples or claim that relocating a file reruns a simulation.

Run `python3 tools/check_data.py` before committing. Every payload must be listed with its byte size and SHA-256. Keep private research data, caches, credentials and recovery histories out of this repository. Publication requires authorization for the task; this file grants none.

Pages publishes `main` at the repository root. Verify the deployed manifest before updating Canopy's reference. Keep its Viewer link working; do not duplicate the Viewer here.
