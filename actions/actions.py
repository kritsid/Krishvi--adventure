from flask import Flask,redirect,url_for,render_template,request,g,session
import pandas as pd
from database import get_db
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pathlib import Path
import os
from flask import Flask,render_template,request
from flask_mail import Mail,Message
from random import randint

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


import sys
sys.path.insert(0,'G:\krishvi-xethon\Krishvi--adventure')
import global_data_config

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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType



class ActionWelcome(Action):
    def name(self) -> Text:
        return "action_welcome"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        slots = {
            "user_email": 'kag@123.com',
            "user_name": 'abc',
            "user_balance": 29020,
            "account_number": 7080904050,
            "account_type": 'Saving',
            "account_hold": False,
        }
        data = pd.read_csv('output.csv')
        # print(slots.items())
        # print('check slot values')
        # print(slots['user_email'])
        # print(slots['user_balance'])

        # print('global values')
        # print(global_data_config.email,global_data_config.balance,global_data_config.account_number,)
        dispatcher.utter_message(response = "utter_about_user")
        return [SlotSet(slot, value) for slot, value in slots.items()]      
        # return [SlotSet('user_email',data.iloc[0,0]), SlotSet("user_name",data.iloc[0,1]),SlotSet("user_balance",data.iloc[0,2]),SlotSet("account_number",data.iloc[0,3]), SlotSet("account_type",data.iloc[0,4]),SlotSet("account_hold",data.iloc[0,5])]

class ActionFinalTransferFunds(Action):
    def name(self) -> Text:
        return "action_final_transfer_funds"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        value = tracker.slots.get('approval')
        if value == 'yes':
            dispatcher.utter_message(response ="utter_transfer_done")
        else:
            dispatcher.utter_message(response ="utter_transfer_cancelled")

        return []


class ValidateTransferfundsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_transfer_funds_form"

    def validate_transfer_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print('in validation ', slot_value)
        if slot_value <= tracker.slots.get('user_balance'):
            return {"transfer_amount": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(response = "utter_insufficient_balance")

            return {"transfer_amount": None}

class ActionServices(Action):

    def name(self) -> Text:
        return "action_select_service"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ser = tracker.slots.get('service_name')
        print('in another class and action')
        print(global_data_config.email)       
        print(global_data_config.name) 
        print(global_data_config.account_type) 
        print(global_data_config.account_hold)             
  
        if ser.lower() == 'transfer funds':
            account_type = tracker.slots.get('account_type')
            account_hold = tracker.slots.get('account_hold')
            if account_hold == True:
                dispatcher.utter_message(response = "utter_account_on_hold")
                return []
            if account_type == 'fixed deposit' or account_type == 'recurring':
                dispatcher.utter_message(response = "utter_invalid_acccount_type")
                return []
            else:
                dispatcher.utter_message(response = "utter_ask_transfer_amount")
        else:
            # SlotSet('service_name', 'check balance')
            balance = tracker.slots.get('user_balance')
            dispatcher.utter_message(response = "utter_check_balance")
        return []



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
# global inc  = 105

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()


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

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method =='POST':
        global_data_config.inc = global_data_config.inc+1
        id =global_data_config.inc 
        # cursor = get_db()
        # cursor.execute('select * from voice_banking_users_db')
        # len1 = cursor.fetchall()
        # id = len(len1)+1
        id = 200
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
import pandas as pd
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        # groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
        downloads_path = str(Path.home() / "Downloads")
        identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", downloads_path+"\welcome.wav")
        # identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day", "pa7.mp4")
        print(identified_as)
        print(type(identified_as))
        if identified_as['responseCode'] != 'FAIL':
            x=identified_as['userId']
        # x = 'usr_f14c0b65d6cb459eba0b1b34e41504f5'
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


if __name__ == '__main__':
    app.run(debug=True)
