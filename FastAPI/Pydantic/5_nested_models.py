from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Danny', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# temp = patient1.model_dump(include= {'name', 'age', 'address': {'city', 'state'}})

# print(type(temp))









# nested models in Pydantic allow you to define complex data structures by embedding one model within another.
# This is particularly useful for representing related data that naturally belongs together, such as a patient's vitals, address, or insurance information.


# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed
