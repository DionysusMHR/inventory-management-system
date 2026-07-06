import sqlite3
import pandas as pd


# Global Variable
DATABASE_PATH = r'database/db.sqlite3'
TABLES = ['items', 'warehouses', 'inventory', 'transactions', 'users']


class CreateTable:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_PATH)
        self.con.execute('PRAGMA foreign_keys = ON;')
        self.cur = self.con.cursor()

    def create_items_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL,
            min_stock REAL CHECK(min_stock >= 0)
            );'''
        )

    def create_warehouses_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS warehouses(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            loc TEXT NOT NULL
            );'''
        )

    def create_inventory_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY,
            warehouse_id INTEGER,
            item_id INTEGER,
            qty REAL,
            FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
            FOREIGN KEY (item_id) REFERENCES items(id),
            UNIQUE(warehouse_id, item_id)
            );'''
        )

    def create_transactions_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            warehouse_id INTEGER,
            type TEXT CHECK(type IN ('IN', 'OUT')),
            qty REAL CHECK(qty>=0),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            desc TEXT,
            FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
            );'''
        )

    def create_users_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
            );'''
        )


class DeleteTable:
    def delete_table(self, name:str)->None:
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(
            f'''DROP TABLE IF EXISTS {name}'''
        )
        con.commit()
        con.close()


class InsertData:
    
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_PATH)
        self.cur = self.con.cursor()

    def insert_items_table(self, name:str, category:str, unit:str, min_stock:float)->None:
        self.cur.execute(
            '''INSERT INTO items (name, category, unit, min_stock)
            VALUES (?, ?, ?, ?)''',
            (name, category, unit, min_stock)
        )
        self.con.commit()

    def insert_warehouses_table(self, name:str, loc:str)->None:
        self.cur.execute(
            '''INSERT INTO warehouses (name, loc)
            VALUES (?, ?)''',
            (name, loc)
        )
        self.con.commit()

    def insert_inventory_table(self, warehouse_id:int, item_id:int, qty:float)->None:
        self.cur.execute(
            '''INSERT INTO inventory (warehouse_id, item_id, qty)
            VALUES (?, ?, ?)
            ON CONFLICT(warehouse_id, item_id)
            DO UPDATE SET qty = qty + excluded.qty
            WHERE qty + excluded.qty >= 0''',
            (warehouse_id, item_id, qty)
        )
        self.con.commit()

    def insert_transactions_table(self, item_id:int, warehouse_id:int, type_:str, qty:float, desc:str)->None:
        self.cur.execute(
            '''INSERT INTO transactions (item_id, warehouse_id, type, qty, desc)
            VALUES (?, ?, ?, ?, ?)''',
            (item_id, warehouse_id, type_, qty, desc)
        )
        self.con.commit()

    def insert_users_table(self, username:str, password:str, role:str)->None:
        self.cur.execute(
            '''INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)''',
            (username, password, role)
        )
        self.con.commit()


class SelectData:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_PATH)
        self.cur = self.con.cursor()

    def get_current_stock(self)->list:
        self.cur.execute(
            '''SELECT
            i.id AS item_id,
            i.name AS item_name,
            i.category AS item_category,
            w.id AS warehose_id,
            w.name AS warehouse_name,
            w.loc AS warehouse_location,
            inv.qty AS current_stock
            FROM inventory inv
            INNER JOIN items i ON inv.item_id = i.id
            INNER JOIN warehouses w ON inv.warehouse_id = w.id
            ORDER BY i.name, w.name
            '''
        )
        rows = self.cur.fetchall()
        return rows


class DeleteRecords:
    def delete_all(self, name:str)->None:
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(
            f'''DELETE FROM {name};'''
        )
        con.commit()
        con.close()
    


# define functions for better management database

def create_tables():
    create = CreateTable()
    create.create_inventory_table()
    create.create_items_table()
    create.create_transactions_table()
    create.create_users_table()
    create.create_warehouses_table()

def delete_tables():
    delete = DeleteTable()
    for t in TABLES:
        delete.delete_table(name=t)


if __name__ == "__main__":
    #delete_tables()
    #create_tables()

    insert_handle = InsertData()
    #insert_handle.insert_items_table('turbo_fan', 'fan', 'Pcs', 20)
    #insert_handle.insert_warehouses_table('product_wh', 'site-2')
    #insert_handle.insert_inventory_table(2, 1, 100)
    #insert_handle.insert_transactions_table(1, 1, 'IN', 200, 'be anbar material dar site 1')
    
    select_handle = SelectData()
    #rows = select_handle.get_current_stock()
    #df = pd.DataFrame(rows, columns=['item_id', 'item_name', 'category', 'warehose_id', 'warehouse_name', 'warehouse_loc', 'current_stock'])
    #df.to_excel('inventory3.xlsx')
    #df.to_markdown('inventory.md')

    delete_handle = DeleteRecords()
    #delete_handle.delete_all('transactions')