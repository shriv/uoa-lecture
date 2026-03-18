GPKG_FILES = data/nz-suburbs-and-localities.gpkg

$(GPKG_FILES): 
	unzip data/lds-nz-suburbs-and-localities-GPKG.zip nz-suburbs-and-localities.gpkg -d data

GBA_BUILDINGS = data/e170_s35_e175_s40.parquet

$(GBA_BUILDINGS):
	curl -o data/e170_s35_e175_s40.parquet https://data.source.coop/tge-labs/globalbuildingatlas-lod1/e170_s35_e175_s40.parquet


AUCKLAND_CENTRAL = data/buildings_osm_Auckland\ Central.parquet \
	data/streets_osm_Auckland\ Central.parquet

$(AUCKLAND_CENTRAL): $(GPKG_FILES) \
		$(GBA_BUILDINGS)
	uv run uoa_lecture/main.py \
	-b $(GBA_BUILDINGS) \
	-g "data/nz-suburbs-and-localities.gpkg" \
	-a "Auckland Central"

auckland: $(AUCKLAND_CENTRAL)

process-data: $(AUCKLAND_CENTRAL)
	uv sync

# render: 
# 	source .venv/bin/activate && \
# 	Rscript -e "renv::activate()" && \
# 	quarto render quarto/