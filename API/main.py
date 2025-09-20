from fastapi import FastAPI
from schemas.schema import ShopName
from routers.routes import routers as routes_router
from data.filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

from data.filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

'''
Útmutató a fájl használatához:

Ez a fájl a REST API main modulja. A futtatásához telepíteni kell a pip
csomagkezelővel a uvicorn és a fastapi csomagokat:

   pip install uvicorn, fastapi

vagy

   pip3 install uvicorn, fastapi

Ezután az alkalmazása  következő paranccsal futtatható a terminálban:

   uvicorn main:app --reload --port 9000

A port nem kötelező opció. 

A futó alkalmazás a következő URL-en érhető el:

   127.0.0.1:9000

A webes UI pedig az alábbi URL használatával:

   127.0.0.1:9000/docs

A dokumentáció pedig itt:

   127.0.0.1:9000/redoc

'''

app = FastAPI()
app.include_router(routes_router)

@app.get('/')
def route():
    return {'Wellcome in ': ShopName}    
