from pymongo import MongoClient
from mongo_crud.crud import DBCollectionCrudHandler
import os

if os.path.exists(".env"): # Carrega as variaveis de ambiente de desenvolvimento
    from dotenv import load_dotenv
    load_dotenv()

DATABASE_LOGIN = os.environ.get('DATABASE_LOGIN')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

if not DATABASE_LOGIN or not DATABASE_PASSWORD:
    print("\033[94m"+"DB:" + "\033[0m" + "\t  Database data available through .env file! Connecting...")
else:
    print("\033[94m"+"DB:" + "\033[0m" + "\t  Database env data available! Connecting...")

URL = f"mongodb+srv://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@cluster0.zj9tl.mongodb.net/Cluster0?"
client = MongoClient(URL)

DB = 'demap-sci'
db = client[DB]

crud_handler = DBCollectionCrudHandler(db)