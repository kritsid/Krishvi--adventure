from flask import Flask,redirect,url_for,render_template,request,g,session
# import pandas as pd
from database import get_db
from pathlib import Path
import global_data_config
import os
from flask import Flask,render_template,request
from flask_mail import Mail,Message
from random import randint

app=Flask(__name__)
mail=Mail(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='vipul27goel@gmail.com'
app.config['MAIL_PASSWORD']='!Hanumanji12'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)




from voiceit2 import VoiceIt2
import speech_recognition as s_r
# import pyaudio
# from deepspeech import Model
import scipy.io.wavfile as wav
import wave
import os
# from flask_mail import Mail,Message
from random import randint

app=Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)#for session


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()

def get_current_user():
    pass
def set_user_data():
    pass
# my_voiceit = VoiceIt2('key_2a3d1f042f234bc089208f1bad26e64b','tok_a10c3c9017b84cb7bb53b49f7bd64859')
my_voiceit = VoiceIt2('key_56c24a5f4d4e41268ad35e3cc73eaca0','tok_132c2d00a38449179502fc4ed5a84f55')
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        downloads_path = str(Path.home() / "Downloads")
        if os.path.exists(downloads_path+"\welcome.wav"):
            print(downloads_path+"\welcome.wav")
            os.remove(downloads_path+"\welcome.wav")
        print(downloads_path+"\welcome.wav")
        return render_template('voice_home.html')
    downloads_path = str(Path.home() / "Downloads")
    if os.path.exists(downloads_path+"\welcome.wav"):
        print(downloads_path+"\welcome.wav")
        os.remove(downloads_path+"\welcome.wav")
    print(downloads_path+"\welcome.wav")
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        # groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        downloads_path = str(Path.home() / "Downloads")
        # identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", downloads_path+"\welcome.wav")
        identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", "pa7.mp4")
        print(identified_as)
        print(type(identified_as))
        if identified_as['responseCode'] != 'FAIL':
            x=identified_as['userId']
            cursor = get_db()
            cursor.execute('select * from voice_banking_users_db where voice_id = %s',(x,))
            taken = cursor.fetchone()
            if len(taken)>=1:
                global_data_config.email = taken['email']
                global_data_config.user_id = taken['id']
                global_data_config.name = taken['first_name'] +' '+ taken['last_name']
                global_data_config.account_number = taken['account_number']
                global_data_config.balance = taken['balance']
                global_data_config.account_type = taken['account_type']
                global_data_config.account_hold = taken['on_hold']
                print(global_data_config.email)       
                print(global_data_config.name)   
                print("*************************")
                email=global_data_config.email
                msg=Message(subject='OTP',sender='vipul27goel@gmail.com',recipients=[email])
                msg.body=str(otp)
                mail.send(msg)
                return render_template('verify.html')
                
            return render_template('voice_home.html')
        else:
            print("AUTHENTICATION FAILED")
            return "AUTHENTICATION FAILED"
    return render_template('voice_home.html')





@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        session['user']= global_data_config.email
        return render_template('chatroom.html')
    email=global_data_config.email
    global_data_config.count+=1
    msg=Message(subject='OTP',sender='vipul27goel@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    if global_data_config.count==2 :
        return "AUTHENTICATION FAILED"
    elif global_data_config.count<2 :
        return render_template('verify.html')


if __name__ == '__main__':
    app.run(port = 5055, debug=True)