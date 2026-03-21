GPKG_ZIP = lds-nz-suburbs-and-localities-GPKG.zip
GPKG_FILES = nz-suburbs-and-localities.gpkg

$(GPKG_FILES): 
	unzip lds-nz-suburbs-and-localities-GPKG.zip nz-suburbs-and-localities.gpkg

GBA_BUILDINGS = e170_s35_e175_s40.parquet

$(GBA_BUILDINGS):
	curl -o e170_s35_e175_s40.parquet https://data.source.coop/tge-labs/globalbuildingatlas-lod1/e170_s35_e175_s40.parquet


AUCKLAND_CENTRAL = buildings_osm_Auckland\ Central.parquet \
	streets_osm_Auckland\ Central.parquet

$(AUCKLAND_CENTRAL): $(GPKG_FILES) \
		$(GBA_BUILDINGS)
	uv run uoa_lecture/main.py \
	-b $(GBA_BUILDINGS) \
	-g "auckland-suburbs.gpkg" \
	-a "Auckland Central"

auckland: $(AUCKLAND_CENTRAL)

process-data: $(AUCKLAND_CENTRAL)
	uv sync

# render: 
# 	source .venv/bin/activate && \
# 	Rscript -e "renv::activate()" && \
# 	quarto render quarto/