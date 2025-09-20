
from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi import APIRouter
from data.filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

from data.filehandler import (
    save_json,
    load_json,
    add_user,
    add_basket,
    add_item_to_basket,
)

from fastapi.encoders import jsonable_encoder

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)   
def adduser(user: User) -> User:
    try:
        add_user(user.dict())
        user_json = jsonable_encoder(user)
        return JSONResponse(content=user_json, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        new_basket = {"id": userid * 100 +1, "user_id": userid, "items": []}
        add_basket(new_basket)
        return JSONResponse(content=new_basket, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        basket = get_basket_by_user_id(userid)
        if not basket:
            raise HTTPException(status_code=422, detail="Kosár nem található.")

        add_item_to_basket(userid, item.dict())

        ujKosar = get_basket_by_user_id(userid)
        return JSONResponse(content=ujKosar, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, ujItem: Item) -> Basket:
    try:
        data = load_json()
        basket = get_basket_by_user_id(userid)
        items = basket["items"]

        for i in range(len(items)):
            if items[i]["item_id"] == itemid:
                items[i] = ujItem.dict()
                break
        else:
            raise ValueError("A megadott termék nem található a listában.")

        for kosar in data["Baskets"]:
            if kosar["user_id"] == userid:
                kosar["items"] = items
                break

        save_json(data)

        ujKosar = {"id": basket["id"], "user_id": userid, "items": items}
        return JSONResponse(content=ujKosar, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        data = load_json()
        basket = get_basket_by_user_id(userid)
        items = basket["items"]

        for item in items:
            if item["item_id"] == itemid:
                items.remove(item)
                break
        else:
            raise ValueError("ATörlendő termék nem talalható")

        for kosar in data["Baskets"]:
            if kosar["user_id"] == userid:
                kosar["items"] = items
                break

        save_json(data)

        ujKosar = {"id": basket["id"], "user_id": userid, "items": items}
        return JSONResponse(content=ujKosar, status_code=200)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e2:
        raise HTTPException(status_code=422, detail=str(e2))

@routers.get('/user')
def user(userid: int) -> User:
    try:
        user_data = get_user_by_id(userid)
        return JSONResponse(content=user_data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@routers.get('/users')
def users() -> list[User]:
    all_users = get_all_users()
    return JSONResponse(content=all_users, status_code=200)

@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    try:
        items = get_basket_by_user_id(userid)
        return JSONResponse(content=items, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    try:
        total_price = get_total_price_of_basket(userid)
        return JSONResponse(content={"total_price": total_price}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))



