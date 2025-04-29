import polars as pl
from typing import List

def get_all_cities(path: str) -> List[str]:
    df = pl.read_excel(path, sheet_name="cities")
    lst = df["city"].to_list()
    
    return lst