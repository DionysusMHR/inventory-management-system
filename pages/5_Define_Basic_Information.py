import streamlit as st
from utils.db import InsertData, SelectData
from streamlit_option_menu import option_menu



insert_handler = InsertData()
select_handler = SelectData()

#load data lists
categories = select_handler.get_category_list()
locations = select_handler.get_location_list()
units = select_handler.get_unit_list()
items_table_data = select_handler.get_items_table()
items_name = select_handler.get_item_names()
warehoses_names = select_handler.get_warehouse_names()
categories = select_handler.get_category_list()
users = select_handler.get_users()



with st.sidebar:
    selected_sidebar = option_menu(
        None,
        [
            'Items',
            'Warehouse',
            'Category',
            'Location',
            'Unit',
            'Users'
        ],
        default_index=0
    )


st.title('Define Basic Information')
st.divider()

if selected_sidebar == 'Items':
    st.header('Items')
    with st.form(key='items', enter_to_submit=False, clear_on_submit=True):
        name = st.text_input('Name')
        category = st.selectbox('Category', categories, index=None)
        unit = st.selectbox('Unit', units, index=None)
        min_stock = st.number_input('Min Stock', min_value=0.0)
        item_sub_btn = st.form_submit_button('Submit')
    if item_sub_btn is True:
        if name in items_name:
            st.error("The item already defined.")
        else:
            insert_handler.insert_items_table(name, category, unit, min_stock)
            st.success('The operation was successful')

    headers_items_table = [['id', 'name', 'category', 'unit', 'min stock']]
    st.table(headers_items_table + items_table_data)


if selected_sidebar == 'Warehouse':
    st.header('Warehouse')
    with st.form(key='wh', enter_to_submit=False, clear_on_submit=True):
        name = st.text_input('Name')
        loc = st.selectbox('Location', locations, index=None)
        wh_sub_btn = st.form_submit_button('Submit')
    if wh_sub_btn is True:
        if name in warehoses_names:
            st.error("The warehouse already defined.")
        else:
            insert_handler.insert_warehouses_table(name, loc)
            st.success('The operation was successful')


if selected_sidebar == 'Category':
    st.header('Category')
    with st.form(key='category', enter_to_submit=False, clear_on_submit=True):
        category_name = st.text_input('Category')
        category_submit_btn = st.form_submit_button('Submit')
    if category_submit_btn is True:
        if category_name in categories:
            st.error("The category already defined.")
        else:
            insert_handler.insert_category_table(category_name)
            st.success('The operation was successful')


if selected_sidebar == 'Location':
    st.header('Location')
    with st.form(key='location', enter_to_submit=False, clear_on_submit=True):
        location_name = st.text_input('Location Name')
        location_address = st.text_input('Address')
        location_submit_btn = st.form_submit_button('Submit')
    if location_submit_btn is True:
        if location_name in locations:
            st.error("The location already defined.")
        else:
            insert_handler.insert_location_table(location_name, location_address)
            st.success('The operation was successful')


if selected_sidebar == 'Unit':
    st.header('Unit')
    with st.form(key='unit', enter_to_submit=False, clear_on_submit=True):
        desc = st.text_input('Desc')
        symbol = st.text_input('Symbol')
        unit_submit_btn = st.form_submit_button('Submit')
    if unit_submit_btn is True:
        if symbol in units:
            st.error("The unit already defined.")
        else:
            insert_handler.insert_unit_table(desc, symbol)
            st.success('The operation was successful')


if selected_sidebar == 'Users':
    st.header('Users')
    with st.form(key='users', enter_to_submit=False, clear_on_submit=True):
        username = st.text_input('Username')
        password = st.text_input('Password')
        role = st.text_input('Role')
        user_sub_btn = st.form_submit_button('Submit')
    if user_sub_btn is True:
        if username in users:
            st.error("The user already defined.")
        else:
            insert_handler.insert_users_table(username, password, role)
            st.success('The operation was successful')
    