from fastapi import FastAPI

from api.router import router
from services.database import init_database

app = FastAPI()
init_database()
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
