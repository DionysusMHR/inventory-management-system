import streamlit as st
from utils.db import InsertData, SelectData


insert_handler = InsertData()
select_handler = SelectData()


st.title('Input Item')

with st.form(key='input_form'):
    name = st.text_input('Name')
    warehouse = st.text_input('Warehouse')
    qty = st.number_input('Quantity')
    desc = st.text_area('Description')
    sub_btn = st.form_submit_button('Submit')

if sub_btn is True:
    item_id = select_handler.get_item_id(item_name=name)
    warehouse_id = select_handler.get_warehouse_id(warehouse_name=warehouse)

    insert_handler.insert_transactions_table(
        item_id=item_id,
        warehouse_id=warehouse_id,
        type_='IN',
        qty=qty,
        desc=desc
    )

    insert_handler.insert_inventory_table(
        warehouse_id=warehouse_id,
        item_id=item_id,
        qty=qty
    )

    st.success('The operation was successful')
