



# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet,EventType

# from rasa_sdk.events import AllSlotsReset

# class ActionHelloWorld(Action):

#      def name(self) -> Text:
#             return "action_hello_world"

#      def run(self, dispatcher: CollectingDispatcher,
#              tracker: Tracker,
#              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#          dispatcher.utter_message("Hello World!")

#          return [AllSlotsReset()]

# class ActionWelcome(Action):
#     def name(self) -> Text:
#         return "action_welcome"
#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         slots = {
#             "user_email": 'kag@123.com',
#             "user_name": 'abc',
#             "user_balance": 500000,
#             "account_number": 74607266160,
#             "account_type": 'Saving',
#             "account_hold": False,
#         }
#         data = pd.read_csv('output.csv')
#         # print(slots.items())
#         # print('check slot values')
#         # print(slots['user_email'])
#         # print(slots['user_balance'])

#         # print('global values')
#         # print(global_data_config.email,global_data_config.balance,global_data_config.account_number,)
#         dispatcher.utter_message(response = "utter_about_user")
#         return [SlotSet(slot, value) for slot, value in slots.items()]      
#         # return [SlotSet('user_email',data.iloc[0,0]), SlotSet("user_name",data.iloc[0,1]),SlotSet("user_balance",data.iloc[0,2]),SlotSet("account_number",data.iloc[0,3]), SlotSet("account_type",data.iloc[0,4]),SlotSet("account_hold",data.iloc[0,5])]

# class ActionFinalTransferFunds(Action):
#     def name(self) -> Text:
#         return "action_final_transfer_funds"
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
#     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         transfer_amount = tracker.slots.get('transfer_amount')
#         receiver_account_number = tracker.slots.get('receiver_account_number')
#         value = tracker.slots.get('approval')
#         if value == 'yes':
#             cursor = get_db()
#             cursor.execute('select * from voice_banking_users_db where account_number = %s',(receiver_account_number, ) )
#             result = cursor.fetchone()
#             if len(result)>=1:
#                 user_balance = tracker.slots.get('user_balance')
#                 user_balance = user_balance - transfer_amount
#                 temp = result['balance']+transfer_amount
#                 cursor.execute('update voice_banking_users_db set balance = %s where account_number = %s',(user_balance, tracker.slots.get('account_number'),))
#                 cursor.execute('update voice_banking_users_db set balance = %s where account_number = %s',(temp, receiver_account_number, ))
#                 dispatcher.utter_message(response ="utter_transfer_done")
#             else:
#                 dispatcher.utter_message(response ="utter_transfer_cancelled")

#         else:
#             dispatcher.utter_message(response ="utter_transfer_cancelled")

#         return [SlotSet('transfer_amount',0.0),SlotSet('receiver_account_number',None),SlotSet('user_balance',user_balance)]


# # class ValidateTransferfundsForm(FormValidationAction):
# #     def name(self) -> Text:
#         # return "validate_transfer_funds_form"

#     # def validate_transfer_amount(
#     #     self,
#     #     slot_value: Any,
#     #     dispatcher: CollectingDispatcher,
#     #     tracker: Tracker,
#     #     domain: DomainDict,
#     # ) -> Dict[Text, Any]:
#     #     print('in validation ', slot_value)
#     #     if slot_value <= tracker.slots.get('user_balance'):
#     #         return {"transfer_amount": slot_value}
#     #     else:
#     #         # validation failed, set this slot to None so that the
#     #         # user will be asked for the slot again
#     #         dispatcher.utter_message(response = "utter_insufficient_balance")

#     #         return {"transfer_amount": None}

# class ActionServices(Action):

#     def name(self) -> Text:
#         return "action_select_service"


#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         ser = tracker.slots.get('service_name')
#         # print('in another class and action')
#         # print(global_data_config.email)       
#         # print(global_data_config.name) 
#         # print(global_data_config.account_type) 
#         # print(global_data_config.account_hold)             
  
#         if ser.lower() == 'transfer funds':
#             account_type = tracker.slots.get('account_type')
#             account_hold = tracker.slots.get('account_hold')
#             if account_hold == True:
#                 dispatcher.utter_message(response = "utter_account_on_hold")
#                 return []
#             if account_type == 'fixed deposit' or account_type == 'recurring':
#                 dispatcher.utter_message(response = "utter_invalid_acccount_type")
#                 return []
#             else:
#                 dispatcher.utter_message(response = "utter_ask_transfer_amount")
#         else:
#             # SlotSet('service_name', 'check balance')
#             balance = tracker.slots.get('user_balance')
#             dispatcher.utter_message(response = "utter_check_balance")
#         return []



























