from  fastapi import FastAPI
from typing import Optional,List
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("api_key")
app=FastAPI()
"""
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }
"""
class Text(BaseModel):
   text:str
class Parts(BaseModel):
   parts:List[Text]
class Contents(BaseModel):
    contents:List[Parts]
   
@app.get("/")
def read_root(conditional : Optional[bool]=True):
    if conditional:
      return {"message" : f"hello world"}
    else:
       return {"message" : f"goodbye world"}
    

@app.get("/{id}")
def read_root(id:int):
    return {"message" : f"hello world {id}"}

@app.post("/ask")
def ask(ques:Contents):
    response = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}',json=ques.model_dump())
    answer = response.json()
    return answer["candidates"][0]["content"]["parts"][0]["text"]



