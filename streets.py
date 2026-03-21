import momepy
import geopandas as gpd
import osmnx as ox
import os
import neatnet

def process_osm_streets(
    geometry_maskfile, 
    mask_area, 
    output_file):

    local_crs = 2193

    # get mask geometry
    mask_df = gpd.read_file(geometry_maskfile)
    if "urban" in geometry_maskfile:
        mask_geom = mask_df.query('UR2025_V1_00_NAME in @mask_area')
    else:    
        mask_geom = mask_df.query('name in @mask_area')

    bbox = mask_geom.bounds.values[0]

    osm_graph = ox.graph_from_bbox(
        bbox,
        network_type="drive"
        )

    osm_graph = ox.projection.project_graph(osm_graph, to_crs=local_crs)
    streets = ox.graph_to_gdfs(
        ox.convert.to_undirected(osm_graph),
        nodes=False,
        edges=True,
        node_geometry=False,
        fill_edge_geometry=True,
    ).reset_index(drop=True)

    streets = neatnet.remove_interstitial_nodes(streets)
    streets = streets[["geometry"]]
    # streets = gpd.clip(streets, mask_geom.to_crs(local_crs))
    streets.to_parquet(output_file)

    return