from flask import Flask,redirect,url_for,render_template,request,g,session
# import pandas as pd
from database import get_db

from voiceit2 import VoiceIt2
import speech_recognition as s_r
# import pyaudio
# from deepspeech import Model
import scipy.io.wavfile as wav
import wave
import os
from flask_mail import Mail,Message
from random import randint

app=Flask(__name__)


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
        return render_template('voice_home.html')
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        # groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", "pa7.mp4")
        print(identified_as)
        print(type(identified_as))
        if bool(identified_as):
            x=identified_as['userId']
            cursor = get_db()
            cursor.execute('select * from voice_banking_users_db where voice_id = %s',(x,))
            taken = cursor.fetchone()
            if len(taken)>=1:
                email = taken['email']
                user_id = taken['id']
                name = taken['first_name'] +' '+ taken['last_name']
                account_number = taken['account_number']

                session['user']= taken['email']
                return render_template('chatroom.html')
            return render_template('voice_home.html')
        else:
            print("AUTHENTICATION FAILEd")
            return "AUTHENTICATION FAILEd"
    return render_template('voice_home.html')

if __name__ == '__main__':
    app.run(port = 5055, debug=True)