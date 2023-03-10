from fastapi.testclient import TestClient
from app.app import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.database import get_db,Base
from app.db.models.ig_model import Instagrammer
import os
from dotenv import load_dotenv
load_dotenv()


database_url_test=os.getenv('database_url_test')

engine=create_engine(database_url_test)

TestingSessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False)



@pytest.fixture()
def session():
    TestingSessionLocal.close_all()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    except:
        db.close()



@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        except:
            session.close()
    app.dependency_overrides[get_db]=override_get_db           
    yield TestClient(app)
       

@pytest.fixture
def new_user(client):
    data={"username":"test_user","email":"test_user@gmail.com","password":"test_user_password"}
    res=client.post('/users/register',json=data)
    
    new_user= res.json()
    new_user['password']=data['password']
    
    return new_user

@pytest.fixture
def authorized_client(new_user,client):
    client.headers={
        **client.headers,
         "Authorization":f"Bearer {new_user['token']['access_token']}"
    }

    return client 

@pytest.fixture
def test_ig_acc(new_user,session):
    ig_acc_data=[
                {
                    'username':'vicorandy',
                    'bio':'i am a front-end developer',
                    'follower_count':100,
                    'user_id':new_user['id']
                },
                {
                    'username':'code_vic',
                    'bio':'i am a back-end developer',
                    'follower_count':1000,
                    'user_id':new_user['id']
                },
                {
                    'username':'victor',
                    'bio':'i am a fullstack developer',
                    'follower_count':10000,
                    'user_id':new_user['id']
                }
                   ]
    def create_entries_data(entry):
        return Instagrammer(**entry)

    ig_acc_map=map(create_entries_data,ig_acc_data)
    ig_acc=list(ig_acc_map)
    session.add_all(ig_acc)
    session.commit()
    data=session.query(Instagrammer).filter(Instagrammer.user_id==new_user['id']).all()
    return data

