from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://neondb_owner:npg_SUp1iMyYFH5h@ep-autumn-scene-a8lger8v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# with ConnectionPool(
#     # Example configuration
#     conninfo=DB_URI,
#     max_size=20,
# ) as pool:
#     checkpointer = PostgresSaver(pool)

#     # NOTE: you need to call .setup() the first time you're using your checkpointer
#     checkpointer.setup()

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # call .setup() the first time you're using the checkpointer
    checkpointer.setup()