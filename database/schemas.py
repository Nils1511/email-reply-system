from pydantic import BaseModel

class EquipmentBase(BaseModel):
    name: str
    category: str
    description: str
    price: float
    availability: bool

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int

    class Config:
        orm_mode = True