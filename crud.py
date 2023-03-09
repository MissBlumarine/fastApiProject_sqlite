from sqlalchemy.orm import Session
import models
import schemas

SOFTWARE: dict[int, models.Software] = {}


def list_software() -> list[schemas.Software]:
    return list(SOFTWARE.values())


def get_all_software(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Software).offset(skip).limit(limit).all()


def get_software_by_id(db: Session, software_id: int):
    return db.query(models.Software).filter(models.Software.id == software_id).first()


def get_software_by_software_and_version(db: Session, version: str, software: str):
    return db.query(models.Software).filter(models.Software.version == version,
                                            models.Software.software == software).first()


def create_software(db: Session, software: schemas.SoftwareCreate):
    # software_id = len(SOFTWARE) + 1
    software = models.Software(id=software.id, software=software.software, version=software.version)
    db.add(software)
    db.commit()
    db.refresh(software)
    return software
