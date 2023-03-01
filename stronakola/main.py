import uvicorn
from fastapi.middleware.cors import CORSMiddleware


#! FASTAPI part
from fastapi import FastAPI
from fastapi import FastAPI
from app.containers import Container
from app import endpoints

container = Container()
db = container.db()
db.create_database()
app = FastAPI()
app.container = container
app.include_router(endpoints.router)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
