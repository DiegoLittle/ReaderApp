from typing import List
from fastapi import Depends, FastAPI, HTTPException,Request,UploadFile,File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import crud, models, schemas,security
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from routers import files,papers,search,wiki
import re
from data_access.users import get_user,create_apple_user,apple_login,verify_refresh_token
import requests
import json
import time
import jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

app.include_router(files.router)
app.include_router(papers.router)
app.include_router(search.router)
app.include_router(wiki.router)

origins = "*"
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://localhost:5000",
    "http://localhost:3000",
"http://localhost:4444"
]
origins = "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.email)
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    db_user = crud.get_user_by_email(db, email=user.email)
    if (re.fullmatch(regex, user.email)==None):
        raise HTTPException(status_code=409, detail="Invalid Email Address")
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    # print(form_data.username)
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if not (security.verify_hash(form_data.password,db_user.salt).decode('utf-8') == db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # return {"message":"ERROR"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}

@app.get("/user",response_model=schemas.User)
async def get_current_user(token: schemas.Token,db: Session = Depends(get_db)):    
    email=security.get_current_user_email(token.access_token)
    db_user = crud.get_user_by_email(db, email=email)
    
    return db_user

@app.get("/user/notes")
async def get_current_user(access_token: str,db: Session = Depends(get_db)):
    print(access_token)
    email=security.get_current_user_email(access_token)
    db_user = crud.get_user_by_email(db, email=email)
    return crud.get_user_notes(db,db_user)

@app.post("/user/notes")
async def post_user_items(request:Request,access_token:str,db: Session = Depends(get_db)):
    # print(request.json())
    json = await request.json()
    print(json)
    # access_token = json["token"]["access_token"]
    email=security.get_current_user_email(access_token)
    db_user = crud.get_user_by_email(db, email=email)
    note = json["note"]
    
    try:
        crud.create_user_note(db,note,db_user.id)
    except IntegrityError:
        db.rollback()
        crud.update_user_note(db,note,db_user.id)
    
    # email=security.get_current_user_email(access_token)
    # db_user = crud.get_user_by_email(db, email=email)
    return {"message":json}

@app.put("/user/notes")
async def update_user_note(request:Request,access_token:str,db: Session = Depends(get_db)):
    print(request.json())
    json = await request.json()
    print(json)
    # access_token = json["token"]["access_token"]
    email=security.get_current_user_email(access_token)
    db_user = crud.get_user_by_email(db, email=email)
    note = json["note"]
    crud.update_user_note(db,note,db_user.id)
    return {"message":json}

@app.delete("/user/notes")
async def post_user_items(request:Request,access_token:str,db: Session = Depends(get_db)):
    json = await request.json()
    # access_token = json["token"]["access_token"]
    email=security.get_current_user_email(access_token)
    db_user = crud.get_user_by_email(db, email=email)
    note = json["note"]
    print(note)
    crud.delete_user_note(db,note,db_user.id)
    # email=security.get_current_user_email(access_token)
    # db_user = crud.get_user_by_email(db, email=email)
    return {"message":json}
    
#     # return test
# @app.post("/test")
# async def playground(request:Request):
#     json = await request.json()
#     print(json)
#     return {"message":json}

# # Replace with JWT Access token response
# @app.post("/login/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = security.get_user_by_email(db, email=user.email)
#     if (security.verify_hash(user.password,db_user.salt).decode('utf-8') == db_user.hashed_password):
#         return db_user
#     else:
#         raise HTTPException(status_code=400, detail="Invalid Login")
import base64


# app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     print(user.email)
#     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if (re.fullmatch(regex, user.email)==None):
#         raise HTTPException(status_code=409, detail="Invalid Email Address")
#     if db_user:
#         raise HTTPException(status_code=409, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     print(user.email)
#     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if (re.fullmatch(regex, user.email)==None):
#         raise HTTPException(status_code=409, detail="Invalid Email Address")
#     if db_user:
#         raise HTTPException(status_code=409, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

@app.post("/users_apple")
def create_user_apple(userRequest:schemas.UserCreateApple,db: Session = Depends(get_db)):

    create_apple_user(db=db,userRequest=userRequest)
    # print(userRequest.user.email)
    # print(userRequest.user.name.givenName)

    # # A JSON Web Token (JWT) that securely communicates information about the user to the app.
    # print(userRequest.identityToken)

    # # A token that the app uses to interact with the server.
    # print(userRequest.authorizationCode)

    # db_user = crud.get_user_by_email
def verify_id_token(id_token):
    headers = json.loads(base64.b64decode(id_token.split('.')[0]+"=="))
    payload = json.loads(base64.b64decode(id_token.split('.')[1]+"=="))
    signature = id_token.split('.')[2]
    print(headers)
    print(payload)
    print(signature)
    
    if payload['iss'] != "https://appleid.apple.com":
        return False
    
def get_client_secret():
    team_id = 'APR949UZ95'
    client_id = 'synesthesia.ReaderApp'
    # client_id = 'synesthesia.ReaderApp.client'
    key_id = 'GPD6T964V7'
    with open('apple_key.txt','r') as f:
        key = f.read()
    headers = {
    'alg':'ES256',
    'kid':key_id
    }
    claims = {
        'iss':team_id,
        'iat' : int(time.time()),
        'exp' : int(time.time() + 86400*180),
        'aud' : 'https://appleid.apple.com',
        'sub' : client_id,
    }
    client_secret = jwt.encode(claims, key, algorithm="ES256",headers=headers).decode('utf-8')
    return client_secret
def get_token_response(authorizationCode):
    client_id = 'synesthesia.ReaderApp'
    client_secret = get_client_secret()
    body = {
    'client_id': client_id,
    'client_secret':client_secret,
    'code':authorizationCode,
    'grant_type':"authorization_code"
    }
    headers = {'content-type': "application/x-www-form-urlencoded"}
    req = requests.post("https://appleid.apple.com/auth/token",data =body,headers=headers)
    token_response = req.json()
    return token_response
@app.post("/apple_login")
async def post_apple_login(UserLogin:schemas.UserLoginApple,db: Session = Depends(get_db)):
    client_id = 'synesthesia.ReaderApp'
    # keys_req = requests.get("https://appleid.apple.com/auth/keys")
    # JWKSet = keys_req.json()
    # apple_keys = JWKSet['keys']
    # print(UserLogin)
    # ecdsa_key = OpenSSL::PKey::EC.new IO.read key_file
    # key_file = 'apple_key.txt'
    # key = 'MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg3KrOWtEVoaRF1JB9+5I78ZGR3Z4HEcHay0ngzhMIlUegCgYIKoZIzj0DAQehRANCAARtK93efYXngv0u1TnAfCZ+4Z2HiQpyTPmCFwdGx6+6P8sdlqsJxvunM8rHPQTJmh0wD+rErywri4zGNX0olpl5'
    
    # header = json.loads(base64.b64decode(UserLogin.identityToken.split('.')[0]+"=="))
    # payload = json.loads(base64.b64decode(UserLogin.identityToken.split('.')[1]+"=="))
    # print(header)
    # print(payload)
    # print(UserLogin.authorizationCode)
    token_response = get_token_response(UserLogin.authorizationCode)
    # print(token_response)
    user = apple_login(db,token_response)
    if user:
        return token_response
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
import re
import pdfx
import json
@app.post("/pdf")
async def upload_pdf(refresh_token:str,user_id:str,file: UploadFile = File(...),db: Session = Depends(get_db)):
    contents = file.file.read()
    print(file.filename)
    token = refresh_token
    if(verify_refresh_token(db,user_id,refresh_token)):
        print("Verified refresh token")
        with open('files/'+file.filename,"wb") as f:
            f.write(contents)
        isArxiv = "arXivStAmP".encode("UTF-8") in contents
        # pdf = pdfx.PDFx('files/'+file.filename)
        # metadata = pdf.get_metadata()
        # full_text = pdf.get_text()
        # bookmark = schemas.Bookmark(
        #     type:"arxiv_paper",
        # 
        return {"isArXiv":isArxiv}

from data_access.bookmarks import create_user_bookmark,get_user_bookmarks,update_user_bookmark,delete_user_bookmark

@app.post("/bookmark")
async def add_bookmark(bookmarkRequest:schemas.BookmarkRequest,db: Session = Depends(get_db)):
    print("Got bookmark")
    print(bookmarkRequest)
    refresh_token = bookmarkRequest.refresh_token
    user_id = bookmarkRequest.user_id

    if(verify_refresh_token(db,user_id,refresh_token)):
        print("Verified refresh token")
        db_bm = create_user_bookmark(db,bookmarkRequest.bookmark,user_id)

        return db_bm
@app.put("/bookmark")
async def update_bookmark(bookmarkRequest:schemas.BookmarkRequest,db: Session = Depends(get_db)):
    print("Got bookmark")
    print(bookmarkRequest)
    refresh_token = bookmarkRequest.refresh_token
    user_id = bookmarkRequest.user_id

    if(verify_refresh_token(db,user_id,refresh_token)):
        print("Verified refresh token")
        db_bm = update_user_bookmark(db,bookmarkRequest.bookmark,user_id)

        return db_bm
@app.delete("/bookmark")
async def delete_bookmark(bookmarkRequest:schemas.BookmarkRequest,db: Session = Depends(get_db)):
    print("Got bookmark")
    print(bookmarkRequest)
    refresh_token = bookmarkRequest.refresh_token
    user_id = bookmarkRequest.user_id

    if(verify_refresh_token(db,user_id,refresh_token)):
        print("Verified refresh token")
        db_bm = delete_user_bookmark(db,bookmarkRequest.bookmark,user_id)
        
        # return db_bm
        
@app.get("/bookmarks")
async def get_bookmarks(refresh_token:str,user_id:str,db: Session = Depends(get_db)):
    if(verify_refresh_token(db,user_id,refresh_token)):
        print("Verified refresh token")
        bookmarks = get_user_bookmarks(db,user_id)
        return bookmarks


    # refresh_token = token['refresh_token']
    # id_token = token['id_token']
    # print(id_token)
    # header = json.loads(base64.b64decode(id_token.split('.')[0]+"=="))
    # payload = json.loads(base64.b64decode(id_token.split('.')[1]+"=="))
    # print(payload)


    



# @app.post("/pdf")
# async def upload_pdf(request:Request):
#     # contents = file.file.read()
#     # print(file.filename)
#     print(await request.form())


# @app.post("/test")
# async def playground(user:schemas.Dummy):
#     print(user.email)
#     # json = await request.json()
#     # print(json)
#     return {"message":user.email}

