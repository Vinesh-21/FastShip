from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
from app.database.session import create_db_tables, get_session


#MongoDB
from app.database.mongodb import connect_to_MongoDB,create_TTL_Indexing


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    await connect_to_MongoDB()
    await create_TTL_Indexing()
    yield


description="""
Delivery Managment System For Sellers And Delivery Partners

### Sellers
- Can Submit Shipments effortlessly

### Delivery Partners
- Auto Accept Shipments
- Track and Update Shipment Status
- On Status Updates Sends Mail and SMS To The Clients 

"""



app = FastAPI(

    title="FastShip",
    description=description,
    docs_url=None, #if None -> "/swagger" then Swagger Doc is now available in "http://localhost:8000/swagger" and not in '/docs'
    redoc_url=None,
    version="0.1.0",
    contact={
        "name": "FastShip Support",
        "url": "https://fastship.com/contact",
        "email": "support@fastship.com"
    },
    openapi_tags=[
        {
            "name":"Shipment",
            "description":"Operation Related to Shipments"
        },
        {
            "name":"Seller",
            "description":"Operation Related to Seller"
        },
        {
            "name":"Delivery Partner",
            "description":"Operation Related to Delivery Partner"
        }
    ],
    generate_unique_id_function=lambda route:route.name,
    # Server start/stop listener
    lifespan=lifespan_handler,
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,             
    allow_methods=["*"],                
    allow_headers=["*"],                
)

app.include_router(master_router)





### Scalar API Documentation
@app.get("/docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
