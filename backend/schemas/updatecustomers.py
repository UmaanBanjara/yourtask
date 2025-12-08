from pydantic import BaseModel , EmailStr
from typing import Optional
class UpdateCustomerCheck(BaseModel):
    first_name : Optional[str] | None
    last_name : Optional[str] | None
    email : Optional[EmailStr] | None
    phone_number : Optional[str] | None
    address : Optional[str] | None
    city : Optional[str] | None