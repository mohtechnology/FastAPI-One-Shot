from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "sqlite:///./contacts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Contact Model (SQLAlchemy)
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# CORS Middleware (Allow React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Contact Model (for request/response validation)
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str

class ContactResponse(ContactCreate):
    id: int

    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/contacts/", response_model=list[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(name=contact.name, email=contact.email, phone=contact.phone)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db_contact.name = contact.name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    
    db.commit()
    db.refresh(db_contact)
    
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact 
