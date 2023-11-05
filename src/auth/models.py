from pydantic import BaseModel


class UserForReg(BaseModel):
    username: str
    first_name: str
    last_name: str
    passw: str
    mail: str
    mobile_telephone: str
    address: str