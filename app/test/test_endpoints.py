import pytest
from app.api.schema.users_schema import UserResponse ,Token
from app.api.schema.ig_schema import IgResponse
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")


def test_login_user(new_user,client):
    user=new_user
    res=client.post('/users/login',data={"username":user['email'],"password":user['password']})
    token=Token(**res.json())
    payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id=payload.get('user_id')
    assert id == user['id']
    assert res.status_code == 200
    
def test_incorrect_login(new_user,client):
  
   res = client.post('/users/login',data={"username":"test_user@gmail.com","password":"wrong_password"})
   assert res.status_code ==401
   assert res.json()['detail'] == 'Invalid Credentials'

def test_no_user_login(client):
   res = client.post('/users/login',data={"username":"test_user@gmail.com","password":"wrong_password"})
   assert res.status_code ==404
   assert res.json()['detail'] == 'user with the email :test_user@gmail.com was not found'
   
 

def test_create_user(client):
    res=client.post('/users/register',json={"username":"test","email":"test@gmail.com","password":"testpassword"})
    new_user =UserResponse(**res.json())
    assert new_user.email=='test@gmail.com'
    assert new_user.username=='test'


def test_create_user_already_exist(new_user,client):
    res=client.post('/users/register',json={"username":"test_user","email":"test_user@gmail.com","password":"test_user_password"})
    assert res.status_code == 400
    assert res.json()['detail']=='A user account with the email :test_user@gmail.com already exist'

def test_create_ig_acc(authorized_client):
    res=authorized_client.post('/add_ig_acc',json={'username':'vicorandy','follower_count':10000,'bio':'i am a software developer','user_id':1})
    data= IgResponse(**res.json())
    assert res.status_code == 201
    assert data.username == 'vicorandy'
    assert data.bio == 'i am a software developer'
    assert data.follower_count== 10000
    assert data.user_id == 1

def test_search(test_ig_acc,client):
    res=client.get('/search')
    print(res.json())
    assert res.status_code ==200
    assert len(res.json())==3
    



def test_search_with_query(test_ig_acc,client):
    res=client.get('/search?username=victor&bio=fullstack&max_follower=1&min_followers=10000')

    data=res.json()[0]
    assert res.status_code == 200
    assert data['id']==3
    assert data['username'] == 'victor'
    assert data['follower_count']==10000
    assert data['bio']=='i am a fullstack developer'
    assert data['user_id']==1
