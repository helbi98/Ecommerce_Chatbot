import pandas as pd
import random
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

yaml = YAML()
yaml.allow_unicode = True

# Loading CSV file
data = pd.read_csv("../Chatbot/data/customer_data.csv")

# List of predefined order numbers
order_numbers = [20241, 20242, 20243, 20245, 20246, 20247, 20248, 20249, 20250]

filtered_data = data[data["intent"] == "cancel_order"]

# Dictionary to store intents
intents = {}

# Populating intents dictionary
for _, row in filtered_data.iterrows():
    intent = row["intent"]
    instruction = row["instruction"]

    # Replacing {{Order Number}} with a random order number from the list
    formatted_instruction = instruction
    formatted_instruction = formatted_instruction.replace(
        "{{Order Number}}", f"[{random.choice(order_numbers)}](Order Number)"
    )

    # Add formatted instruction to the corresponding intent
    if intent not in intents:
        intents[intent] = []
    intents[intent].append(formatted_instruction)

nlu_data = {"version": "3.1", "nlu": []}

for intent, examples in intents.items():
    nlu_data["nlu"].append(
        {
            "intent": intent,
            "examples": LiteralScalarString("\n".join([f"- {ex}" for ex in examples])),
        }
    )

output_file = "data/intents/cancel_order.yml"
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump(nlu_data, f)
