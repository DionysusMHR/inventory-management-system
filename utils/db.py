import sqlite3


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
    
    def get_item_id(self, item_name:str)->int:
        self.cur.execute(
            f'''SELECT id FROM items
            WHERE name = "{item_name}"'''
        )
        item_id = self.cur.fetchone()
        return item_id[0]
    
    def get_warehouse_id(self, warehouse_name:str)->int:
        self.cur.execute(
            f'''SELECT id FROM warehouses
            WHERE name = "{warehouse_name}"'''
        )
        warehouse_id = self.cur.fetchone()
        return warehouse_id[0]
    
    def get_item_names(self)->list:
        self.cur.execute(
            '''SELECT name FROM items'''
        )
        item_names = self.cur.fetchall()
        item_names = [row[0] for row in item_names]
        return item_names
    
    def get_warehouse_names(self)->list:
        self.cur.execute(
            '''SELECT name FROM warehouses'''
        )
        warehouse_names = self.cur.fetchall()
        warehouse_names = [row[0] for row in warehouse_names]
        return warehouse_names
    
    def get_qty(self, item_id, warehouse_id)->float:
        self.cur.execute(
            f'''SELECT qty FROM inventory
            WHERE item_id = "{item_id}"
            AND warehouse_id = "{warehouse_id}"'''
        )
        qty = self.cur.fetchone()[0]
        return qty


class DeleteRecords:
    def delete_all(self, name:str)->None:
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(
            f'''DELETE FROM {name};'''
        )
        con.commit()
        con.close()



if __name__ == "__main__":

    delete_handler = DeleteRecords()
    delete_handler.delete_all('warehouses')