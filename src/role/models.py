from pydantic import BaseModel



class Role(BaseModel):
    acc_id: int
    role: str