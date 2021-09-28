from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType
from rasa_sdk.events import AllSlotsReset
from database import get_db
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pandas as pd
from flask import Flask,redirect,url_for,render_template,request,g,session

from flask import g
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
import os
app=Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)#for session

@app.teardown_appcontext
class ActionHelloWorld(Action):

     def name(self) -> Text:
            return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(response = "greet")

         return [AllSlotsReset()]
data = pd.read_csv('output.csv')

class ActionWelcome(Action):
    def name(self) -> Text:
        return "action_welcome"
    
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        slots = {
            "user_email": str(data.iloc[0,0]),
            "user_name": str(data.iloc[0,1]),
            "user_balance": str(data.iloc[0,2]),
            "account_number": str(data.iloc[0,3]),
            "account_type": str(data.iloc[0,4]),
            "account_hold": str(data.iloc[0,5])
        }
        
        print(data.iloc[0,0],data.iloc[0,1],data.iloc[0,2],data.iloc[0,3])
        dispatcher.utter_message(response = "utter_about_user")
        return [SlotSet(slot, value) for slot, value in slots.items()]      
        # return [SlotSet('user_email',data.iloc[0,0]), SlotSet("user_name",data.iloc[0,1]),SlotSet("user_balance",data.iloc[0,2]),SlotSet("account_number",data.iloc[0,3]), SlotSet("account_type",data.iloc[0,4]),SlotSet("account_hold",data.iloc[0,5])]

class ActionFinalTransferFunds(Action):
    def name(self) -> Text:
        return "action_final_transfer_funds"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        transfer_amount = tracker.slots.get('transfer_amount')
        receiver_account_number = str(tracker.slots.get('receiver_account_number'))
        print('receiver_account_number is ', receiver_account_number)
        value = tracker.slots.get('approval')
        print(value)
        if value == 'yes' or value== 'YES' or value =='Yes' or value == 'yEs' or value =='yup' or value == 'yeah' or value == 'yes please' or value == 'yes transfer' :
            # cursor = get_db()
            conn = psycopg2.connect('postgres://qahsnefkaipjxg:325b65d33021cb764a558159aaccb79974554c1e5a70d154a4a2ea44218908f3@ec2-34-233-187-36.compute-1.amazonaws.com:5432/dfjoleem3udeag', cursor_factory=DictCursor)
            conn.autocommit = True    
            cursor = conn.cursor()    
            cursor.execute('select * from voice_banking_users_db where account_number = %s',(receiver_account_number, ) )
            result = cursor.fetchone()

            if float(transfer_amount) > float(tracker.slots.get('user_balance')):
                dispatcher.utter_message(response ="utter_insufficient_balance")
            user_balance = tracker.slots.get('user_balance')
            if result == None:
                print('data not fetched from DB')
                dispatcher.utter_message(response ="utter_transfer_cancelled")
                return []
            if len(result)>=1:
                user_balance = float(user_balance) - float(transfer_amount)
                temp = float(result['balance'])+float(transfer_amount)
                cursor.execute('update voice_banking_users_db set balance = %s where account_number = %s',(user_balance, tracker.slots.get('account_number'),))
                cursor.execute('update voice_banking_users_db set balance = %s where account_number = %s',(temp, receiver_account_number, ))
                dispatcher.utter_message(response ="utter_transfer_done")
                return [SlotSet('user_balance',user_balance),SlotSet('transfer_amount',None),SlotSet('receiver_account_number',None)]
            else:
                print('data not fetched from DB')

                dispatcher.utter_message(response ="utter_transfer_cancelled")
                

        else:
            dispatcher.utter_message(response ="utter_transfer_cancelled")
            return [SlotSet('user_balance',user_balance),SlotSet('transfer_amount',None),SlotSet('receiver_account_number',None)]

        return [SlotSet('transfer_amount',None),SlotSet('receiver_account_number',None)]

class ActionServices(Action):
    def name(self) -> Text:
        return "action_select_service"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ser = tracker.slots.get('service_name')
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












