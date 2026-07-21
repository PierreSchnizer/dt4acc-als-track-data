# Examples for accessing track data from a dt4acc twin

Based on the dt4acc ALS twin

## Install package and its dependencies

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

This step is necessary as these dependency packages are not upstream.
Please note that it installs the application example is built based on qt.
The QT library is well supported on Linux and may run on other OS. 

Clone this repository (to have access to the examples) 

```bash
git clone https://github.com/PierreSchnizer/dt4acc-als-track-data.git

```

## Run the twin

Start the twin (preferably in a separate terminal). You need to activate 
the enviroment you installed the packages above. Then it should be sufficient
to type

```bash

dt4acc_als
```

It will provide some messages: at the end it will give you access to 
the prompt of a python softioc

## Run the examples

The application examples are found in `examples/ophyd_async`. 
Both set the start vector and retrieve the data. 

* `32_tbt_data_read_different_vectors_as_qt_application.py` 
   sets some start vectors and retrieves the data
* `33_tbt_with_sampled_start_vec.py`samples start vectors from 
  some emittance based distribution
   


