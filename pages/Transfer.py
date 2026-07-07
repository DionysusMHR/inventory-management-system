import streamlit as st
from utils.db import InsertData, SelectData


insert_handler = InsertData()
select_handler = SelectData()

st.title('Transfer between warehouses')
with st.form(key='transfer_form'):
    name = st.text_input('Name')
    from_warehouse = st.text_input('From Warehouse')
    to_warehouse = st.text_input('To Warehouse')
    qty = st.number_input('Quantity')
    desc = st.text_area('Description')
    sub_btn = st.form_submit_button('Submit')

if sub_btn is True:
    item_id = select_handler.get_item_id(item_name=name)
    from_warehouse_id = select_handler.get_warehouse_id(warehouse_name=from_warehouse)
    to_warehouse_id = select_handler.get_warehouse_id(warehouse_name=to_warehouse)

    insert_handler.insert_transactions_table(
        item_id=item_id,
        warehouse_id=from_warehouse_id,
        type_='OUT',
        qty=qty,
        desc=desc
    )

    insert_handler.insert_inventory_table(
        warehouse_id=from_warehouse_id,
        item_id=item_id,
        qty=-qty
    )

    insert_handler.insert_transactions_table(
        item_id=item_id,
        warehouse_id=to_warehouse_id,
        type_='IN',
        qty=qty,
        desc=desc
    )

    insert_handler.insert_inventory_table(
        warehouse_id=to_warehouse_id,
        item_id=item_id,
        qty=qty
    )

    st.success('The operation was successful')
    