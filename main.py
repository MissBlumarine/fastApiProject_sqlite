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


@app.get("/versions")
async def get_all_software(db: Session = Depends(get_db)):
    return db.query(Software).all()


@app.get("/versions/{id}")
async def get_software_by_id(id, db: Session = Depends(get_db)):
    software = db.query(Software).filter(Software.id == id).first()
    if software == None:
        return JSONResponse(status_code=404, content={'внимание': f'Software_продукта c id={id} не существует'})
    return software



@app.post("/version")
async def create_software(data= Body(), db: Session = Depends(get_db)):
    product = Software(software=data["software"], version=data["version"])
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
#
#
# @app.patch("/users/patch")
# async def patch_software(data = Body(), db: Session = Depends(get_db)):
#     product = db.query(Software).filter(Software.id == data["id"]).first()
#     if product == None:
#         return JSONResponse(status_code=404, content={'внимание': f'Software_продукта c id={id} не существует'})
#     product.software = data["software"]
#     product.version = data["version"]
#     db.commit()
#     db.refresh(product)
#     return product


# @app.get("/version")
# async def create_software(name: str):
#     return {"message": f"Hello {name}"}
