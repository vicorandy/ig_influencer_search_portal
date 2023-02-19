from  app.core.database  import Base
from sqlalchemy import Column,String,Integer,DateTime,func
from sqlalchemy.orm import relationship
from datetime import datetime,timedelta
from jose import JWTError,jwt
from app.api.schema.users_schema import TokenData
import os
from dotenv import load_dotenv
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv('ACCESS_TOKEN_EXPIRE_DAYS'))


class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String,unique=True)
    password=Column(String)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
    def create_access_token(self,data:dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(encoded_jwt)
        return encoded_jwt
    
  
    



