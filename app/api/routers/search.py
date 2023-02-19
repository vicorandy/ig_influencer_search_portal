from fastapi import APIRouter,Depends
from typing import Optional,List
from sqlalchemy.orm import Session
from app.db.models.ig_model import Instagrammer
from app.core.database import get_db
from app.api.schema.ig_schema import IgResponse



router =APIRouter(tags=['Endpoint'])

@router.get('/search',response_model=List[IgResponse],status_code=200)
def search(db:Session=Depends(get_db),username:Optional[str]=None,bio:Optional[str]=None,min_followers:Optional[int]=None,max_followers:Optional[int]=None):

    if bio==None and username==None and min_followers==None and min_followers==None:
        res = db.query(Instagrammer).order_by(Instagrammer.created_at).all()
        return res
  
    res=[]

    if username:
        query_username=db.query(Instagrammer).filter(Instagrammer.username==username).all()
        res.extend(query_username)

    if bio:
        query_bio = db.query(Instagrammer).filter(Instagrammer.bio.ilike('%{}%'.format(bio))).all()
        res.extend(query_bio)

    if max_followers:
        query_max_followers=db.query(Instagrammer).filter(Instagrammer.follower_count <= max_followers).all()
        res.extend(query_max_followers)

    if min_followers:
        query_min_followers=db.query(Instagrammer).filter(Instagrammer.follower_count >= min_followers).all()
        res.extend(query_min_followers)
    
    res_list=[]

    for data in res:
        if data not in res_list:
            res_list.append(data) 
    
    return res_list