from fastapi import FastAPI, Depends, Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, FileResponse
from database import *


# создаем таблицу
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/versions")
async def get_all_software(db: Session = Depends(get_db)):
    return db.query(Software).all()

@app.get("/versions/{id}")
async def get_software_by_id(id, db: Session = Depends(get_db)):
    software = db.query(Software).filter(Software.id == id).first()
    if software == None:
        return JSONResponse(status_code=404, content={'внимание': 'Такого продукта нет'})
    return software


# @app.post("/version")
# def create_software(data=Body(), db: Session = Depends(get_db)):
#     software = Software(software=data['software'], version=data['version'])
#     db.add(software)
#     db.commit()
#     db.refresh(software)
#     return software




# @app.get("/version")
# async def create_software(name: str):
#     return {"message": f"Hello {name}"}
