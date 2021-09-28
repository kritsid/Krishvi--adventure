from database import get_db
from flask import Flask,redirect,url_for,render_template,request,g,session
import pandas as pd
from typing import Any, Text, Dict, List
import os
from flask_mail import Mail,Message
from random import randint
import global_data_config
from pathlib import Path
from voiceit2 import VoiceIt2
import speech_recognition as s_r
# import pyaudio
# from deepspeech import Model
import scipy.io.wavfile as wav
import wave

app=Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)#for session

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()

mail=Mail(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='vipul27goel@gmail.com'
app.config['MAIL_PASSWORD']='!Hanumanji12'                    
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)

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

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method =='POST':
        global_data_config.inc = global_data_config.inc+1
        id =global_data_config.inc 
        
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        balance = request.form['balance']
        account_number = request.form['account_number']
        on_hold = request.form['on_hold']
        account_type = request.form['account_type']
        voice_id = str(id)
        cursor = get_db()
        cursor.execute('insert into voice_banking_users_db (id, first_name, last_name,email, gender, account_number, account_type, on_hold, balance,voice_id ) values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)',(id, first_name, last_name,email, gender, account_number, account_type, on_hold, balance ,voice_id))
        return render_template('voice_home.html')
        
        
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        downloads_path = str(Path.home() / "Downloads")
        identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", downloads_path+"\welcome.wav")
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
                # print(global_data_config.email)       
                # print(global_data_config.name)   
                # print("*************************")
                dict1 = {"user_email": global_data_config.email,
                        "user_name": global_data_config.name,
                        "user_balance": global_data_config.balance,
                        "account_number": global_data_config.account_number,
                        "account_type": global_data_config.account_type,
                        "account_hold": global_data_config.account_hold
                    }
                df = pd.DataFrame(dict1,index=[0])
                print(df)
                df.to_csv('G:\krishvi-xethon\Krishvi--adventure\output.csv',index=False)
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
        return render_template('chatroom.html',name =global_data_config.name )
    email=global_data_config.email
    global_data_config.count+=1
    msg=Message(subject='OTP',sender='vipul27goel@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    if global_data_config.count==2 :
        return "AUTHENTICATION FAILED"
    elif global_data_config.count<2 :
        return render_template('verify.html')


@app.route('/insert_data_from_csv_to_heroku_postgres_db',methods=['GET'])
def adding_db   ():    
    df=pd.read_csv('data.csv')
    
    cursor = get_db()
    #cursor.execute('insert into voice_banking_users_db(id, first_name, last_name,email, gender, account_number, account_type, on_hold, balance ) values (%s, %s,%s,%s,%s,%s,%s,%s,%s)',(str(df.iloc[i,0]),df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],str(df.iloc[i,5]),df.iloc[i,6],str(df.iloc[i,7]),str(df.iloc[i,8])))
    cursor.execute('select* from voice_banking_users_db')
    users=cursor.fetchall()
    print(users)
    return 'Database deployment (creation and insertion of data given to us) done....'

if __name__ == '__main__':
    app.run(debug=True)