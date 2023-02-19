from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.api.schema.ig_schema import IgRequest,IgResponse
from app.api.dependency import get_current_user
from app.core.database import get_db
from app.db.models.ig_model import Instagrammer

router=APIRouter(tags=['Endpoint'])

@router.post('/add_ig_acc',status_code=201,response_model=IgResponse)
def adding_instagram_account(request:IgRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    id=current_user.user_id
    data=Instagrammer(user_id=id,username=request.username,bio=request.bio,follower_count=request.follower_count)

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
