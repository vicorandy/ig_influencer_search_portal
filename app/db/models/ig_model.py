from  app.core.database  import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Instagrammer(Base):
    __tablename__='instagrammers'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    follower_count=Column(Integer)
    bio=Column(String)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id =Column(Integer, ForeignKey('users.id')) 