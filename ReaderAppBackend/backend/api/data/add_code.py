import json
from database import SessionLocal, engine
import jwt
import models, schemas

db_bookmark = db.query(models.Bookmark).filter(models.Bookmark.id == bookmark.id).first()
for key, value in bookmark.dict().items():
    setattr(db_bookmark,key,value)