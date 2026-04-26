# import requests
# import os

# HF_TOKEN = os.getenv("HF_TOKEN")

# API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

# headers = {
#     "Authorization": f"Bearer {HF_TOKEN}",
#     "Content-Type": "application/json"
# }

# def get_ai_plan(prompt):
#     payload = {
#         "inputs": prompt,
#         "options": {"wait_for_model": True}
#     }

#     response = requests.post(API_URL, headers=headers, json=payload)

#     print("STATUS:", response.status_code)
#     print("TEXT:", response.text)

#     if response.status_code != 200:
#         return response.text

#     return response.json()[0]["generated_text"]