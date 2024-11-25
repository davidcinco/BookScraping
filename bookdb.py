import psycopg2

class BookDB:
    globalConnection = None
    
    def databaseConnection(self):
        try:        
            con = psycopg2.connect(
                database="bookscrapingdb",
                host="127.0.0.1",
                user="postgres",
                password="1234",
                port="5433"
            )
            self.globalConnection = con
            print("Connection Completed.")
        except ConnectionError as e:
            print(f"ConnectionError happened {e}")
        except Exception as e:
            print(f"Exception happened: {e}") 
            
    def createBookTable(self):
        connection = self.globalConnection.cursor()
        try:
            connection.execute("""
            CREATE TABLE books(
                id serial primary key,
                title varchar(255) not null,
                rating int,
                price decimal(4,2) not null,
                stock boolean not null
            )
            """)
            self.globalConnection.commit()
            connection.close()
        except ConnectionError as e:
            print(f"ConnectionError Happened: {e}")
        except Exception as e:
            print(f"An Exception Happened: {e}")
            
    def addBook(self, book):
        connection = self.globalConnection.cursor()
        try:
            connection.execute("""
                INSERT INTO books(title, rating, price, stock) VALUE(%s, %s, %s, %s)""", 
                (book[0], book[1], book[2], book[3])
                )
            self.globalConnection.commit()
            connection.close()
            print(f"Book [{book[0]}] added.")
        except ConnectionError as e:
            print(f"ConnectionError Happened: {e}")
        except Exception as e:
            print(f"An Exception Happened: {e}")
                    
book = BookDB()
book.databaseConnection()
    