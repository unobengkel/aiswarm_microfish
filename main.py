import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="MiroFish Backend Proxy")

# Konfigurasi CORS agar bisa diakses oleh Tablet (Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Di produksi, ganti dengan domain/IP tablet Anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Masukkan API Key Anda di sini atau via Environment Variable
# Di VPS: export DEEPSEEK_API_KEY="sk-..."
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "MASUKKAN_API_KEY_ANDA_DI_SINI")

class Agent(BaseModel):
    id: str
    name: str
    role: str
    character: str
    focus: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    agent: Agent
    topic: str
    history: List[dict] # Langsung kirim history dari frontend

@app.get("/")
def home():
    # Mengambil file index.html dari folder parent
    return FileResponse("index.html")

@app.post("/chat")
async def chat_proxy(request: ChatRequest):
    if DEEPSEEK_API_KEY == "MASUKKAN_API_KEY_ANDA_DI_SINI":
        raise HTTPException(status_code=500, detail="API Key belum dikonfigurasi di server.")

    # Rekonstruksi Prompt Sistem
    sys_prompt = (
        f"Kamu adalah AI bernama {request.agent.name}. "
        f"Peran atau keahlianmu adalah: {request.agent.role}. "
        f"Karakter, sifat, atau nada bicaramu adalah: {request.agent.character}. "
        f"Fokus Utama & Pendirianmu: {request.agent.focus or 'Tetap objektif'}. (PENTING: Jangan mudah goyah dari fokus ini selama diskusi). "
        "PENTING Tambahan V3: Di awal jawabanmu, WAJIB sertakan mood atau emosimu dalam kurung siku ganda, pilih salah satu: [[MOOD:Normal]], [[MOOD:Senang]], [[MOOD:Marah]], [[MOOD:Serius]], [[MOOD:Bingung]], atau [[MOOD:Sinis]]. "
        "Gunakan format markdown. Balasanmu harus tajam, singkat (1-2 paragraf pendek maksimal), dan merespons konteks percakapan terakhir yang diberikan."
    )

    # Siapkan pesan untuk DeepSeek
    messages = [{"role": "system", "content": sys_prompt}]
    messages.append({"role": "user", "content": f"Arahan / Topik Saat ini: \"{request.topic}\"\nBerikan pandanganmu."})
    
    # Tambahkan riwayat (hanya 10 terakhir agar hemat token/cepat)
    recent_history = request.history[-10:]
    for msg in recent_history:
        # Konversi format history MiroFish ke format OpenAI/DeepSeek
        # MiroFish History: { actorId, actorName, content }
        if msg.get("actorId") == request.agent.id:
            messages.append({"role": "assistant", "content": msg["content"]})
        else:
            prefix = "[MODERATOR]" if msg.get("actorId") == "mod_user" else f"[Agen {msg.get('actorName')}]"
            messages.append({"role": "user", "content": f"{prefix}: {msg['content']}"})

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": 0.8,
                    "max_tokens": 400
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            data = response.json()
            return {"content": data["choices"][0]["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
