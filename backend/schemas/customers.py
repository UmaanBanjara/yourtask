from pydantic import BaseModel, EmailStr, field_validator

class CustomerCheck(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
    city: str

    @field_validator('email')
    def validate_email(cls, email):
        if not email.endswith('@gmail.com'):
            raise ValueError('Email must end with @gmail.com')
        return email

    @field_validator('phone_number')
    def validate_phonenumber(cls, phone_number):
        if len(phone_number) != 10:
            raise ValueError('Phone number must have 10 digits')
        return phone_number
