# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose Your friuts you want in your custom Smoothie.
    """
)

name_on_order = st.text_input('Name On Smoothie')
st.write('The Name on your Smoothie with be ',name_on_order)


# option = st.selectbox(
#     "What is your favarite fruit!",
#     ("Bannana", "Strawberries", "Peaches"))

# st.write("Your favarite fruit is:", option)

# importing col from snowflake

from snowflake.snowpark.functions import col

# Get the current credentials
session = get_active_session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect(
    'Choose up for 5 ingredients',
    my_dataframe,
    max_selections = 5
)
if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '
    #st.write(ingredients_string)
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    #st.write(my_insert_stmt) #st.stop()
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


