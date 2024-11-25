from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from typing import Any, Text, Dict, List
import re


# To check if the order number is a valid 5-digit number
class ActionValidateOrderNumber(Action):
    def name(self) -> str:
        return "action_validate_order_number"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        order_number = tracker.get_slot("order_number")
        context = tracker.get_slot("context")

        if order_number and re.fullmatch(r"\d{5}", order_number):
            if context == "cancel":
                return [
                    SlotSet("order_number", order_number),
                    FollowupAction("action_cancel_order"),
                ]
            elif context == "track":
                return [
                    SlotSet("order_number", order_number),
                    FollowupAction("action_track_order"),
                ]
        else:
            dispatcher.utter_message(
                text="The order number you provided is invalid. It should be a 5-digit number"
            )
            return [
                SlotSet("order_number", None),
                FollowupAction("utter_ask_order_number"),
            ]


# To set the 'cancel' context when the user mentions canceling an order
class ActionSetCancelContext(Action):
    def name(self) -> str:
        return "action_set_cancel_context"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        return [SlotSet("context", "cancel")]


# To set the 'track' context when the user mentions tracking an order
class ActionSetTrackContext(Action):
    def name(self) -> str:
        return "action_set_track_context"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        return [SlotSet("context", "track")]


# To check if the item in place order request is valid or not
class ActionValidateItem(Action):
    def name(self) -> Text:
        return "action_validate_item"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        available_items = ["smartphone", "headphones", "laptop", "smartwatch"]
        item_name = tracker.get_slot("item_name")

        if item_name and item_name.lower() in available_items:
            dispatcher.utter_message(
                text=f"Great choice! Placed an order for {item_name}."
            )
            return [SlotSet("item_name", item_name)]
        else:
            dispatcher.utter_message(
                text=f"Sorry, this item is not available. Please choose from the below items:\n1. Smartphone\n2. Headphones\n3. Laptop\n4. Smartwatch\n"
            )
            return [SlotSet("item_name", None)]


# Logic for tracking order
class ActionTrackOrder(Action):
    def name(self) -> str:
        return "action_track_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        order_number = tracker.get_slot("order_number")
        if order_number:
            dispatcher.utter_message(text=f"Your order {order_number} is on the way.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find your order number.")
        return [SlotSet("order_number", None)]


# Logic for canceling the order
class ActionCancelOrder(Action):
    def name(self) -> str:
        return "action_cancel_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        order_number = tracker.get_slot("order_number")
        if order_number:
            dispatcher.utter_message(text=f"Order {order_number} has been cancelled.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find your order number.")
        return [SlotSet("order_number", None)]
