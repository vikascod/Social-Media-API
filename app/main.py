from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import user, post, auth, vote, comment, chat, follow
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(follow.router)
app.include_router(comment.router)
app.include_router(chat.router)


@app.get('/', tags=['Home'])
def home():
    return  {"message":"Welcome to Social page"}