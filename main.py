from fastapi import FastAPI

from api.router import router

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
