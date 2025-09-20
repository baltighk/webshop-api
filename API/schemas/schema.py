from pydantic import BaseModel, EmailStr, Field

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

ShopName='Bolt'

class User(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        json_schema_extra = {
            "pelda": {
                "id": 1,
                "name": "Orban Viktor",
                "email": "zebratulajdonos@batida.com"
            }
        }


class Basket(BaseModel):
    id: int = Field(..., ge=0)
    user_id: int = Field(..., ge=0)
    items: list = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "pelda": {
                "id": 104,
                "user_id": 2,
                "items": []
            }
        }

class Item(BaseModel):
    item_id: int = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    brand: str = Field(..., min_length=1)
    price: float = Field(..., gt=0.0)
    quantity: int = Field(..., ge=1)

    class Config:
        json_schema_extra = {
            "pelda": {
                "item_id": 101,
                "name": "Szilva",
                "brand": "Palinka",
                "price": 70.99,
                "quantity": 3
            }
        }
