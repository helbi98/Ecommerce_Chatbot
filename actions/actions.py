from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from typing import Any, Text, Dict, List
import re
import random
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ecommerce_bot",
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


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
        order_number = f"{random.randint(10000, 99999)}"

        connection = get_db_connection()
        if connection:
            if item_name and item_name.lower() in available_items:
                cursor = connection.cursor()
                insert_query = """ 
                                INSERT INTO orders (order_number, item_name, order_status)
                                    VALUES (%s, %s, %s)
                                """
                cursor.execute(insert_query, (order_number, item_name, "Placed"))
                connection.commit()
                cursor.close()
                connection.close()
                dispatcher.utter_message(
                    text=f"Great choice! Placed an order for {item_name}. Order number: {order_number}."
                )
                return [SlotSet("item_name", item_name)]
            else:
                dispatcher.utter_message(
                    text=f"Sorry, this item is not available. Please choose from the below items:\n1. Smartphone\n2. Headphones\n3. Laptop\n4. Smartwatch\n"
                )
                return [SlotSet("item_name", None)]
        else:
            dispatcher.utter_message(
                "Sorry, there was an issue placing your order. Please try again later."
            )


# Logic for tracking order
class ActionTrackOrder(Action):
    def name(self) -> str:
        return "action_track_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        order_number = tracker.get_slot("order_number")

        connection = get_db_connection()
        if connection:
            if order_number:
                cursor = connection.cursor()
                select_query = "SELECT order_status FROM orders WHERE order_number = %s"
                cursor.execute(select_query, (order_number,))
                result = cursor.fetchone()

                if result:
                    status = result[0]
                    dispatcher.utter_message(
                        text=f"Your order {order_number} is {status}."
                    )
                else:
                    dispatcher.utter_message(
                        text="Sorry, I couldn't find your order number."
                    )
                cursor.close()
                connection.close()
        else:
            dispatcher.utter_message(
                "Sorry, I couldn't track your order at the moment."
            )
        return [SlotSet("order_number", None)]


# Logic for canceling the order
class ActionCancelOrder(Action):
    def name(self) -> str:
        return "action_cancel_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> list:
        order_number = tracker.get_slot("order_number")
        connection = get_db_connection()
        if connection:
            if order_number:
                cursor = connection.cursor()

                update_query = (
                    "UPDATE orders SET order_status = %s WHERE order_number = %s"
                )
                cursor.execute(update_query, ("Cancelled", order_number))
                connection.commit()
                if cursor.rowcount > 0:
                    dispatcher.utter_message(
                        text=f"Order {order_number} has been cancelled."
                    )
                else:
                    dispatcher.utter_message(
                        text="Sorry, I couldn't find your order number."
                    )
                cursor.close()
                connection.close()
        else:
            dispatcher.utter_message(
                "Sorry, I couldn't cancel your order at the moment."
            )
        return [SlotSet("order_number", None)]
