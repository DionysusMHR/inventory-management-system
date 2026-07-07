import streamlit as st
from utils.db import SelectData


select_handler = SelectData()

st.title('Inventory')
headers = [['item_id', 'item_name', 'category', 'warehouse_id', 'warehouse_name', 'warehouse_loc', 'qty']]
inventory = select_handler.get_current_stock()
st.table(headers + inventory)