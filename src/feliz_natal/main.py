from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

class Item(BaseModel):
    phone: str
    message: str

@app.get("/")
def welcome():
    return {"message": "System running!"}

@app.post("/message")
def send_message(item: Item):
    json_request = {
        "phone": f"55{item.phone}",
        "message": item.message,
    }

    client_token = os.getenv("TOKEN")

    headers = {
        "Client-Token": client_token
    }

    try:
        response = requests.post(
            f"{os.getenv('BASE_URL')}/send-text",
            json=json_request,
            headers=headers
        )

        print(response.json())

        if response.status_code not in [200, 201]:
            return {"message": f"There's an error in JSON response: {response.status_code}, {response.json()}"}

    except requests.RequestException as err:
        return {"error": f"There's an error in request to the API: {err}"}

    return {"message": response.json()}
