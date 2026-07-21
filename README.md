# Examples for accessing track data from a dt4acc twin

Based on the dt4acc ALS twin

## Installing package and dependencies

* create a fresh virtual environment
* within this environement install 

```bash

 python3 -m pip install \
     'dt4acc-als-track-data[qt-example] @ git+https://github.com/PierreSchnizer/dt4acc-als-track-data' \
     'dt4acc-als @ git+https://github.com/dt4acc/dt4acc-als' \
     'dt4acc[epics] @ git+https://github.com/dt4acc/dt4acc@next/main' \
     'dt4acc-lib @ git+https://github.com/dt4acc/dt4acc-lib@next/main' \
     'bact-mml-json-importer @ git+https://github.com/hz-b/bact-mml-importer/@dev/feature/family-model-convienience-attributes' 

```