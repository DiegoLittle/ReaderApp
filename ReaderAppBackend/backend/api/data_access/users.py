from sqlalchemy.orm import Session
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional, OrderedDict
import json
from database import SessionLocal, engine
import jwt
import models, schemas
import uuid
import time


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def apple_login(db:Session,token_response):
    id_token = token_response.get('id_token', None)
    if id_token:
            decoded = jwt.decode(id_token, '', verify=False)
            email = decoded['email']
            user_id = decoded['sub']
    print(token_response)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
        return True
    else:
        False
    return

def create_apple_user(db: Session, userRequest: schemas.UserCreateApple):
    user = userRequest.user
    db_account = models.Account(
        id = str(uuid.uuid4()),
        userId=user.identifier,
        type = "oauth",
        provider= "apple",
        providerAccountId = user.identifier,
        expires_at = int(time.time() + 86400*180),
        token_type = "Bearer",
        scope=None,
        id_token = userRequest.identityToken,
        session_state=None,
    )
    db_user = models.User(
        id=user.identifier,
        email=user.email,
        given_name=user.name.givenName,
        family_name=user.name.familyName
        )
    db.add(db_account)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_refresh_token(db:Session, user_id:str,refresh_token:str):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user.refresh_token == refresh_token:
        return True
    