# class ValidateTransferfundsForm(FormValidationAction):
#     def name(self) -> Text:
        # return "validate_transfer_funds_form"

    # def validate_transfer_amount(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     print('in validation ', slot_value)
    #     if slot_value <= tracker.slots.get('user_balance'):
    #         return {"transfer_amount": slot_value}
    #     else:
    #         # validation failed, set this slot to None so that the
    #         # user will be asked for the slot again
    #         dispatcher.utter_message(response = "utter_insufficient_balance")

    #         return {"transfer_amount": None}


# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# # import sys
# # sys.path.insert(0,'G:\krishvi-xethon\Krishvi--adventure')
# # from global_data_config import fun
# # import global_data_config
# # import Krishvi--adventure.global_data_config
# # from Krishvi--adventure.global_data_config import fun
# #  SlotSet("user_email", global_data_config.email)

# # # SlotSet('user_name', global_data_config.name)

# # # SlotSet('user_balance',global_data_config.balance)

# # # SlotSet('account_number',global_data_config.account_number)

# # # SlotSet('account_type', global_data_config.account_type)

# # # SlotSet('account_hold',global_data_config.account_hold)
# from rasa_sdk.events import SlotSet,EventType
# import global_data_config
# class ActionWelcome(Action):
#     def name(self) -> Text:
#         return "action_welcome"
#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         slots = {
#             "user_email": global_data_config.email,
#             "user_name": global_data_config.name,
#             "user_balance": global_data_config.balance,
#             "account_number": global_data_config.account_number,
#             "account_type": global_data_config.account_type,
#             "account_hold": global_data_config.account_hold,
#         }
#         print('check slot values')
#         print(slots['user_email'])
#         print(slots['user_balance'])
  
#         print('global values')
#         print(global_data_config.email,global_data_config.balance,global_data_config.account_number,)
#         dispatcher.utter_message(response = "utter_about_user")        
#         return [SlotSet(slot, value) for slot, value in slots.items()]

# class ActionHelloWorld(Action):
#     def name(self) -> Text:
#         return "action_hello_world"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
#         dispatcher.utter_message(text="Hello World!")
#         return []

# class ActionServices(Action):

#     def name(self) -> Text:
#         return "action_select_service"


#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         ser = tracker.slots.get('service_name')
#         print('in another class and action')
#         print(global_data_config.email)       
#         print(global_data_config.name) 
#         print(global_data_config.account_type) 
#         print(global_data_config.account_hold)             
  
<<<<<<< HEAD
        if ser.lower() == 'transfer funds':
            account_type = tracker.slots.get('account_type')
            account_hold = tracker.slots.get('account_hold')
            if account_hold == True:
                dispatcher.utter_message(response = "utter_account_on_hold")
            if account_type == 'fixed deposit' or account_type == 'recurring':
                dispatcher.utter_message(response = "utter_invalid_acccount_type")
            else:
                dispatcher.utter_message(response = "utter_invalid_acccount_type")
                # dispatcher.utter_message(response = "request_transfer_funds_data")
        else:
            # SlotSet('service_name', 'check balance')
            balance = tracker.slots.get('user_balance')
            dispatcher.utter_message(response = "utter_check_balance")
        return []
=======
#         if ser.lower() == 'transfer funds':
#             account_type = tracker.slots.get('account_type')
#             account_hold = tracker.slots.get('account_hold')
#             if account_hold == True:
#                 dispatcher.utter_message(response = "utter_account_on_hold")
#                 return []
#             if account_type == 'fixed deposit' or account_type == 'recurring':
#                 dispatcher.utter_message(response = "utter_invalid_acccount_type")
#                 return []
#             else:
#                 dispatcher.utter_message(response = "utter_transfer_funds")
#         else:
#             # SlotSet('service_name', 'check balance')
#             balance = tracker.slots.get('user_balance')
#             dispatcher.utter_message(response = "utter_check_balance")
#         return []
>>>>>>> 8955daf1499c8dd2501b9e401f37036a59d39f10
