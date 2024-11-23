from src.utils import blob_utils


def load_emdat(date_accessed: str = "2024-11-22"):
    blob_name = (
        f"{blob_utils.PROJECT_PREFIX}/raw/emdat/"
        f"emdat_africa_floods_accessed_{date_accessed}.xlsx"
    )
    return blob_utils.load_excel_from_blob(blob_name)
