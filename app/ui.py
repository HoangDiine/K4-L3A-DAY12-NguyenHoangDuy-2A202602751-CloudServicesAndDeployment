"""Web UI Dashboard for Day 12 Production Agent."""

INDEX_HTML = """<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day 12 Production Agent | Cloud Services & Deployment</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            400: '#38bdf8',
                            500: '#0ea5e9',
                            600: '#0284c7',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #080c14;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.15) 0px, transparent 45%),
                radial-gradient(circle at 85% 85%, rgba(14, 165, 233, 0.15) 0px, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.06) 0px, transparent 65%);
            background-attachment: fixed;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 16px 32px -10px rgba(14, 165, 233, 0.2);
        }
        .glow-pulse {
            box-shadow: 0 0 14px rgba(34, 197, 94, 0.55);
        }
        .chat-scroll::-webkit-scrollbar {
            width: 6px;
        }
        .chat-scroll::-webkit-scrollbar-track {
            background: transparent;
        }
        .chat-scroll::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
        }
        .chat-scroll::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.22);
        }
        @keyframes bounce-delay {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }
        .typing-dot {
            animation: bounce-delay 1.4s infinite ease-in-out both;
        }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        .code-inline {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1px 5px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85em;
            color: #38bdf8;
        }
    </style>
</head>
<body class="text-slate-100 min-h-screen flex flex-col items-center justify-between p-3 sm:p-6 antialiased selection:bg-brand-500 selection:text-white">

    <!-- Top Navigation Bar -->
    <header class="w-full max-w-5xl glass-panel rounded-2xl p-4 sm:px-6 mb-5 shadow-2xl flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/25 ring-1 ring-white/20">
                <i data-lucide="bot" class="w-6 h-6 text-white"></i>
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 class="text-lg font-bold tracking-tight text-white">Day 12 Production Agent</h1>
                    <span class="text-[11px] px-2.5 py-0.5 rounded-full font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 flex items-center gap-1.5 shadow-sm">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> v1.0.0 Live
                    </span>
                </div>
                <p class="text-xs text-slate-400 mt-0.5">Cloud Services, High Availability & Modern Deployment</p>
            </div>
        </div>

        <div class="flex items-center gap-3 ml-auto">
            <div class="hidden sm:flex items-center gap-2 bg-slate-900/90 px-3.5 py-1.5 rounded-xl border border-slate-700/70 text-xs shadow-inner">
                <i data-lucide="graduation-cap" class="w-4 h-4 text-brand-400"></i>
                <span class="text-slate-200 font-semibold">Nguyễn Hoàng Duy</span>
                <span class="text-slate-600">•</span>
                <span class="text-slate-400 font-mono">2A202602751</span>
            </div>
            <a href="https://github.com/HoangDiine/K4-L3A-DAY12-NguyenHoangDuy-2A202602751-CloudServicesAndDeployment" target="_blank" title="GitHub Repository" class="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/70 text-slate-300 hover:text-white transition shadow-sm">
                <i data-lucide="github" class="w-4 h-4"></i>
            </a>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="w-full max-w-5xl flex-1 flex flex-col gap-5">

        <!-- Architecture & Probe Status Cards -->
        <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Liveness Probe -->
            <div class="glass-card rounded-2xl p-4 sm:p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <i data-lucide="heart-pulse" class="w-3.5 h-3.5 text-emerald-400"></i> Liveness Probe
                    </span>
                    <span id="health-code" class="text-xs font-mono font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">200 OK</span>
                </div>
                <div class="flex items-center gap-3 my-1">
                    <div id="health-indicator" class="w-3 h-3 rounded-full bg-emerald-500 glow-pulse"></div>
                    <div>
                        <div id="health-status" class="text-sm sm:text-base font-bold text-white">Online & Healthy</div>
                        <div class="text-[11px] text-slate-400 font-mono">GET /health • Zero-dependency</div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <span>Process</span>
                    <span class="font-mono text-slate-300 text-[11px]">FastAPI + Uvicorn ASGI</span>
                </div>
            </div>

            <!-- Readiness Probe -->
            <div class="glass-card rounded-2xl p-4 sm:p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <i data-lucide="database" class="w-3.5 h-3.5 text-brand-400"></i> Readiness Probe
                    </span>
                    <span id="ready-code" class="text-xs font-mono font-medium px-2 py-0.5 rounded bg-brand-500/10 text-brand-400 border border-brand-500/20">Redis 8.2</span>
                </div>
                <div class="flex items-center gap-3 my-1">
                    <div id="ready-indicator" class="w-3 h-3 rounded-full bg-emerald-500 glow-pulse"></div>
                    <div>
                        <div id="ready-status" class="text-sm sm:text-base font-bold text-white">Redis Connected</div>
                        <div class="text-[11px] text-slate-400 font-mono">GET /ready • Stateless Memory</div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <span>Rate Limit & Budget</span>
                    <span class="font-mono text-slate-300 text-[11px]">10 req/m • $10/mo</span>
                </div>
            </div>

            <!-- Cloud Infrastructure -->
            <div class="glass-card rounded-2xl p-4 sm:p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <i data-lucide="cloud" class="w-3.5 h-3.5 text-indigo-400"></i> Cloud Hosting
                    </span>
                    <span class="text-xs font-mono font-medium px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Railway</span>
                </div>
                <div class="flex items-center gap-3 my-1">
                    <div class="w-3 h-3 rounded-full bg-emerald-500 glow-pulse"></div>
                    <div>
                        <div class="text-sm sm:text-base font-bold text-white">Production Cluster</div>
                        <div class="text-[11px] text-slate-400 font-mono">SFO Region • Dynamic $PORT</div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <span>Docker Container</span>
                    <span class="font-mono text-slate-300 text-[11px]">Multi-stage (Non-root)</span>
                </div>
            </div>
        </section>

        <!-- Interactive AI Agent Console -->
        <section class="glass-panel rounded-2xl flex flex-col shadow-2xl overflow-hidden border border-slate-700/80">
            <!-- Console Header -->
            <div class="px-4 sm:px-5 py-3.5 bg-slate-900/80 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                    <div class="flex gap-1.5">
                        <div class="w-3 h-3 rounded-full bg-rose-500/80"></div>
                        <div class="w-3 h-3 rounded-full bg-amber-500/80"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-500/80"></div>
                    </div>
                    <span class="text-xs font-semibold text-slate-300 ml-2">Console: <code class="text-brand-400 font-mono">POST /ask</code></span>
                </div>

                <!-- API Key & Action Buttons -->
                <div class="flex items-center gap-2.5 text-xs">
                    <div class="flex items-center bg-slate-950/80 border border-slate-700 rounded-xl px-2.5 py-1 gap-2 shadow-inner">
                        <i data-lucide="key" class="w-3.5 h-3.5 text-amber-400 shrink-0"></i>
                        <input type="password" id="apiKey" value="rgBiClDjf1l_h8rsc6w8gxL--bFLiPeK01yIGkBQvDc" class="bg-transparent text-slate-200 font-mono text-xs w-36 sm:w-56 focus:outline-none placeholder-slate-500" placeholder="AGENT_API_KEY...">
                        <button type="button" onclick="toggleKeyVisibility()" title="Ẩn/Hiện API Key" class="text-slate-400 hover:text-slate-200 transition">
                            <i id="keyEyeIcon" data-lucide="eye" class="w-3.5 h-3.5"></i>
                        </button>
                    </div>

                    <button onclick="clearChat()" title="Xóa lịch sử hiển thị" class="px-2.5 py-1 bg-slate-800/80 hover:bg-slate-700 border border-slate-700 rounded-xl text-slate-300 hover:text-white transition flex items-center gap-1.5 text-xs">
                        <i data-lucide="trash-2" class="w-3 h-3"></i>
                        <span class="hidden sm:inline">Xóa chat</span>
                    </button>
                </div>
            </div>

            <!-- Chat Message Feed -->
            <div id="chatFeed" class="chat-scroll p-4 sm:p-6 min-h-[380px] max-h-[480px] overflow-y-auto flex flex-col gap-4">
                <!-- Welcome Bot Message -->
                <div class="flex items-start gap-3 max-w-[88%]">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shrink-0 shadow-md ring-1 ring-white/10">
                        <i data-lucide="sparkles" class="w-4 h-4 text-white"></i>
                    </div>
                    <div class="bg-slate-800/90 border border-slate-700/80 rounded-2xl rounded-tl-sm p-4 shadow-sm text-sm text-slate-200 leading-relaxed">
                        <p class="font-bold text-white mb-1">Xin chào Hoàng Duy! 👋</p>
                        Tôi là **Day 12 Production Agent** được triển khai trực tiếp trên nền tảng **Railway Cloud**, đồng bộ cơ sở dữ liệu **Redis 8.2** với đầy đủ các chuẩn sản xuất:
                        <ul class="list-disc list-inside mt-2 space-y-1 text-slate-300 text-xs">
                            <li><strong>Xác thực bảo mật:</strong> Header <code class="code-inline">X-API-Key</code> so sánh an toàn bằng <code class="code-inline">secrets.compare_digest</code></li>
                            <li><strong>Kiểm soát lưu lượng:</strong> Thuật toán cửa sổ trượt (Sliding Window) qua Redis Sorted Set (10 req/phút)</li>
                            <li><strong>Bảo vệ ngân sách:</strong> Cost Guard theo dõi chi phí hàng tháng bằng Redis Hash ($10.00/tháng)</li>
                            <li><strong>Độ tin cậy:</strong> Tách biệt <code class="code-inline">/health</code> (Liveness) &amp; <code class="code-inline">/ready</code> (Readiness), Graceful Shutdown qua SIGTERM</li>
                        </ul>
                        <p class="mt-3 text-xs text-slate-400">Chọn câu hỏi nhanh bên dưới hoặc nhập câu hỏi bất kỳ để trò chuyện nhé!</p>
                    </div>
                </div>
            </div>

            <!-- Quick Suggestion Chips -->
            <div class="px-4 sm:px-6 py-2.5 bg-slate-900/40 border-t border-slate-800/60 flex flex-wrap items-center gap-2 text-xs">
                <span class="text-slate-500 text-xs font-medium flex items-center gap-1">
                    <i data-lucide="zap" class="w-3 h-3 text-amber-400"></i> Gợi ý:
                </span>
                <button onclick="usePrompt(this)" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition shadow-sm">Deploy là gì?</button>
                <button onclick="usePrompt(this)" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition shadow-sm">Stateless service là gì?</button>
                <button onclick="usePrompt(this)" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition shadow-sm">Vì sao /health khác /ready?</button>
                <button onclick="usePrompt(this)" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition shadow-sm">Rate limit cửa sổ trượt là gì?</button>
            </div>

            <!-- Input Bar -->
            <div class="p-3 sm:p-4 bg-slate-900/90 border-t border-slate-800">
                <form id="chatForm" onsubmit="event.preventDefault(); handleSend();" class="relative flex items-center">
                    <input type="text" id="userInput" placeholder="Nhập câu hỏi cho Production Agent (Enter để gửi)..." class="w-full bg-slate-950/90 border border-slate-700/80 rounded-xl pl-4 pr-28 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition shadow-inner">
                    <button type="submit" id="sendButton" class="absolute right-1.5 px-4 py-2 bg-gradient-to-r from-brand-500 to-indigo-600 hover:from-brand-600 hover:to-indigo-700 text-white font-semibold rounded-lg text-xs flex items-center gap-1.5 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-md shadow-brand-500/20 active:scale-95">
                        <span>Gửi</span>
                        <i data-lucide="send" class="w-3.5 h-3.5"></i>
                    </button>
                </form>
            </div>
        </section>

        <!-- Fast Links & Diagnostic Endpoints -->
        <section class="flex flex-wrap items-center justify-center gap-3 text-xs text-slate-400">
            <a href="/health" target="_blank" class="flex items-center gap-1.5 hover:text-brand-400 transition bg-slate-900/60 hover:bg-slate-800/80 px-3.5 py-1.5 rounded-xl border border-slate-800/80 shadow-sm">
                <i data-lucide="activity" class="w-3.5 h-3.5 text-emerald-400"></i> Liveness Probe (<code class="font-mono text-slate-300">/health</code>)
            </a>
            <a href="/ready" target="_blank" class="flex items-center gap-1.5 hover:text-brand-400 transition bg-slate-900/60 hover:bg-slate-800/80 px-3.5 py-1.5 rounded-xl border border-slate-800/80 shadow-sm">
                <i data-lucide="layers" class="w-3.5 h-3.5 text-brand-400"></i> Readiness Probe (<code class="font-mono text-slate-300">/ready</code>)
            </a>
            <a href="/docs" target="_blank" class="flex items-center gap-1.5 hover:text-brand-400 transition bg-slate-900/60 hover:bg-slate-800/80 px-3.5 py-1.5 rounded-xl border border-slate-800/80 shadow-sm">
                <i data-lucide="file-code" class="w-3.5 h-3.5 text-indigo-400"></i> Swagger OpenAPI (<code class="font-mono text-slate-300">/docs</code>)
            </a>
        </section>

    </main>

    <!-- Footer -->
    <footer class="w-full max-w-5xl text-center py-4 mt-5 text-xs text-slate-500 border-t border-slate-800/60">
        K4 Level 3A • Day 12 Lab: Cloud Services & Deployment • Học viên: <strong class="text-slate-400">Nguyễn Hoàng Duy</strong> (MSSV: <span class="font-mono text-slate-400">2A202602751</span>)
    </footer>

    <!-- App Logic Script -->
    <script>
        lucide.createIcons();

        function toggleKeyVisibility() {
            const input = document.getElementById('apiKey');
            const icon = document.getElementById('keyEyeIcon');
            if (input.type === 'password') {
                input.type = 'text';
                icon.setAttribute('data-lucide', 'eye-off');
            } else {
                input.type = 'password';
                icon.setAttribute('data-lucide', 'eye');
            }
            lucide.createIcons();
        }

        function clearChat() {
            const chatFeed = document.getElementById('chatFeed');
            chatFeed.innerHTML = `
                <div class="flex items-start gap-3 max-w-[88%]">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shrink-0 shadow-md ring-1 ring-white/10">
                        <i data-lucide="sparkles" class="w-4 h-4 text-white"></i>
                    </div>
                    <div class="bg-slate-800/90 border border-slate-700/80 rounded-2xl rounded-tl-sm p-4 shadow-sm text-sm text-slate-200">
                        Đã làm mới màn hình trò chuyện. Hãy đặt câu hỏi tiếp theo!
                    </div>
                </div>
            `;
            lucide.createIcons();
        }

        async function fetchSystemStatus() {
            try {
                const res = await fetch('/health');
                const data = await res.json();
                if (res.ok && data.status === 'ok') {
                    document.getElementById('health-status').innerText = 'Online & Healthy';
                    document.getElementById('health-indicator').className = 'w-3 h-3 rounded-full bg-emerald-500 glow-pulse';
                    document.getElementById('health-code').innerText = '200 OK';
                } else {
                    throw new Error();
                }
            } catch {
                document.getElementById('health-status').innerText = 'Degraded / Offline';
                document.getElementById('health-indicator').className = 'w-3 h-3 rounded-full bg-rose-500';
                document.getElementById('health-code').innerText = 'Error';
            }

            try {
                const res = await fetch('/ready');
                const data = await res.json();
                if (res.ok && data.redis) {
                    document.getElementById('ready-status').innerText = 'Redis Connected';
                    document.getElementById('ready-indicator').className = 'w-3 h-3 rounded-full bg-emerald-500 glow-pulse';
                    document.getElementById('ready-code').innerText = 'Redis Live';
                } else {
                    throw new Error();
                }
            } catch {
                document.getElementById('ready-status').innerText = 'Redis Unreachable';
                document.getElementById('ready-indicator').className = 'w-3 h-3 rounded-full bg-amber-500';
                document.getElementById('ready-code').innerText = '503 Error';
            }
        }

        function usePrompt(btn) {
            const input = document.getElementById('userInput');
            input.value = btn.innerText;
            input.focus();
        }

        function formatMessageContent(content) {
            let escaped = escapeHtml(content);
            // bold: **text**
            escaped = escaped.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-white font-semibold">$1</strong>');
            // code: `text`
            escaped = escaped.replace(/`([^`]+)`/g, '<code class="code-inline">$1</code>');
            // newlines
            escaped = escaped.replace(/\\n/g, '<br>');
            return escaped;
        }

        async function handleSend() {
            const input = document.getElementById('userInput');
            const keyInput = document.getElementById('apiKey');
            const sendBtn = document.getElementById('sendButton');
            const chatFeed = document.getElementById('chatFeed');
            const text = input.value.trim();
            const key = keyInput.value.trim();

            if (!text) return;

            // Render User Bubble
            const userBubble = document.createElement('div');
            userBubble.className = 'flex items-start justify-end gap-3 max-w-[85%] self-end';
            userBubble.innerHTML = `
                <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-700 text-white rounded-2xl rounded-tr-sm p-3.5 shadow-md text-sm leading-relaxed border border-indigo-500/30">
                    ${escapeHtml(text)}
                </div>
                <div class="w-8 h-8 rounded-xl bg-slate-800 flex items-center justify-center shrink-0 border border-slate-700 shadow-sm">
                    <i data-lucide="user" class="w-4 h-4 text-slate-300"></i>
                </div>
            `;
            chatFeed.appendChild(userBubble);
            input.value = '';
            input.disabled = true;
            sendBtn.disabled = true;
            lucide.createIcons();
            chatFeed.scrollTop = chatFeed.scrollHeight;

            // Render Typing Indicator
            const typingBubble = document.createElement('div');
            typingBubble.id = 'typingBubble';
            typingBubble.className = 'flex items-start gap-3 max-w-[85%]';
            typingBubble.innerHTML = `
                <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shrink-0 shadow-md ring-1 ring-white/10">
                    <i data-lucide="sparkles" class="w-4 h-4 text-white"></i>
                </div>
                <div class="bg-slate-800/80 border border-slate-700/60 rounded-2xl rounded-tl-sm p-3.5 flex items-center gap-1.5 shadow-sm">
                    <div class="w-2 h-2 rounded-full bg-brand-400 typing-dot"></div>
                    <div class="w-2 h-2 rounded-full bg-brand-400 typing-dot"></div>
                    <div class="w-2 h-2 rounded-full bg-brand-400 typing-dot"></div>
                </div>
            `;
            chatFeed.appendChild(typingBubble);
            chatFeed.scrollTop = chatFeed.scrollHeight;
            lucide.createIcons();

            const startTime = performance.now();

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': key,
                        'X-User-Id': 'hoangduy'
                    },
                    body: JSON.stringify({ question: text })
                });

                const duration = Math.round(performance.now() - startTime);
                const data = await response.json();
                typingBubble.remove();

                const botBubble = document.createElement('div');
                botBubble.className = 'flex items-start gap-3 max-w-[88%]';

                if (response.ok) {
                    botBubble.innerHTML = `
                        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shrink-0 shadow-md ring-1 ring-white/10">
                            <i data-lucide="sparkles" class="w-4 h-4 text-white"></i>
                        </div>
                        <div class="bg-slate-800/90 border border-slate-700/80 rounded-2xl rounded-tl-sm p-4 shadow-sm text-sm text-slate-200 leading-relaxed">
                            <div>${formatMessageContent(data.answer)}</div>
                            <div class="mt-3 pt-2.5 border-t border-slate-700/60 flex flex-wrap gap-2 text-[11px] font-mono text-slate-400">
                                <span class="bg-slate-900/70 px-2 py-0.5 rounded-md border border-slate-700/50 flex items-center gap-1">⚡ ${duration}ms</span>
                                <span class="bg-slate-900/70 px-2 py-0.5 rounded-md border border-slate-700/50 flex items-center gap-1">📜 Lịch sử: ${data.history_length}</span>
                                <span class="bg-slate-900/70 px-2 py-0.5 rounded-md border border-slate-700/50 flex items-center gap-1">🪙 In: ${data.tokens.in} / Out: ${data.tokens.out}</span>
                                <span class="bg-slate-900/70 px-2 py-0.5 rounded-md border border-slate-700/50 text-emerald-400 font-semibold">💰 $${data.cost_usd.toFixed(6)}</span>
                            </div>
                        </div>
                    `;
                } else {
                    botBubble.innerHTML = `
                        <div class="w-8 h-8 rounded-xl bg-rose-600 flex items-center justify-center shrink-0 shadow-md">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-white"></i>
                        </div>
                        <div class="bg-rose-950/40 border border-rose-800/60 rounded-2xl rounded-tl-sm p-4 text-sm text-rose-200 shadow-sm">
                            <div class="font-semibold text-rose-300">Lỗi HTTP ${response.status}</div>
                            <p class="mt-1">${escapeHtml(data.detail || 'Không thể xử lý yêu cầu.')}</p>
                        </div>
                    `;
                }
                chatFeed.appendChild(botBubble);
            } catch (err) {
                typingBubble.remove();
                const errBubble = document.createElement('div');
                errBubble.className = 'flex items-start gap-3 max-w-[88%]';
                errBubble.innerHTML = `
                    <div class="w-8 h-8 rounded-xl bg-rose-600 flex items-center justify-center shrink-0 shadow-md">
                        <i data-lucide="wifi-off" class="w-4 h-4 text-white"></i>
                    </div>
                    <div class="bg-rose-950/40 border border-rose-800/60 rounded-2xl rounded-tl-sm p-4 text-sm text-rose-200">
                        Không thể kết nối đến máy chủ. Kiểm tra kết nối mạng của bạn.
                    </div>
                `;
                chatFeed.appendChild(errBubble);
            } finally {
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
                chatFeed.scrollTop = chatFeed.scrollHeight;
                lucide.createIcons();
            }
        }

        function escapeHtml(string) {
            return String(string).replace(/[&<>"']/g, function (s) {
                return {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#39;'
                }[s];
            });
        }

        fetchSystemStatus();
        setInterval(fetchSystemStatus, 10000);
    </script>
</body>
</html>
"""
