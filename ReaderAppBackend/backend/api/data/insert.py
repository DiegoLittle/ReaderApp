from sqlalchemy.orm import Session
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional, OrderedDict
import json
# from database import SessionLocal, engine
# import jwt
# import models, schemas
import sys
sys.path.append('../')

# import models,schemas
from database import SessionLocal,engine

res = engine.execute("SELECT * FROM entities INNER JOIN methods ON entities.id = methods.id;").fetchone()
print(res.id)


# db_item = models.Bookmark(**bookmark.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)

