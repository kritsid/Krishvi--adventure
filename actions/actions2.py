from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import global_data_config
from rasa_sdk.events import SlotSet

class ActionWelcome(Action):
    def name(self) -> Text:
        return "action_welcome"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        SlotSet("user_email", global_data_config.email)
        SlotSet('user_name', global_data_config.name)
        SlotSet('user_balance',global_data_config.balance)
        SlotSet('account_number',global_data_config.account_number)
        SlotSet('account_type', global_data_config.account_type)
        SlotSet('account_hold',global_data_config.account_hold)
        dispatcher.utter_message(response = "utter_about_user")        
        return []

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionServices(Action):

    def name(self) -> Text:
        return "action_select_service"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ser = tracker.slots.get('service_name')
        print(global_data_config.email)       
        print(global_data_config.name)      
        # SlotSet("user_email", global_data_config.email)
        # SlotSet('user_name', global_data_config.name)
        # SlotSet('user_balance',global_data_config.balance)
        # SlotSet('account_number',global_data_config.account_number)
        # SlotSet('account_type', global_data_config.account_type)
        # SlotSet('account_hold',global_data_config.account_hold)
  
        if ser.lower() == 'transfer funds':
            account_type = tracker.slots.get('account_type')
            account_hold = tracker.slots.get('account_hold')
            if account_hold == True:
                dispatcher.utter_message(response = "utter_account_on_hold")
            if account_type == 'fixed deposit' or account_type == 'recurring':
                dispatcher.utter_message(response = "utter_invalid_acccount_type")
            else:
                dispatcher.utter_message(response = "utter_transfer_funds")
        else:
            # SlotSet('service_name', 'check balance')
            balance = tracker.slots.get('user_balance')
            dispatcher.utter_message(response = "utter_check_balance")
        return []
