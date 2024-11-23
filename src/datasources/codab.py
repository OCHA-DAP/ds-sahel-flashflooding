import pandas as pd
import requests

from src.utils import blob_utils
from src.constants import AOI_ADM1_PCODES, ISO3S

FIELDMAPS_BASE_URL = "https://data.fieldmaps.io/cod/originals/{iso3}.shp.zip"


def get_blob_name(iso3: str = "bfa"):
    iso3 = iso3.lower()
    return f"{blob_utils.PROJECT_PREFIX}/raw/codab/{iso3}.shp.zip"


def download_codab_to_blob(iso3: str, clobber: bool = False):
    blob_name = get_blob_name(iso3=iso3)
    if not clobber and blob_name in blob_utils.list_container_blobs(
        name_starts_with=f"{blob_utils.PROJECT_PREFIX}/raw/codab/"
    ):
        print(f"{blob_name} already exists in blob storage")
        return
    url = FIELDMAPS_BASE_URL.format(iso3=iso3)
    response = requests.get(url)
    response.raise_for_status()
    blob_utils.upload_blob_data(blob_name, response.content, stage="dev")


def load_codab_from_blob(
    iso3: str, admin_level: int = 2, aoi_only: bool = False
):
    shapefile = f"{iso3}_adm{admin_level}.shp"
    gdf = blob_utils.load_gdf_from_blob(
        blob_name=get_blob_name(iso3),
        shapefile=shapefile,
        stage="dev",
    )
    if iso3 in ["nga", "tcd"] and admin_level == 0:
        # remove weird double adm0
        gdf = gdf.iloc[:1]
    if aoi_only:
        if iso3 in ["nga", "cmr"]:
            if admin_level == 0:
                gdf = blob_utils.load_gdf_from_blob(
                    blob_name=get_blob_name(iso3),
                    shapefile=f"{iso3}_adm1.shp",
                    stage="dev",
                )
            gdf = gdf[gdf["ADM1_PCODE"].isin(AOI_ADM1_PCODES.get(iso3))]
            if admin_level == 0:
                gdf = gdf.dissolve().drop(
                    columns=[x for x in gdf.columns if "ADM1" in x]
                )
    return gdf


def load_all_codabs(admin_level: int = 2, aoi_only: bool = False):
    gdfs = []
    for iso3 in ISO3S:
        gdfs.append(load_codab_from_blob(iso3, admin_level, aoi_only))
    return pd.concat(gdfs)
