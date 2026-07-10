import streamlit as st
from utils.db import InsertData


handler = InsertData()


st.title('Define Basic Information')
st.divider()


st.header('Items')
with st.form(key='items', enter_to_submit=False, clear_on_submit=True):
    name = st.text_input('Name')
    category = st.text_input('Category')
    unit = st.text_input('Unit')
    min_stock = st.number_input('Min Stock', min_value=0.0)
    item_sub_btn = st.form_submit_button('Submit')
if item_sub_btn is True:
    handler.insert_items_table(name, category, unit, min_stock)
    st.success('The operation was successful')


st.header('Warehouse')
with st.form(key='wh', enter_to_submit=False, clear_on_submit=True):
    name = st.text_input('Name')
    loc = st.text_input('Location')
    wh_sub_btn = st.form_submit_button('Submit')
if wh_sub_btn is True:
    handler.insert_warehouses_table(name, loc)
    st.success('The operation was successful')



st.header('Users')
with st.form(key='users', enter_to_submit=False, clear_on_submit=True):
    username = st.text_input('Username')
    password = st.text_input('Password')
    role = st.text_input('Role')
    user_sub_btn = st.form_submit_button('Submit')
if user_sub_btn is True:
    handler.insert_users_table(username, password, role)
    st.success('The operation was successful')
    