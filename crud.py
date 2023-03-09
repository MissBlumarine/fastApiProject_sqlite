from sqlalchemy.orm import Session
import models
import schemas


def get_all_software(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Software).offset(skip).limit(limit).all()


def get_software_by_id(db: Session, id: int):
    return db.query(models.Software).filter(models.Software.id == id).first()


def create_software(db: Session, software: schemas.SoftwareCreate):
    software = models.Software(software=software.software, version=software.version)
    db.add(software)
    db.commit()
    db.refresh(software)
    return software
