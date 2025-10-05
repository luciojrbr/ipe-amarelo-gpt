from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai, os

app = FastAPI(title="Ipê-Amarelo GPT Bridge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/api/ipe-amarelo")
async def ipe_amarelo_chat(req: Request):
    body = await req.json()
    user_prompt = body.get("prompt", "")
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{
            "role":
            "system",
            "content":
            "Você é Ipê-Amarelo 🌳, gestora de eventos inteligente da evento.ai."
        }, {
            "role": "user",
            "content": user_prompt
        }],
        temperature=0.7,
        max_tokens=300)
    resposta = completion.choices[0].message["content"]
    return {"resposta": resposta}


@app.get("/")
def status():
    return {"status": "ativo", "modulo": "Ipê-Amarelo GPT Bridge"}

