from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude_unset=True)

# exclude_unset is a parameter that can be used with the model_dump method to exclude fields that were not explicitly set when creating the model instance.
# This is useful for scenarios where you want to serialize only the fields that have been provided with values, and ignore any fields that have default values or were not included in the input data.

print(temp)
print(type(temp))
