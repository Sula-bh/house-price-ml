import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model/house_price_model.pkl")

df = pd.read_csv('data/processed/clean_housing.csv')

st.title("🏠 House Price Prediction")

st.write("Enter house details to predict price")


land_area = st.number_input("Land Area (Aana)", min_value=1.0)
road_access = st.number_input("Road Access (Feet)", min_value=1.0)
floor = st.number_input("Number of Floors", min_value=1.0)
bedroom = st.number_input("Bedrooms", min_value=1)
bathroom = st.number_input("Bathrooms", min_value=1)
house_age = st.number_input("Age of House (Years)", min_value=1)

facing = st.selectbox(
    "Facing",
    ["east", "west", "north", "south", "north-east", "south-east", "north-west", "south-west"]
)

locations = sorted(df['LOCATION'].unique())
location = st.selectbox(
    "Location",
    locations
)

st.write("Amenities: ")
has_drainage = st.checkbox("Drainage")
has_parking = st.checkbox("Parking")
has_drinking_water = st.checkbox("Drinking Water")
has_marbel = st.checkbox("Marbel")
has_power_backup = st.checkbox("Power Backup")
has_earthquake_resistant = st.checkbox("Earthquake Resistant")
has_garden = st.checkbox("Garden")
has_parquet = st.checkbox("Parquet")
has_modular_kitchen = st.checkbox("Modular Kitchen")

if st.button("Predict Price"):

    input_data = pd.DataFrame({
        "LAND_AREA": [land_area],
        "ROAD_ACCESS": [road_access], 
        "FLOOR": [floor],
        "BEDROOM": [bedroom],
        "BATHROOM": [bathroom],
        "FACING": [facing],
        "LOCATION": [location],
        "AMENITY_COUNT": [sum([has_drainage, has_parking, 
                               has_drinking_water, has_marbel, 
                               has_power_backup, has_earthquake_resistant, 
                               has_garden, has_parquet, has_modular_kitchen])],
        "has_drainage": [has_drainage],
        "has_parking": [has_parking],
        "has_drinking_water": [has_drinking_water],
        "has_marbel": [has_marbel],
        "has_power_backup": [has_power_backup],
        "has_earthquake_resistant": [has_earthquake_resistant],
        "has_garden": [has_garden],
        "has_parquet": [has_parquet],
        "has_modular_kitchen": [has_modular_kitchen],
        "house_age": [house_age],
        "bath_per_bed": [bathroom/bedroom],
        "area_road_interaction": [land_area*road_access],
        "area_bedroom": [land_area*bedroom],
    })

    prediction = model.predict(input_data)

    import numpy as np
    price = np.expm1(prediction[0])

    st.success(f"💰 Estimated Price: Rs. {price:,.0f}")