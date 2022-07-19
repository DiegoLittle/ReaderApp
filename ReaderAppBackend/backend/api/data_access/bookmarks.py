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


def create_user_bookmark(db: Session, bookmark: schemas.Bookmark, user_id: str):
    db_item = models.Bookmark(**bookmark.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def update_user_bookmark(db:Session,bookmark: schemas.Bookmark, user_id:str):
    # db_item = models.Bookmark(**bookmark.dict(),owner_id=user_id)
    db_bookmark = db.query(models.Bookmark).filter(models.Bookmark.id == bookmark.id).first()
    for key, value in bookmark.dict().items():
        setattr(db_bookmark,key,value)

    # db.add(db_item)
    db.commit()

def delete_user_bookmark(db:Session,bookmark: schemas.Bookmark, user_id):
    db_bookmark = db.query(models.Bookmark).filter(models.Bookmark.id == bookmark.id.lower()).delete()
    db.commit()

def get_user_bookmarks(db:Session, user_id:str):
    bookmarks = db.query(models.Bookmark).filter(models.Bookmark.owner_id == user_id)
    bookmarks = [x.__dict__ for x in bookmarks.all()]
    return bookmarks
