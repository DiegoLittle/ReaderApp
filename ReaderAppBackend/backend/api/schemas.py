from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str

class Note(BaseModel):
    id: str
    title:str
    description:str

class NoteRequest(BaseModel):
    title:str
    description:str

class Dummy(BaseModel):
    email:str
    name:str
    identifier:str


class AppleName(BaseModel):
    familyName:str
    givenName:str

class AppleUser(BaseModel):
    email:str
    name: AppleName
    identifier:str



class UserCreateApple(BaseModel):
    authorizationCode:str
    user: AppleUser
    identityToken: str

class UserLoginApple(BaseModel):
    user_id:str
    identityToken:str
    authorizationCode:str

class Bookmark(BaseModel):
    id:str
    url:str
    title:str
    type:str
    description:str

class BookmarkRequest(BaseModel):
    bookmark:Bookmark
    refresh_token:str
    user_id:str

{'authorizationCode': 'c1f99bbf185c646db8f41e08a75f6e5cb.0.srzwt.4cjHVXK4aocVVmMtyRRnZA', 'user': {'email': 'diegochelittle@gmail.com', 'name': {'familyName': 'Little', 'givenName': 'Diego'}, 'identifier': '001963.d41a902d40354369b1345979514a2e68.0710'}, 'identityToken': 'eyJraWQiOiJmaDZCczhDIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoic3luZXN0aGVzaWEuUmVhZGVyQXBwIiwiZXhwIjoxNjUxMzI5Mjk0LCJpYXQiOjE2NTEyNDI4OTQsInN1YiI6IjAwMTk2My5kNDFhOTAyZDQwMzU0MzY5YjEzNDU5Nzk1MTRhMmU2OC4wNzEwIiwiY19oYXNoIjoiak1CRWU5TXlPQXVQcGZnZU1ESEtkZyIsImVtYWlsIjoiZGllZ29jaGVsaXR0bGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiYXV0aF90aW1lIjoxNjUxMjQyODk0LCJub25jZV9zdXBwb3J0ZWQiOnRydWUsInJlYWxfdXNlcl9zdGF0dXMiOjJ9.DafLnhfD2vcyTAWh7BXQzaMeMror1P0rS0ru28brW-VB0M0Je7twl6L6Q79JtLacB2eLonhvY2CKN9Vl6REmkOSjfRLqs17sgGWICnNAxAB7unWiWPO4v4O8k6Xiac11wjYlzspqf20A0drgyQ5TkfIcGsGQnXjLp0bcg6aqbxAK_QzuLo_jjcEIzLxpRZMYj_-L2FMV2bVjyia9uyx1256LXOJzgiDuYtUR6j4cQta53oDiAoFV2wnlDrrNduaLihCAWXVGAz9qCsSTZ-Qga1d8ECTY2xtF6dSe59zbQDiA4dWt3vcyonTo21Z49-ajeOR8E7LwbEF1dXeNLFMTMQ'}