from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException


def get_all_software(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Software).offset(skip).limit(limit).all()


def get_software_by_id(db: Session, software_id: int):
    return db.query(models.Software).filter(models.Software.id == software_id).first()


def get_software_by_software_and_version(db: Session, version: str, software: str):
    return db.query(models.Software).filter(models.Software.version == version,
                                            models.Software.software == software).first()


def update_software_by_id(db: Session, software_id: int, software: str, version: str):
    software_by_id = db.query(models.Software).filter(models.Software.id == software_id).first()
    # if software_by_id is None:
    #     raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
    software_by_id.version = version
    software_by_id.software = software
    db.commit()
    db.refresh(software_by_id)
    return software_by_id


def create_software(db: Session, software: schemas.SoftwareCreate):
    software = models.Software(software=software.software, version=software.version)
    db.add(software)
    db.commit()
    db.refresh(software)
    return software


def delete_item_by_id(db: Session, software_id: int):
    software_to_delete = db.query(models.Software).filter(models.Software.id == software_id).first()
    if software_to_delete is None:
        raise HTTPException(status_code=404, detail=f'Не найден id = {software_id}')
    db.delete(software_to_delete)
    db.commit()
    return software_to_delete
