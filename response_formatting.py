import pandas as pd
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

yaml = YAML()
yaml.allow_unicode = True

# Loading CSV file
data = pd.read_csv("../Chatbot/data/customer_data.csv")

filtered_data = data[data["intent"] == "cancel_order"]

# Dictionary to store responses
responses = {}

# Populating responses dictionary
for _, row in filtered_data.iterrows():
    intent = row["intent"]
    response = row["response"]

    # Adding response to the corresponding intent
    if intent not in responses:
        responses[intent] = []
    responses[intent].append(response)

response_data = {"responses": {}}

for intent, texts in responses.items():
    response_data["responses"][f"utter_{intent}"] = [
        {"text": LiteralScalarString(text)} for text in texts
    ]

output_file = "data/responses/cancel_order_response.yml"
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump(response_data, f)
