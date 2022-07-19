from re import S
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime,ARRAY
from sqlalchemy.orm import relationship
import hashlib
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "User"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    refresh_token = Column(String)
    email = Column(String, unique=True, index=True)
    emailVerified = Column(DateTime)
    image = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    bookmarks = relationship("Bookmark",back_populates="owner")
    accounts = relationship("Account",back_populates="user")
    sessions = relationship("Session",back_populates="user")
class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(String, primary_key=True,index=True,default=generate_uuid)
    url = Column(String)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    owner_id = Column(String, ForeignKey('User.id'))
    owner = relationship("User", back_populates="bookmarks")

class Account(Base):
    __tablename__ = "Account"
    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    provider = Column(String)
    providerAccountId = Column(String)
    refresh_token = Column(String)
    access_token = Column(String)
    expires_at = Column(Integer)
    token_type = Column(String)
    scope = Column(String)
    id_token = Column(String)
    session_state = Column(String)
    userId = Column(String, ForeignKey('User.id'))
    user = relationship("User", back_populates="accounts")

class Session(Base):
    __tablename__ = "Session"
    id = Column(String, primary_key=True)
    sessionToken = Column(String)
    userId = Column(String, ForeignKey('User.id'))
    expires = Column(DateTime)
    user = relationship("User",back_populates="sessions")


class Paper(Base):
    __tablename__ = "papers"
    id = Column(String, primary_key=True)
    arxiv_id = Column(String)
    title = Column(String)
    categories = Column(String)
    abstract = Column(String)
    url_abs = Column(String)
    url_pdf = Column(String)
    proceeding = Column(String)
    authors = Column(String)
    num_citations = Column(Integer)
    num_references = Column(Integer)
    num_influential_citations = Column(Integer)
    tasks = Column(String)
    date = Column(String)
    methods = Column(String)
    doi = Column(String)
    grobid = Column(String)
    refs = Column(String)
    keywords = Column(String)
    full_text = Column(String)
    s2_paper = Column(String)
    s2_citations = Column(String)
    code = Column(String)
    entity_links = Column(ARRAY(String))


class Entity(Base):
    __tablename__ = "entities"
    id = Column(String, primary_key=True,index=True,default=generate_uuid)
    name = Column(String,unique=True)
    full_name = Column(String)
    description = Column(String)
    entity_type = Column(String)
    synonyms = Column(String)
    url = Column(String)
    appearsin = Column(ARRAY(String))
    __mapper_args__ = {'polymorphic_on': entity_type}

class Dataset(Entity):
    __tablename__ = "datasets"
    __mapper_args__ = {'polymorphic_identity': 'dataset'}
    id = Column(ForeignKey('entities.id',ondelete="CASCADE"), primary_key=True)
    # name = Column(String)

    homepage = Column(String)
    paper = Column(String)
    introduced_date = Column(DateTime)
    modalities = Column(String)
    tasks = Column(ARRAY(String))
    languages = Column(ARRAY(String))
    variants = Column(ARRAY(String))
    num_papers = Column(Integer)
    data_loaders = Column(ARRAY(String))

class Task(Entity):
    __tablename__ = "tasks"
    __mapper_args__ = {'polymorphic_identity': 'task'}
    id = Column(ForeignKey('entities.id',ondelete="CASCADE"), primary_key=True)
    datasets = Column(ARRAY(String))
    # description = Column(String)
# class Building(Base):
#     __tablename__ = 'building'
#     id = Column(Integer, primary_key=True)
#     building_type = Column(String(32), nullable=False)
#     x = Column(Float, nullable=False)
#     y = Column(Float, nullable=False)
#     __mapper_args__ = {'polymorphic_on': building_type}

# class Commercial(Building):
#     __mapper_args__ = {'polymorphic_identity': 'commercial'}
#     business = Column(String(50))

# class Residential(Building):
#     __mapper_args__ = {'polymorphic_identity': 'residential'}
#     num_residents = Column(Integer)


    # papers = relationship("Paper",back_populates="dataset")

class Method(Entity):
    __tablename__ = "methods"
    id = Column(ForeignKey('entities.id',ondelete="CASCADE"), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'method'}
    paper = Column(String)
    introduced_date = Column(DateTime)
    source_url = Column(String)
    source_title = Column(String)
    code_snippet_url = Column(String)
    num_papers = Column(Integer)
    collections = Column(ARRAY(String))
    papers_mentioned = Column(ARRAY(String))




#     accounts      Account[]
#   sessions      Session[]

#   @@index([id], map: "ix_User_id")
# }

# model Account {
#   id                 String  @id @default(cuid())
#   userId             String
#   type               String
#   provider           String
#   providerAccountId  String
#   refresh_token      String?  @db.Text
#   access_token       String?  @db.Text
#   expires_at         Int?
#   token_type         String?
#   scope              String?
#   id_token           String?  @db.Text
#   session_state      String?

#   user User @relation(fields: [userId], references: [id], onDelete: Cascade)

#   @@unique([provider, providerAccountId])
# }



# model VerificationToken {
#   identifier String
#   token      String   @unique
#   expires    DateTime

#   @@unique([identifier, token])
# } 
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     salt= Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item",back_populates="owner")
#     notes = relationship("Note",back_populates="owner")
    


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

# class Note(Base):
#     __tablename__ = "notes"

#     id = Column(String, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="notes")