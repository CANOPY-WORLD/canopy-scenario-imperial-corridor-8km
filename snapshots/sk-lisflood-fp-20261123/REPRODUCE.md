# South Kensington recorded LISFLOOD-FP case

This package reruns the recorded rain event from the accepted, frozen terrain and warmed initial water-depth grid. It does not regenerate the full terrain preparation or six-hour lake initialization from raw downloads. Their assumptions, checks and input hashes are retained in `metadata/`. The figure workflow illustrates the complete historical process, including those earlier stages.

## Case and limits

- LISFLOOD-FP 8.3 GPU ACC, FP64, with the included experimental shared-face donor limiter and external-boundary volume accounting patch. The unmodified release is not equivalent.
- 3,200 × 3,200 cells, 1 m, EPSG:27700; bounds E 525000–528200, N 177800–181000. Terrain/water-surface elevations use ODN; depth is metres above the local modified bed.
- Synthetic uniform 49.95 mm rain over 90 minutes, followed by 90 minutes of surface redistribution. Four FREE boundaries, Manning n=0.03. No infiltration, drains, roof redistribution or maintained lake stages. Rain falls on roofs and existing water too.
- Six-hour lake-at-rest check preceded the recorded event. DSM-based trial normal levels are 14.98 m ODN for Long Water/Serpentine and 24.54 m for Round Pond. Bathymetry is estimated, not surveyed.
- Deep isolated cells at building edges remain terrain-review flags. Numerical conservation does not establish observed flood accuracy.

## Install

Reference platform: Linux x86-64, NVIDIA RTX 5090, CUDA toolkit 12.8, GCC/G++ 13, Python 3.12. A compatible installed NVIDIA driver, GPU memory and system CMake/Git are required. The explicit conda package list records the current runtime; `environment.yml` is the human-readable equivalent. Other GPU architectures may build with an appropriate numeric CUDA architecture, but have not been validated. No CPU equivalence is claimed.

```sh
micromamba create -y -p "$PWD/lisflood-env" -f sk-lisflood-fp-20261123/environment-linux-64.explicit.txt
export LF_ENV="$PWD/lisflood-env"
export PATH="$LF_ENV/bin:$PATH"
export LD_LIBRARY_PATH="$LF_ENV/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export OMP_NUM_THREADS=8
python sk-lisflood-fp-20261123/reproduce.py verify --case sk-lisflood-fp-20261123
```

Use a CUDA-compatible host compiler; the reference used GCC 13. The environment creation command writes beside the extracted case. Keep the case directory immutable: verification rejects extra files, altered bytes and symlinks.

## Build and run

From the parent of the extracted case (all build/run directories must be new):

```sh
python sk-lisflood-fp-20261123/reproduce.py build --case sk-lisflood-fp-20261123 --work-dir solver-build --cuda-arch 120 --dependency-prefix "$LF_ENV" --jobs 4
python sk-lisflood-fp-20261123/reproduce.py run --case sk-lisflood-fp-20261123 --binary solver-build/build/lisflood --build-record solver-build/build-record.json --output rain-run
python sk-lisflood-fp-20261123/reproduce.py audit --case sk-lisflood-fp-20261123 --output rain-run
```

The builder fetches pinned upstream commit `78dda58284701f99a24ec982dab0de8a28a00246`, verifies original and patched sources, and records the compiled binary hash. It never uses the latest upstream revision. A matching local checkout can be supplied with `--upstream-checkout`. `run --dry-run` validates the planned invocation without starting the solver; `--seconds 1800` gives a bounded test, not the complete event. Ctrl-C stops the process and marks it interrupted; resume is not implemented. An unsuccessful run must use a new directory when retried.

A full run takes roughly 26 minutes on the reference GPU, depending on other workloads; allow at least 15 GB free disk for native outputs/build products and several GB available GPU memory. The runner copies inputs, keeps `rain.log`, writes `run-record.json`, and creates native depth, staggered velocity, stage and boundary-budget outputs in `rain-run/results/`. Saved times come from the solver and can slightly exceed nominal intervals. No bitwise equivalence is promised across compilers or hardware.

## Acceptance and outputs

A zero exit code only means the process completed. `audit` independently integrates rain in the actual ACC update order using the previous timestep (zero for the first increment), then checks finite, nonnegative depths and stored volume against external fluxes. The absolute water-balance tolerance is 0.1 m³; `verification.json` records every checked snapshot. It is not field calibration. Native `.mass` is insufficient for this dynamic-rain GPU case.

The original complete run reached 10800.069185625774 s; maximum sampled absolute volume residual was 4.7630130097786605e-6 m³. Reference diagnostics are in `metadata/validation_summary.json`. The presentation archive contains float32 GeoTIFFs and a seven-second video/GIF covering 0–105 minutes. Its interpolated animation frames are for display, not additional solver outputs; teal marks pre-existing water. Raw native outputs can be regenerated by this package and are not included in the website snapshot.

`gis/` contains the accepted terrain, masks and initial-water context. Building and lake masks must be applied when reporting ground flooding: roof storage and initial lake depths are separate quantities. A future Canopy 3D integration must explicitly transform EPSG:27700/ODN to the Scenario's spatial conventions; this package does not perform that conversion or register a Method/Asset.

See [source notices](ATTRIBUTION.md). `reproduction.json` locks every distributed file by SHA-256. Archive checksums are recorded by the companion Scenario data snapshot.
