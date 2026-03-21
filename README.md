# Guest lecture for GISCI 343
This repo contains the guest lecture demo notebook for the session on 23 March 2026 by Shrividya (Shriv) Ravi. 

## Running the notebook
The notebook (`demo.ipynb`) depends on datasets filtered to `Auckland Central` suburb which are committed to the repo. Only `uv` is needed for running the notebook. All the modules, demo notebook and data are in one folder to make paths easier. 

IF you want to change the spatial area of interest to a different suburb, you will need to download the open data sources and have the `make` utility installed. A Makefile contains the commands to build the filtered datasets from open data sourced from the web. You need to manually download the full LINZ suburbs and localities dataset as a GPKG from https://data.linz.govt.nz/login/?next=%2Flayer%2F113764-nz-suburbs-and-localities%2F. In the Makefile: 

- change the GPKG dataset name in Line 20 to the downloaded one with all suburbs 
- change the spatial area of interest in Line 21 
- change filenames and make variables
- run `make process-data` in the terminal after `cd <repo folder>`
