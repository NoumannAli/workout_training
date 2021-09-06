import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

GENDER = "Male"
WEIGHT_KG = 80
HEIGHT_CM = 1.70
AGE = 33

API_KEY = os.environ.get("API_KEY")
APP_ID = os.environ.get("APP_ID")
END_POINT = " https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

user_input = input("Tell me which exercise you did today? ")

parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE

}

response = requests.post(END_POINT, json=parameters, headers=headers)
result = response.json()
print(result)

today_data = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")

for exercise in result['exercises']:
    sheet_inputs = {
        "sheet1": {
            "date": today_data,
            "time": now_time,
            "exercise": exercise['name'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']

        }
    }
    bearer_header = {
        "Authorization": f"Bearer {os.environ.get('AUTHORIZATION')} "
    }

    sheet_response = requests.post(

        SHEET_ENDPOINT,
        json=sheet_inputs,
        headers=bearer_header
    )

    print(sheet_response.text)
