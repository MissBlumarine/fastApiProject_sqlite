from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

import models
from database import *
import crud
import schemas


# создаем таблицу
Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/version", response_model=schemas.Software)
def create_software(software: schemas.SoftwareCreate, db: Session = Depends(get_db)):
    software_new = crud.get_software_by_software_and_version(db, version=software.version, software=software.software)
    if software_new:
        raise HTTPException(status_code=400, detail="Уже существует")
    return crud.create_software(db=db, software=software)


@app.get("/versions", response_model=List[schemas.Software])
def get_all_software(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    softwares = crud.get_all_software(db, skip=skip, limit=limit)
    return softwares


@app.get("/versions/{id}", response_model=schemas.Software)
def get_software_by_id(software_id: int, db: Session = Depends(get_db)):
    software_ex = crud.get_software_by_id(db, software_id=software_id)
    if software_ex is None:
        raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
    return software_ex


@app.put("/version/{id}", response_model=schemas.Software)
def update_software_by_id(software_id: int, software: str, version: str, db: Session = Depends(get_db)):
    software_new = crud.update_software_by_id(db, software_id=software_id, software=software, version=version)
    return software_new


# @app.put("/version/{id}", response_model=schemas.Software)
# def update_software_by_id(software_id: int, software: str, version: str, db: Session = Depends(get_db)):
#     software_new = db.query(models.Software).filter(models.Software.id == software_id).first()
#     if software_new is None:
#         raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
#     software_new.version = version
#     software_new.software = software
#     db.commit()
#     db.refresh(software_new)
#     return software_new


# @app.delete("/version/{id}")
# def delete_item_by_id(software_id: int, db: Session = Depends(get_db)):
#     software_to_delete = db.query(models.Software).filter(models.Software.id == software_id).first()
#     if software_to_delete is None:
#         raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
#     db.delete(software_to_delete)
#     db.commit()
#     return software_to_delete


@app.delete("/version/{id}")
def delete_item_by_id(software_id: int, db: Session = Depends(get_db)):
    software_to_delete = crud.delete_item_by_id(db, software_id=software_id)
    if software_to_delete is None:
        raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
    return software_to_delete
