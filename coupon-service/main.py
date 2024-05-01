import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

import database as sess
import pymodels as pym
import sqlmodels as sqlm

app = FastAPI()

templates = Jinja2Templates(directory='/views/templates')

# CORS 설정
origins = [
    "http://localhost:3000",  # 허용할 프론트엔드 도메인
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 데이터베이스 세션 의존생 생성
def get_db():
    db = sess.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Hello World"}


# 조회
@app.get("/coupons", response_model=list[pym.Coupon])
async def list_coupons(db: Session = Depends(get_db)):
    coupons = db.query(sqlm.Coupon).all()
    return [pym.Coupon.from_orm(p) for p in coupons]


# 입력
@app.post("/coupons", response_model=pym.Coupon)
async def create_coupons(coupon: pym.CouponCreate, db: Session = Depends(get_db)):
    coupon = sqlm.Coupon(**coupon.model_dump())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return pym.Coupon.from_orm(coupon)


# 조회
@app.get("/coupons/{skey}", response_model=list[pym.Coupon])
async def find_coupons(skey: str, db: Session = Depends(get_db)):
    coupons = db.query(sqlm.Coupon).filter(func.lower(sqlm.Coupon.disc_time).like('%' + skey + '%'))
    return [pym.Coupon.from_orm(p) for p in coupons]


if __name__ == '__main__':
    sess.create_tables()
    uvicorn.run('main:app', port=8040, reload=True)