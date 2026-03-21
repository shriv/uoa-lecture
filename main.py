
from uoa_lecture import process_gba_buildings, process_osm_streets
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FILE] [AREA]...",
        description="Process building and streets data"
    )
    parser.add_argument(
        "-b", "--buildingfile", action="store"
    )
    parser.add_argument(
        "-g", "--geometryfile", action="store"
    )
    parser.add_argument(
        "-a", "--area", action="store"
    )
    return parser


parser = init_argparse()
args = parser.parse_args()

geometry_filename = args.geometryfile
buildings_filename = args.buildingfile
urban_area = args.area

processed_buildings_filename = f"data/buidings_osm_{urban_area}.parquet"
processed_streets_filename = f"data/streets_osm_{urban_area}.parquet"

process_gba_buildings(
    buildings_filename,
    geometry_filename, 
    urban_area,
    processed_buildings_filename)

process_osm_streets(
    geometry_filename, 
    urban_area,
    processed_streets_filename)