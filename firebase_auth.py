import pyrebase
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

config = {
  'apiKey': "AIzaSyBnz6wws3EjTRnFOG7NvefKSr9CsaOlcxY",
  'authDomain': "flick-it-users-storage.firebaseapp.com",
  'projectId': "flick-it-users-storage",
  'storageBucket': "flick-it-users-storage.appspot.com",
  'messagingSenderId': "1046722019798",
  'appId': "1:1046722019798:web:905b021820e1922f95a477",
  'measurementId': "G-J3T9K8WPV2",
  'databaseURL':"",
  'serviceAccount': 'serviceAccountCredentials.json'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = FastAPI()

class User(BaseModel):
    username:str
    password:str
    mail:str

class UserLogin(BaseModel):
    login:str
    password:str

@app.post('/v1/register')
async def register(user:User):
    try:
        user = auth.create_user_with_email_and_password(user.mail,user.password)
        auth.send_email_verification(user['idToken'])
        return 200
    except:
        return 400

@app.post('/v1/login')
async def login(user:UserLogin):
    try:    
        user = auth.sign_in_with_email_and_password(user.login,user.password)
        user_info = auth.get_account_info(user['idToken'])
        if(user_info["users"][0]["emailVerified"] == True):
            return auth.create_custom_token(user['localId'])
        else:
            return 400
    except:
        return 400

@app.post('/v1/tokenLogin')
async def tokenLogin(token:str):
    try:
        auth.sign_in_with_custom_token(token)
        return 200
    except:
        return 400

@app.post('/v1/forgotpwd')
async def forgetpwd(mail:str):
    try:
        auth.send_password_reset_email(mail)
        return 200
    except:
        return 400