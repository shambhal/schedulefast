from fastapi import FastAPI
from api import cats,doctors,utils,cart,checkout,user,pms,orders,information,banners,config
from chat.routes import chat_router
from core.database import engine
#from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
from db import events
allowed_hosts = ["http://localhost:3000",'http://localhost', "*.example.com",'http://localhost/op33/']

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost(:\d+)?",
    allow_origins=allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cats.router, prefix="/cats")
app.include_router(chat_router,prefix='/chat')
#app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(doctors.router, prefix="/doctor", )
app.include_router(utils.router, prefix="/utils", )
app.include_router(cart.router, prefix="/cart", )
app.include_router(checkout.router, prefix="/checkout", )
app.include_router(user.router, prefix="/user", )
app.include_router(pms.router, prefix="/payments", )
app.include_router(orders.router, prefix="/orders", )
app.include_router(banners.router, prefix="/banner", )
app.include_router(information.router, prefix="/information", )
app.include_router(config.router, prefix="/config", )
'''
app2.include_router(products.router, prefix="/products", tags=["products"])
app2.include_router(cart.router, prefix="/cart", tags=["cart"])
app2.include_router(orders.router, prefix="/orders", tags=["orders"])
'''