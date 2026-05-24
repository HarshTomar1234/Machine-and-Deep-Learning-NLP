from fastapi import FastAPI, Path , HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import List, Dict, Annotated, Literal, Optional


import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal weight'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

    


@app.get("/")

def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")

def about():
    return {"message": "A fully functional API to manage patient records!"}

@app.get("/view")

def view_patients():
    data = load_data()
    return data



@app.get('/patient/{patient_id}')

def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples="P003")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi", examples="height"), order: str = Query("asc", description="Sort order: asc or desc", examples="asc")):
    data = load_data()
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter select between 'asc' and 'desc'")
    
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=sort_order)
    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    
    # existing_patient_info --> pydantic object --> update bmi + verdict --> dict --> save in json file
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info) # validation

    existing_patient_info = patient_pydantic_object.model_dump(exclude="id")

    # adding id back to the dict before saving in json file
    data[patient_id] = existing_patient_info

    # save the updated data back to the json file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})