from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

class textField(BaseModel) :
  text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/textreturn")
def text_return(data: dict):
    if "text" in data:
        input_text = data["text"]
        return {'text': input_text}
    else:
        return {'error': 'Invalid request payload'}
    
if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)