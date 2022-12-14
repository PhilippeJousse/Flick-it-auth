import pyrebase,json
from fastapi import FastAPI
from pydantic import BaseModel

firebaseConfig = json.load(open("firebaseConfig.json"))

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

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
        userCreation = auth.create_user_with_email_and_password(user.mail,user.password)
        auth.send_email_verification(userCreation['idToken'])
        db.child("users").child(user.username).set({"username":user.username,"mail":user.mail,"totalPoint":0})
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