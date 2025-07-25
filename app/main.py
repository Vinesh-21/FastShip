from contextlib import asynccontextmanager

from fastapi import FastAPI,Depends
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


app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
)


app.include_router(master_router)





### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
