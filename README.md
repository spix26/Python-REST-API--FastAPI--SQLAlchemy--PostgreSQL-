### Python REST API (FastAPI, SQLAlchemy, PostgreSQL)
 
Install dependencies:

`pip install -r requirements.txt`

Setting database connection on main.py
API_HOST = 'localhost'
API_DATABASE = 'wo'
API_DBUSER = 'postgres'
API_DBPASSWORD = 'awizindo'
API_DBPORT = '5432'

Running:
`uvicorn main:app --reload`

Running using custom port:
`uvicorn --port 8000 --host 127.0.0.1 main:app --reload`

--reload to make server automatically reload if any update.

Auto Generate Documentation and Web Testing:
`http://127.0.0.1:8000/docs`






Regards
**Ari Abimanyu**
