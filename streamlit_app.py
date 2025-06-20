# Import python packages
import requests

import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write(f"The name on your Smoothie will be: {name_on_order}")

cnx = st.connection("snowflake")
session = cnx.session()
fruit_options_df = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
)
st.dataframe(data=fruit_options_df, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options_df,
    max_selections=5,
)

if ingredients_list:
    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}"
        )
        sf_df = st.dataframe(
            data=smoothiefroot_response.json(), use_container_width=True
        )

    ingredients_string = " ".join(ingredients_list)
    my_insert_stmt = f"insert into smoothies.public.orders(ingredients, name_on_order) values ('{ingredients_string}','{name_on_order}')"

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
