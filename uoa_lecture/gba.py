import geopandas as gpd

def process_gba_buildings(
    raw_parquet_file, 
    geometry_maskfile, 
    mask_area, 
    output_file):
    
    local_crs = 2193
    # Load Global Building Atlas - AKL - lower North Island
    buildings_full = gpd.read_parquet(raw_parquet_file)
    buildings_full = buildings_full.to_crs(local_crs)
    # Clip to urban area
    mask_df = gpd.read_file(geometry_maskfile)
    mask_df = mask_df.to_crs(local_crs)

    if "urban" in geometry_maskfile:
        mask_geom = mask_df.query('UR2025_V1_00_NAME in @mask_area')
    else:    
        mask_geom = mask_df.query('name in @mask_area')

    buildings = gpd.clip(buildings_full, mask_geom)

    # Tidying up
    buildings = (buildings[buildings.geom_type == "Polygon"]
            .reset_index(drop=True)
        )
    # Two-step process for removing duplicates
    # https://github.com/geopandas/geopandas/issues/3098#issuecomment-1839326589
    # Need this as well to remove pesky geometry duplicates
    buildings["geometry"] = buildings.normalize()
    # buildings.drop_duplicates()

    # https://github.com/pysal/momepy/issues/721#issuecomment-3442038750
    buildings = buildings[buildings.geometry.duplicated() == False]
    
    # Only keep geometry and height
    buildings = buildings.explode()[['geometry', 'height']]

    # Save
    buildings.to_parquet(output_file)
    return
