import sqlite3

class bookSqlite:
    connection = None
    
    def __init__(self):
        self.connection = sqlite3.connect("books_data.db")
        
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
        """
        CREATE TABLE IF NOT books_sqlite
        (
            id serial primary key,
            title varchar(255) not null UNIQUE,
            rating int,
            price decimal(4,2) not null,
            stock boolean not null
        )
        """
        )
        
        
db = bookSqlite()