import pandas as pd
import numpy as np
import re
import ast
from itertools import chain
from bikram_sambat import date

def clean_price(price):
    if pd.isna(price):
        return np.nan
    price = price.replace("Rs.", "").strip()
    if "/" in price or "price on call" in price.lower():
        return np.nan
    price_lower = price.lower()
    if "cr" in price_lower:
        num = re.sub(r"[^\d.]", "", price.split("cr")[0])
        return float(num) * 10000000
    elif "lakh" in price_lower or "lac" in price_lower:
        num = re.sub(r"[^\d.]", "", re.split(r"la[ck]", price, flags=re.IGNORECASE)[0])
        return float(num) * 100000
    else:
        num = re.sub(r"[,]", "", price)
        num = re.sub(r"[^\d.]", "", num)
        return float(num) if num else np.nan
    
def convert_to_sqft(land_area):
    if pd.isna(land_area):
        return np.nan
    land_area = str(land_area).lower().strip()
    match = re.search(r'(\d+\.?\d*)', land_area)
    if not match:
        return np.nan
    value = float(match.group(1))
    if 'kattha' in land_area:
        return value * 125.44  
    elif 'aana' in land_area:
        return value * 31.36   
    elif 'sq. ft' in land_area or 'sqft' in land_area:
        return value
    elif 'sq. mtr' in land_area or 'sqm' in land_area:
        return value * 10.764  
    else:
        return value  
    
def process_road_access(x):
    if pd.isna(x):
        return np.nan
    numbers = re.findall(r'\d+\.?\d*', str(x))
    if not numbers:
        return np.nan
    elif len(numbers) == 1:
        return float(numbers[0])
    else:
        return np.mean([float(numbers[0]), float(numbers[1])])
    
def clean_facing(df):
    df["FACING"] = df["FACING"].str.lower().str.strip()

    df["FACING"] = df["FACING"].replace({
        "south east": "south-east",
        "east/south": "south-east",
        "east-south": "south-east",
        "north east": "north-east",
        "north- east": "north-east",
        "east-north": "north-east",
        "north/east": "north-east",
        "south west": "south-west",
        "west-south": "south-west",
        "north west": "north-west",
        "west / north": "north-west",
        "west-north": "north-west",
    })

def clean_location(df):
    df["LOCATION"] = (
        df["LOCATION"]
        .astype(str)
        .str.split(",")
        .str[-1]
        .str.strip()
        .str.title()
    )
    df["LOCATION"] = df["LOCATION"].replace({
        "Karhmandu": "Kathmandu",
        "Kathmandhu": "Kathmandu",
        "Kathmndu": "Kathmandu",
        "Narayanthan": "Kathmandu",
        "Rumba Chowk": "Kathmandu",
        "Sitapaila": "Kathmandu",
        "Sukedhara": "Kathmandu",
        "Swoyambhu": "Kathmandu",
        "Imadol": "Lalitpur",
        "Undefined": "Other",
        
    })


def preprocess_data(df):
    df.drop("TITLE",axis=1,inplace=True)

    df["PRICE"] = df["PRICE"].apply(clean_price)

    df = df.dropna(subset=['PRICE'])

    clean_location(df)

    df["LAND_AREA"] = df["LAND AREA"].apply(convert_to_sqft)

    df["ROAD_ACCESS"] = df["ROAD ACCESS"].apply(process_road_access)

    clean_facing(df)

    df["BUILT_YEAR"] = df["BUILT YEAR"].str.extract(r"(\d+)").astype(float)

    df["AMENITY_COUNT"] = df["AMENITIES"].apply(lambda x: len(ast.literal_eval(x)) if pd.notna(x) else 0)

    df["AMENITIES"] = df["AMENITIES"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

    all_amenities = list(chain.from_iterable(df["AMENITIES"]))
    top_amenities = pd.Series(all_amenities).value_counts().head(10).index.tolist()

    for amenity in top_amenities:
        df[f"has_{amenity.lower().replace(' ', '_')}"] = df["AMENITIES"].apply(lambda x: amenity in x)

    df.drop(["BUILDUP AREA","LAND AREA","ROAD ACCESS","BUILT YEAR","PARKING","AMENITIES"], axis=1, inplace=True)

    df["LAND_AREA"].fillna(df["LAND_AREA"].median(), inplace=True)

    df["ROAD_ACCESS"].fillna(df["ROAD_ACCESS"].median(), inplace=True)

    df["FACING"].fillna(df["FACING"].mode()[0], inplace=True)

    df["FLOOR"].fillna(df["FLOOR"].median(), inplace=True)
    df["BEDROOM"].fillna(df["BEDROOM"].median(), inplace=True)
    df["BATHROOM"].fillna(df["BATHROOM"].median(), inplace=True)
    df["BUILT_YEAR"].fillna(df["BUILT_YEAR"].median(), inplace=True)
    current_year = date.today().year
    df["house_age"] = current_year - df["BUILT_YEAR"]
    df.drop("BUILT_YEAR",axis=1,inplace=True)

    df["bath_per_bed"] = np.where(
        df["BEDROOM"] > 0,
        df["BATHROOM"] / df["BEDROOM"],
        np.nan
    )
    df["bath_per_bed"].fillna(df["bath_per_bed"].median(), inplace=True)
    df["area_road_interaction"] = df["LAND_AREA"] * df["ROAD_ACCESS"]
    df["area_bedroom"] = df["LAND_AREA"] * df["BEDROOM"]

    return df