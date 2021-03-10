### Python REST API (FastAPI, SQLAlchemy, PostgreSQL)
 
Install dependencies:
</br>
`pip install -r requirements.txt`


Setting database connection on main.py
```python
API_HOST = 'localhost'
API_DATABASE = 'wo'
API_DBUSER = 'postgres'
API_DBPASSWORD = 'awizindo'
API_DBPORT = '5432'
```


Running:
</br>
`uvicorn main:app --reload`

Running using custom port:
</br>
`uvicorn --port 8000 --host 127.0.0.1 main:app --reload`

<strong>--reload</strong> to make server automatically reload if any update.

Auto Generate Documentation and Web Testing:
`http://127.0.0.1:8000/docs`





 </br> </br>
Regards </br>
**Ari Abimanyu**
