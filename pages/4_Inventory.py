import streamlit as st
from utils.db import SelectData
import pandas as pd
from st_aggrid import AgGrid
from streamlit_option_menu import option_menu



select_handler = SelectData()


selected = option_menu(
    None,
    ['Home', 'Items', 'Warehouse'],
    orientation='horizontal'
)

st.title('Inventory')
headers = [['item_id', 'item_name', 'category', 'warehouse_id', 'warehouse_name', 'warehouse_loc', 'qty']]
inventory = select_handler.get_current_stock()
data = pd.DataFrame(inventory, columns=['item_id', 'item_name', 'category', 'warehouse_id', 'warehouse_name', 'warehouse_loc', 'qty'])
AgGrid(data)