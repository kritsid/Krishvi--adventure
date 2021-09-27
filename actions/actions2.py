from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import global_data_config

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
        if ser.lower() == 'transfer funds':
            dispatcher.utter_message(response = "utter_transfer_funds")
        else:
            dispatcher.utter_message(response = "utter_check_balance")

        return []
