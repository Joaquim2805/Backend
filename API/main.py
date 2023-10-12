from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import  Annotated
import random
import uvicorn
import model
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


model.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    id : str
    password :str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]    



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines autorisées ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.post("/testbdd")
async def create_user(user : UserBase, db : db_dependency):
    db_user = model.User(id = user.id, password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    

@app.get("/item")
def get_user(id: str = Query(..., description="ID de l'utilisateur"),
                   password: str = Query(..., description="Mot de passe de l'utilisateur"),
                   db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id, model.User.password == password).first()
    if user is None:
        return {"access_token": 0}
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
 





def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None



@app.get("/protected-route")
async def protected_route(current_user: str = Depends(oauth2_scheme)):
    return {"message": "This route is protected and only accessible with a valid token."}
