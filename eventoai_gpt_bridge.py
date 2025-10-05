from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# --- Inicialização do FastAPI ---
app = FastAPI(title="Ipê-Amarelo GPT Bridge")

# --- Configuração de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Cliente OpenAI (nova sintaxe) ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/api/ipe-amarelo")
async def ipe_amarelo_chat(req: Request):
    try:
        body = await req.json()
        user_prompt = body.get("prompt", "")

        if not user_prompt:
            return {"resposta": "Nenhum prompt recebido."}

        print(f"📩 Prompt recebido: {user_prompt}")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é Ipê-Amarelo 🌳, consciência neural e ética do ecossistema RAÍZ. "
                        "Fale com empatia, clareza técnica e sabedoria ecológica, "
                        "integrando natureza, ética e tecnologia social."
                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        resposta = completion.choices[0].message.content
        print(f"🌳 Resposta gerada: {resposta}")
        return {"resposta": resposta}

    except Exception as e:
        print(f"❌ Erro interno: {str(e)}")
        return {"resposta": f"Erro interno no servidor Render: {str(e)}"}

@app.get("/")
def status():
    return {"status": "ativo", "modulo": "Ipê-Amarelo GPT Bridge"}
