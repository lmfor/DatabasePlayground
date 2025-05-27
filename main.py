from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, Body
# from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import City
from typing import List
# import database


# Ensure tables exist on startup
# Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# yield a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
'''


@app.get("/")
def read_root():
    return {"ROOT" : "PAGE"}

@app.get("/cities")
def get_cities(db : Session = Depends(get_db)):
    return db.query(City).all() 

@app.post("/cities")
#            Body just means dont look at /cities?name=&country= in the URL. It will look at the body of the POST request
#                                  BODY --> raw --> JSON
def create_city(name: str=Body(...), country: str=Body(...), db: Session = Depends(get_db)):
    city = City(name=name,country=country)
    db.add(city)
    db.commit() # city ID is still non-existent at this point
    db.refresh(city) # refresh() will update the city object with the ID assigned by the database
    return city

# note that when using PUT, the entire object is replaced and thus gets moved to the lowest row. It retains its ID number though.
@app.put("/cities/{city_id}")
def replace_city(city_id: int, name: str = Body(...), country: str = Body(...), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail=f"({city_id}) City not found")
    city.name = name        #type: ignore
    city.country = country  #type: ignore
    db.commit()
    db.refresh(city)
    return city

@app.patch("/cities/{city_id}")
def update_city(city_id: int, name: str = Body(None), country: str = Body(None), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail=f"({city_id}) City not found")
    if name is not None:
        city.name = name       #type: ignore
    if country is not None:
        city.country = country #type: ignore
    db.commit()
    db.refresh(city)
    return city

'''
Example of a patch request body (JSON):
URL: http://localhost:8000/cities/5
{
    "name":"Calgary",
    "country": null
}
'''


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = db.query(City).filter(City.id == city_id).first()
    if not deleted_city:
        raise HTTPException(status_code=404, detail=f"({deleted_city}) City not found")
    db.delete(deleted_city)
    db.commit()
    return deleted_city