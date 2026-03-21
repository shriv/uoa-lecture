import momepy
import geopandas as gpd
import pandas as pd
import osmnx as ox
import libpysal
import os

def generate_morphometrics(buildings, streets, include_height=False):
    
    ## Tesselation
    limit = momepy.buffered_limit(buildings, "adaptive")
    tessellation = momepy.morphological_tessellation(buildings, segment = 4.0, clip=limit)
    collapsed, _ = momepy.verify_tessellation(tessellation, buildings)

    buildings = buildings.drop(collapsed)
    limit = momepy.buffered_limit(buildings, "adaptive")
    tessellation = momepy.morphological_tessellation(buildings, segment = 4.0, clip=limit)

    # check
    tessellation.shape[0] == buildings.shape[0]

    # associate streets
    buildings["street_index"] = momepy.get_nearest_street(
        buildings, streets, max_distance=100
    )

    tessellation["street_index"] = buildings["street_index"]

    # pre-req
    queen_1 = libpysal.graph.Graph.build_contiguity(tessellation, rook=False)
    queen_3 = queen_1.higher_order(3)
    buildings_q1 = libpysal.graph.Graph.build_contiguity(buildings, rook=False)

    # dimensions
    buildings["building_area"] = buildings.area
    if include_height: 
        buildings["volume"] = momepy.volume(buildings.area, buildings.height)
        buildings["floor_area"] = momepy.floor_area(buildings.area, buildings.height)
    buildings["eri"] = momepy.equivalent_rectangular_index(buildings)
    buildings["elongation"] = momepy.elongation(buildings)
    buildings["shared_walls"] = momepy.shared_walls(buildings) / buildings.length
    buildings["neighbor_distance"] = momepy.neighbor_distance(buildings, queen_1)
    buildings["interbuilding_distance"] = momepy.mean_interbuilding_distance(buildings, queen_1, queen_3)
    buildings["adjacency"] = momepy.building_adjacency(buildings_q1, queen_3)

    tessellation["tess_area"] = tessellation.area
    tessellation["convexity"] = momepy.convexity(tessellation)
    tessellation["neighbors"] = momepy.neighbors(tessellation, queen_1, weighted=True)
    tessellation["covered_area"] = queen_1.describe(tessellation.area)["sum"]
    tessellation["car"] = buildings.area / tessellation.area

    streets["length"] = streets.length
    streets["linearity"] = momepy.linearity(streets)
    profile = momepy.street_profile(streets, buildings)
    streets[profile.columns] = profile


    graph = momepy.gdf_to_nx(streets)
    graph = momepy.node_degree(graph)
    graph = momepy.closeness_centrality(graph, radius=400, distance="mm_len")
    graph = momepy.meshedness(graph, radius=400, distance="mm_len")
    nodes, edges = momepy.nx_to_gdf(graph)

    buildings["edge_index"] = momepy.get_nearest_street(buildings, edges)
    buildings["node_index"] = momepy.get_nearest_node(
        buildings, nodes, edges, buildings["edge_index"]
    )


    tessellation[buildings.columns.drop(["geometry", "street_index"])] = (
        buildings.drop(columns=["geometry", "street_index"])
    )

    # Blocks
    blocks, tessellation_id = momepy.generate_blocks(
        tessellation, streets, buildings
    )

    # buildings["bID"] = tessellation_id[tessellation_id.index >= 0]
    # tessellation["bID"] = tessellation_id

    # Merged
    merged = tessellation.merge(
        edges.drop(columns="geometry"),
        left_on="edge_index",
        right_index=True,
        how="left",
    )
    merged = merged.merge(
        nodes.drop(columns="geometry"),
        left_on="node_index",
        right_index=True,
        how="left",
    )


    # Extending morphometrics with neighbourhood distributions
    percentiles = []
    for column in merged.columns.drop(
        [
            "street_index",
            "node_index",
            "edge_index",
            "nodeID",
            "mm_len",
            "node_start",
            "node_end",
            "geometry",
        ]
    ):
        perc = momepy.percentile(merged[column], queen_3)
        perc.columns = [f"{column}_" + str(x) for x in perc.columns]
        percentiles.append(perc)

    percentiles_joined = pd.concat(percentiles, axis=1)
    percentiles_joined.head()

    return(
        buildings, 
        streets, 
        tessellation, 
        blocks, 
        merged, 
        percentiles_joined)

