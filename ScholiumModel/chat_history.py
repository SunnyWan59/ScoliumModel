from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver



DB_URI = "postgresql://neondb_owner:npg_SUp1iMyYFH5h@ep-autumn-scene-a8lger8v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

class DatabaseConnection:
    def __init__(self,
                 DB_URI: str = DB_URI, 
                 session_id: str = "test_session"):
        '''
        class for storing chat history in a postgres SQL database
        '''
        self.session_id = session_id
        self.DB_URI = DB_URI
        self.connection_pool = ConnectionPool(
                            conninfo=DB_URI,
                            max_size=20)
        self.connection = self.connection_pool.getconn()
        self.cursor = self.connection.cursor()
    
    def create_table(self, table_name: str = "chat_history"):
        '''
        creates table in the database, use only one time
        '''
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (session_id VARCHAR, role VARCHAR, content VARCHAR)")
        self.connection.commit()
    
    def close_connection(self):
        '''
        closes the connection
        '''
        self.cursor.close()
        self.connection_pool.putconn(self.connection)
        # Close all connections in the pool
        self.connection_pool.close()
        
class ChatHistory(DatabaseConnection):
    def __init__(self, 
                 DB_URI: str = DB_URI, 
                 session_id: str = "test_session",
                 table_name: str = "chat_history"):
        super().__init__(DB_URI, session_id)
        self.table_name = table_name
        # self.create_table(self.table_name)
        self.checkpointer = PostgresSaver(self.connection_pool)
        self.checkpointer.setup()
        
    
    
if __name__ == "__main__":
    ch = DatabaseConnection()
    ch.close_connection()