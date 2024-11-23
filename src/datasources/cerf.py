import pycountry

from src.constants import ISO3S
from src.utils import blob_utils


def load_cerf(date_acessed: str = "2024-11-22"):
    blob_name = f"{blob_utils.PROJECT_PREFIX}/raw/cerf/AllocationsByYear_{date_acessed}.xlsx"
    df = blob_utils.load_excel_from_blob(blob_name)
    # get country names from ISO3s
    country_names = [
        pycountry.countries.get(alpha_3=iso3).name for iso3 in ISO3S
    ]
    df = df[
        (df["Country"].isin(country_names))
        & (df["Emergency"] == "Flood")
        & (df["Window"] == "Rapid Response")
    ]
    df["iso3"] = df["Country"].apply(
        lambda x: pycountry.countries.get(name=x).alpha_3.lower()
    )
    # assume that allocation was for previous year if before May
    df["effective_year"] = df["Allocation date"].apply(
        lambda x: x.year - 1 if x.month < 5 else x.year
    )
    return df
