from typing import List
import databases
import sqlalchemy 
from sqlalchemy import func, and_
from sqlalchemy.orm import Session, relationship, sessionmaker
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import urllib


# ======= Connection
host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'wo')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'awizindo')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username,db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL) 
metadata = sqlalchemy.MetaData()  

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()

# ======= SQLAlchemy Database Table
plu = sqlalchemy.Table(
    "pos_plushow",
    metadata,
    sqlalchemy.Column("pluid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("pluname", sqlalchemy.String), 
    sqlalchemy.Column("plutext", sqlalchemy.String),
)

# ####### Data Model
# ======= PLU
class PLUIn(BaseModel): 
    pluname: str 
    plutext: str

class PLU(BaseModel):
	pluid: int
	pluname: str 
	plutext: str

# ======= FastAPI
app = FastAPI(title = "REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Looks good."}

# ####### End Point
# ======= PLU 
@app.get("/plu/", response_model=List[PLU], status_code = status.HTTP_200_OK)
async def read_plu(skip: int = 0, take: int = 20):
    query = plu.select().order_by(plu.c.pluid.asc()).offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/plu/pagination/", response_model=List[PLU], status_code = status.HTTP_200_OK)
async def read_plu(start_pluid: int = 1, end_pluid: int = 10):
    query = plu.select().where(and_(plu.c.pluid >= start_pluid, plu.c.pluid <= end_pluid)).order_by(plu.c.pluid.asc())
    return await database.fetch_all(query)

@app.get("/plu/{plu_id}/", response_model=PLU, status_code = status.HTTP_200_OK)
async def read_plu(plu_id: int):
    query = plu.select().where(plu.c.pluid == plu_id)
    return await database.fetch_one(query)

@app.post("/plu/", response_model=PLU, status_code = status.HTTP_201_CREATED)
async def create_plu(pluin: PLUIn): 
	qry = session.query(func.max(plu.c.pluid).label("plu_id"))
	res = qry.one() 
	maxpluid = res.plu_id  
	pluid = maxpluid + 1 
	query = plu.insert().values(pluid=pluid, pluname=pluin.pluname, plutext=pluin.plutext)
	last_record_id = await database.execute(query)
	return {**pluin.dict(), "pluid": pluid}

@app.put("/plu/{plu_id}/", response_model=PLU, status_code = status.HTTP_200_OK)
async def update_plu(plu_id: int, payload: PLUIn):
    query = plu.update().where(plu.c.pluid == plu_id).values(pluname=payload.pluname, plutext=payload.plutext)
    await database.execute(query)
    return {**payload.dict(), "pluid": plu_id}

@app.delete("/plu/{plu_id}/", status_code = status.HTTP_200_OK)
async def delete_plu(plu_id: int):
    query = plu.delete().where(plu.c.pluid == plu_id)
    await database.execute(query)
    return {"message": "PLU with pluid: {} deleted successfully!".format(plu_id)}
