# ---------------------------------------
# FastAPI and related imports
# ---------------------------------------
from fastapi import FastAPI, Path, HTTPException, Query 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

# ---------------------------------------
# Pydantic model for patient
# ---------------------------------------
class Patient(BaseModel):
    # Required patient ID with description and example
    id: Annotated[str, Field(..., description='ID of patient', example='P001')]

    # Basic patient info
    name: Annotated[str, Field(..., description='Name of patient')]
    city: Annotated[str, Field(..., description='City of patient')]
    age: Annotated[int, Field(..., description='Age of patient', gt=0, lt=120)]

    # Restrict gender to specific choices
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of patient')]

    # Physical measurements with constraints
    height: Annotated[float, Field(..., gt=0, description='Height of patient in mts.')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of patient in kg.')]

    # Computed property: BMI calculated dynamically
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    # Computed property: health verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 30:
            return 'normal'
        else:
            return 'obese'

# ---------------------------------------
# Pydantic model for update operation
# ---------------------------------------
class PatientUpdate(BaseModel):
    # All fields optional for partial updates
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]  # 🟠 Note: mismatch with main model ('others')
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# ---------------------------------------
# Helper functions for data loading/saving
# ---------------------------------------
def load_data():
    with open('patients_info.json', 'r') as f:
        data = json.load(f)  # Load data from JSON file
    return data

def save_data(data):
    with open('patients_info.json', 'w') as f:
        json.dump(data, f)  # Save data to JSON file

# ---------------------------------------
# FastAPI app instance
# ---------------------------------------
obj = FastAPI()

# Root route - health check
@obj.get("/")
def patient_info():
    return {"message": "patients management system api"}

# About endpoint - info about API purpose
@obj.get("/about")
def about():
    return {"message": " Fully functional API to manage your patient records"}

# ---------------------------------------
# GET: View all patients
# ---------------------------------------
@obj.get("/view")
def view():
    data = load_data()
    return data

# ---------------------------------------
# GET: View single patient by ID
# ---------------------------------------
@obj.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of patient in the DB", example='P001')
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

# ---------------------------------------
# GET: Sort patient list by height/weight/bmi
# ---------------------------------------
@obj.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description='sort on the basis on height, weight or bmi'),
    order: str = Query('asc', description='sort in ascending or descending order')
):
    valid_fields = ['height', 'weight', 'bmi']

    # Check for valid field
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')

    # Check for valid order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order, choose asc or desc')

    data = load_data()

    # Determine sort direction
    sort_order = True if order == 'desc' else False

    # 🟠 bmi is not stored in raw JSON, so sorting by it may give 0 unless precomputed
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

# ---------------------------------------
# POST: Create a new patient
# ---------------------------------------
@obj.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    # Check if ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # Save patient data without ID (ID is the key)
    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

# ---------------------------------------
# PUT: Update existing patient data
# ---------------------------------------
@obj.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    # Ensure patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found.')

    # Get existing patient info
    existing_patient_info = data[patient_id]

    # Extract only provided (non-null) fields from request
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Update fields
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # Recompute BMI/verdict by recreating full Pydantic model
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    # Dump updated model back to dict and remove ID
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    # Save updated patient data
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient updated successfully.'})

# ---------------------------------------
# DELETE: Remove a patient by ID
# ---------------------------------------
@obj.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    # Ensure patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found.')

    # Delete patient
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient records are deleted.'})
