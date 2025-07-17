from fastapi import FastAPI, Path, HTTPException, Query 
import json


# functions to load patient's data from json file
def load_data():
    with open('patients_info.json', 'r') as f:
        data = json.load(f)                     # load data in json file
    return data

# create the FastAPI app instance
obj = FastAPI()

#Root endpoint: Basic info message
@obj.get("/")
def patient_info():
    return {"message": "patients management system api"}

# About endpoint: describe the purpose of API
@obj.get("/about")
def about():
    return {"message": " Fully functional API to manage your patient records"}

# view all the patients
@obj.get("/view")
def view():
    data = load_data()
    return data

# view specific patient by ID
@obj.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description="ID of patient in the DB", examples={'example1':{"value":'P001'}})):
    #load all the patients
    data = load_data()

    # if patient ID exists return that patient's data
    if patient_id in data:
        return data[patient_id]
    
    # otherwise raise a 404 error
    raise HTTPException(status_code = 404 , detail = 'Patient not found')

# sort patient's data by given field
@obj.get("/sort")
def sort_patients(sort_by : str = Query(..., description = ' sort on the basis on height, weight or bmi'), order: str = Query('asc',  description = 'sort in ascending or descending order')):
    
    #validate field
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invalid field select from {valid_fields}')
    
    # validate sort order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = f'Invalid order select between asc and desc')
    
    data = load_data()

    # determine sort direction
    sort_order = True if order == 'desc' else False

    # sort the data by specified field
    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by, 0), reverse= sort_order)

    return sorted_data 
