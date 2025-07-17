# Import FastAPI from fastapi module
from fastapi import FastAPI

# Create instance of FastAPI for web app
app = FastAPI()

# Define a rule using decorator: when someone access "/" this function will run
@app.get("/")
def hello():
    return {'message': 'Hello World'}

@app.get('/about')
def about():
    return {'message': 'CampusX is an education platform.'}

# Run command ------>     uvicorn main:app --reload
# uvicorn → the server that runs FastAPI
# main → the filename (main.py)
# app → the FastAPI instance (app = FastAPI())
# --reload → auto-restarts the server when you change your code (good for development)
