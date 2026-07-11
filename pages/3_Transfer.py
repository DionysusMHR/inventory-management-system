import streamlit as st
from utils.db import InsertData, SelectData


insert_handler = InsertData()
select_handler = SelectData()

# load data lists
item_names = select_handler.get_item_names()
wh_names = select_handler.get_warehouse_names()

st.title('Transfer between warehouses')

with st.form(key='transfer_form', enter_to_submit=False, clear_on_submit=True):
    name = st.selectbox('Name', item_names, index=None)
    from_warehouse = st.selectbox('From Warehouse', wh_names, index=None)
    to_warehouse = st.selectbox('To Warehouse', wh_names, index=None)
    qty = st.number_input('Quantity')
    desc = st.text_area('Description')
    sub_btn = st.form_submit_button('Submit')

if sub_btn is True:
    item_id = select_handler.get_item_id(item_name=name)
    from_warehouse_id = select_handler.get_warehouse_id(warehouse_name=from_warehouse)
    to_warehouse_id = select_handler.get_warehouse_id(warehouse_name=to_warehouse)
    current_qty = select_handler.get_qty(item_id=item_id, warehouse_id=from_warehouse_id)

    if current_qty == None:
        st.error(
            '''The item in this warehouse has no inventory.'''
        )

    elif current_qty < qty:
        st.error(
            '''Operation encountered error:
            The amount of stock inventory is less than the requested value.'''
        )

    else:
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

        st.success('The operation was successful.')
    