from pydantic import BaseModel
from typing import Union,Optional
from pydantic import constr,EmailStr,conint


class IgRequest (BaseModel):
    username:constr(min_length=1)
    follower_count:conint()
    bio:Optional[constr(max_length=100)]= None

class IgResponse(BaseModel):
    id:int
    username:str
    follower_count:int
    bio:Optional[str]= None
    user_id:int
    class Config():
        orm_mode=True
