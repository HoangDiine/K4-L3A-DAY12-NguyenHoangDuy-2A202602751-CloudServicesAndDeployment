"""Agent service — điểm ráp nối của cả lab (CP1, CP3, CP4).

Luồng một request tới /ask:

    client ──► verify_api_key ──► rate_limiter ──► cost_guard
                                                       │
                              store.get_history ◄──────┘
                                       │
                                    ask_llm
                                       │
                              store.append × 2 ──► cost_guard.record ──► log_event
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from utils.mock_llm import ask_llm

from .auth import verify_api_key
from .config import get_settings
from .cost_guard import CostGuard
from .lifecycle import lifecycle
from .logging_utils import log_event
from .rate_limiter import RateLimiter
from .store import ConversationStore, get_redis_client

SERVICE_NAME = "day12-agent"
SERVICE_VERSION = "1.0.0"


# ─────────────────────────────────────────────────────────────
# Providers — CHO SẴN
# Tách ra thành hàm để test có thể thay bằng Redis giả qua
# app.dependency_overrides, và để kết nối Redis chỉ tạo khi thật sự cần.
# ─────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def get_store() -> ConversationStore:
    return ConversationStore(get_redis_client())


@lru_cache(maxsize=1)
def get_rate_limiter() -> RateLimiter:
    return RateLimiter(get_redis_client(), get_settings().rate_limit_per_minute)


@lru_cache(maxsize=1)
def get_cost_guard() -> CostGuard:
    return CostGuard(get_redis_client(), get_settings().monthly_budget_usd)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """CHO SẴN — chạy lúc app khởi động và lúc tắt."""
    lifecycle.install()
    log_event("service_started", service=SERVICE_NAME, version=SERVICE_VERSION)
    yield
    log_event("service_stopped", service=SERVICE_NAME)


app = FastAPI(title="Day 12 Production Agent", version=SERVICE_VERSION, lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


HOME_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day 12 Production Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --text-dim: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --success: #22c55e;
            --warning: #f59e0b;
            --error: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem 1rem;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .header {
            text-align: center;
            padding: 1rem 0;
        }
        .badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        h1 { font-size: 2.1rem; font-weight: 700; margin-bottom: 0.5rem; }
        .subtitle { color: var(--text-dim); font-size: 0.95rem; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            font-size: 0.875rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            font-size: 1.05rem;
        }
        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
        }
        .dot.yellow { background: var(--warning); box-shadow: 0 0 10px var(--warning); }
        .dot.red { background: var(--error); box-shadow: 0 0 10px var(--error); }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-dim);
            margin-bottom: 0.35rem;
        }
        input {
            width: 100%;
            background: #0b1120;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus {
            border-color: var(--accent);
        }
        button {
            width: 100%;
            background: var(--accent);
            color: #0b1120;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.85rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: var(--accent-hover); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .chat-box {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 1rem;
            padding-right: 0.5rem;
        }
        .msg {
            padding: 0.85rem 1rem;
            border-radius: 8px;
            max-width: 85%;
            line-height: 1.5;
            font-size: 0.95rem;
        }
        .msg.user {
            align-self: flex-end;
            background: #2563eb;
            color: white;
        }
        .msg.bot {
            align-self: flex-start;
            background: #334155;
            color: var(--text);
        }
        .msg-meta {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 0.35rem;
        }
        .links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }
        .links a {
            color: var(--accent);
            text-decoration: none;
            font-size: 0.875rem;
        }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🚀 Production Ready</span>
            <h1>Day 12 Production Agent</h1>
            <p class="subtitle">Học viên: <strong>Nguyễn Hoàng Duy</strong> (MSSV: 2A202602751) • Cloud Deployment on Railway</p>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-title">Liveness Probe (/health)</div>
                <div class="status-pill">
                    <span class="dot" id="health-dot"></span> <span id="health-text">Đang kiểm tra...</span>
                </div>
            </div>
            <div class="card">
                <div class="card-title">Readiness Probe (/ready)</div>
                <div class="status-pill">
                    <span class="dot" id="ready-dot"></span> <span id="ready-text">Đang kết nối Redis...</span>
                </div>
            </div>
            <div class="card">
                <div class="card-title">Platform</div>
                <div class="status-pill">
                    <span class="dot"></span> <span>Railway Cloud</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h2 style="font-size: 1.25rem; margin-bottom: 1rem;">💬 Trò chuyện với Agent (/ask)</h2>
            <div class="form-group">
                <label for="apiKey">X-API-Key (Khóa xác thực):</label>
                <input type="password" id="apiKey" value="rgBiClDjf1l_h8rsc6w8gxL--bFLiPeK01yIGkBQvDc" placeholder="Nhập AGENT_API_KEY...">
            </div>
            <div class="form-group">
                <label for="question">Câu hỏi:</label>
                <input type="text" id="question" placeholder="Ví dụ: Deploy là gì? Stateless là gì?..." onkeypress="if(event.key==='Enter') sendQuestion()">
            </div>
            <button id="sendBtn" onclick="sendQuestion()">Gửi câu hỏi</button>

            <div class="chat-box" id="chatBox">
                <div class="msg bot">
                    Xin chào! Tôi là Day 12 Production Agent được triển khai trên Railway và kết nối với Redis. Hãy thử gửi câu hỏi cho tôi!
                </div>
            </div>
        </div>

        <div class="links">
            <a href="/health" target="_blank">Liveness (/health)</a>
            <span>•</span>
            <a href="/ready" target="_blank">Readiness (/ready)</a>
            <span>•</span>
            <a href="/docs" target="_blank">Swagger API Docs (/docs)</a>
        </div>
    </div>

    <script>
        async function checkStatus() {
            try {
                const hRes = await fetch('/health');
                const hData = await hRes.json();
                if (hRes.ok && hData.status === 'ok') {
                    document.getElementById('health-text').innerText = 'Online (' + hData.service + ')';
                    document.getElementById('health-dot').className = 'dot';
                } else {
                    throw new Error();
                }
            } catch {
                document.getElementById('health-text').innerText = 'Offline';
                document.getElementById('health-dot').className = 'dot red';
            }

            try {
                const rRes = await fetch('/ready');
                const rData = await rRes.json();
                if (rRes.ok && rData.redis) {
                    document.getElementById('ready-text').innerText = 'Redis Connected';
                    document.getElementById('ready-dot').className = 'dot';
                } else {
                    throw new Error();
                }
            } catch {
                document.getElementById('ready-text').innerText = 'Not Ready';
                document.getElementById('ready-dot').className = 'dot yellow';
            }
        }

        async function sendQuestion() {
            const qInput = document.getElementById('question');
            const keyInput = document.getElementById('apiKey');
            const btn = document.getElementById('sendBtn');
            const chatBox = document.getElementById('chatBox');
            const q = qInput.value.trim();
            const key = keyInput.value.trim();

            if (!q) return;

            const userMsg = document.createElement('div');
            userMsg.className = 'msg user';
            userMsg.innerText = q;
            chatBox.appendChild(userMsg);
            qInput.value = '';
            btn.disabled = true;
            btn.innerText = 'Đang xử lý...';

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': key,
                        'X-User-Id': 'web-guest'
                    },
                    body: JSON.stringify({ question: q })
                });
                const data = await res.json();
                const botMsg = document.createElement('div');
                botMsg.className = 'msg bot';

                if (res.ok) {
                    botMsg.innerHTML = data.answer + '<div class="msg-meta">History: ' + data.history_length + ' | Tokens: in=' + data.tokens.in + ', out=' + data.tokens.out + ' | Chi phí: $' + data.cost_usd.toFixed(6) + '</div>';
                } else {
                    botMsg.innerHTML = '<span style="color:#ef4444">Lỗi (' + res.status + '): ' + (data.detail || 'Không gửi được') + '</span>';
                }
                chatBox.appendChild(botMsg);
            } catch (err) {
                const errMsg = document.createElement('div');
                errMsg.className = 'msg bot';
                errMsg.innerHTML = '<span style="color:#ef4444">Lỗi mạng: Không thể kết nối tới server.</span>';
                chatBox.appendChild(errMsg);
            } finally {
                btn.disabled = false;
                btn.innerText = 'Gửi câu hỏi';
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        checkStatus();
        setInterval(checkStatus, 10000);
    </script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────
# Health & readiness
# ─────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index():
    return HOME_HTML


@app.get("/health")
def health():
    """Liveness probe — process còn sống không?"""
    if lifecycle.shutting_down:
        return JSONResponse(status_code=503, content={"status": "shutting_down"})
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}


@app.get("/ready")
def ready(store: ConversationStore = Depends(get_store)):
    """Readiness probe — đã sẵn sàng nhận traffic chưa?"""
    if lifecycle.shutting_down:
        return JSONResponse(status_code=503, content={"status": "shutting_down"})
    if not store.ping():
        return JSONResponse(status_code=503, content={"status": "not ready", "redis": False})
    return {"status": "ready", "redis": True}



# ─────────────────────────────────────────────────────────────
# Endpoint chính
# ─────────────────────────────────────────────────────────────
@app.post("/ask")
def ask(
    payload: AskRequest,
    user_id: str = Depends(verify_api_key),
    store: ConversationStore = Depends(get_store),
    limiter: RateLimiter = Depends(get_rate_limiter),
    guard: CostGuard = Depends(get_cost_guard),
):
    """Hỏi agent một câu.

    TODO (CP3 + CP4) — làm ĐÚNG THỨ TỰ sau:
      1. ``limiter.check(user_id)``           → 429 nếu gọi quá nhanh
      2. ``guard.check(user_id)``             → 402 nếu hết ngân sách
      3. ``history = store.get_history(user_id)``
      4. ``result = ask_llm(payload.question, history)``
      5. ``store.append(user_id, "user", payload.question)`` và
         ``store.append(user_id, "assistant", result["answer"])``
      6. ``guard.record(user_id, result["cost_usd"])``
      7. ``log_event("ask_completed", user_id=user_id,
         tokens_in=result["tokens_in"], tokens_out=result["tokens_out"],
         cost_usd=result["cost_usd"])``
      8. trả về::

            {
                "answer": result["answer"],
                "user_id": user_id,
                "history_length": len(history),
                "cost_usd": result["cost_usd"],
                "tokens": {"in": result["tokens_in"], "out": result["tokens_out"]},
            }

    Vì sao check trước rồi mới gọi LLM? Vì tiền mất ở bước gọi LLM. Chặn sau
    khi đã gọi thì bạn vừa trả tiền vừa trả lỗi.

    ``user_id`` do ``verify_api_key`` trả về, nên request không có API key
    hợp lệ sẽ dừng ở 401 trước khi chạm vào bất cứ dòng nào ở đây.
    """
    limiter.check(user_id)
    guard.check(user_id)
    history = store.get_history(user_id)
    result = ask_llm(payload.question, history)
    store.append(user_id, "user", payload.question)
    store.append(user_id, "assistant", result["answer"])
    guard.record(user_id, result["cost_usd"])
    log_event(
        "ask_completed",
        user_id=user_id,
        tokens_in=result["tokens_in"],
        tokens_out=result["tokens_out"],
        cost_usd=result["cost_usd"],
    )
    return {
        "answer": result["answer"],
        "user_id": user_id,
        "history_length": len(history),
        "cost_usd": result["cost_usd"],
        "tokens": {"in": result["tokens_in"], "out": result["tokens_out"]},
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
