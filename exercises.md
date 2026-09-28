# Phiếu Phản Ánh — K4 Level 3A, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay các dòng `*Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyễn Hoàng Duy  Mã học viên: 2A202602751

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi deploy lên server/cloud, nếu tôi lỡ quên cấu hình biến `AGENT_API_KEY`:
> - Nếu để mặc định `"changeme"`: App vẫn chạy bình thường. Người ngoài hoặc bot quét có thể dùng luôn key `"changeme"` để gọi `/ask` thoải mái, vừa lộ thông tin vừa làm hao hụt tiền API của tôi mà tôi không hề hay biết.
> - Khi không có mặc định (fail fast): App sập ngay khi vừa bật và báo lỗi thiếu biến. Việc này buộc tôi phải điền đúng key bí mật trước khi app mở ra ngoài Internet, tránh được rủi ro bảo mật và mất tiền oan.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Dòng log thu được:
> ```json
> {"event": "service_started", "level": "info", "timestamp": "2026-09-28T09:11:06.185653+00:00", "service": "day12-agent", "version": "1.0.0"}
> ```
> Hai việc làm được với log JSON:
> 1. **Lọc và tìm kiếm dễ dàng:** Các hệ thống đọc log (như CloudWatch, Datadog) có thể tự lọc theo trường cụ thể (ví dụ tìm theo `level: "error"` hay theo mốc `timestamp`), không phải căng mắt đọc từng dòng text.
> 2. **Tính toán và vẽ biểu đồ chi phí:** Máy có thể tự động bóc tách các trường số như `cost_usd` hay `tokens` để cộng tổng tiền và vẽ dashboard theo dõi, điều mà `print()` text thuần túy không thể làm được.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | ~1050 MB |
| Multi-stage | 271 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Phần dung lượng chênh lệch (gần 800 MB) chủ yếu gồm:
> - **Hệ điều hành và công cụ biên dịch:** Bản 1-stage dùng base image `python:3.11` đầy đủ, chứa cả bộ compiler (gcc, make), C-headers, git, curl và rất nhiều tiện ích Linux không cần thiết khi chạy. Bản multi-stage chuyển sang `python:3.11-slim` chỉ giữ lại môi trường tối thiểu.
> - **Tách biệt lúc build và lúc chạy:** Ở multi-stage, các công cụ phục vụ cài đặt và file cache phát sinh chỉ nằm lại ở stage `builder`. Sang stage `runtime` chỉ copy đúng thư mục gói đã cài (`/install`), không mang theo cache của pip hay file rác trung gian.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> - **Khi sửa `app/main.py`:** Các layer cài thư viện (`pip install`) và tạo môi trường đều được lấy lại từ cache (`CACHED`). Chỉ có layer `COPY app ./app` và các lệnh sau nó phải chạy lại, build chỉ mất 1-2 giây.
> - **Nếu đặt `COPY . .` trước `pip install`:** Sửa bất kỳ dòng code nào cũng làm mất cache, Docker phải tải và cài lại toàn bộ thư viện từ đầu, khiến mỗi lần build mất thêm vài phút.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> - **Chuỗi sự kiện:** Code có lỗ hổng $\rightarrow$ Hacker chạy được lệnh vào container $\rightarrow$ Do chạy bằng `root`, hacker có toàn quyền trong container $\rightarrow$ Hacker lợi dụng lỗi kernel hoặc volume mount để thoát ra chiếm quyền root của máy host.
> - **Lệnh `USER` cắt đứt ở đâu:** Lệnh `USER appuser` ép app chạy bằng user thường. Hacker vào được cũng không có quyền can thiệp hệ thống, bị chặn đứng không thể leo thang đặc quyền ra máy host.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> - **Số request tối đa:** **20 request** trong 2 giây liên tiếp.
> - **Cách đạt được:**
>   - Ở giây thứ 59 của phút trước (ví dụ `10:00:59`), người dùng gửi hết quota 10 request (tính cho phút 10:00).
>   - Sang giây thứ 01 của phút sau (ví dụ `10:01:01`), đồng hồ bước sang phút mới nên bộ đếm tự reset về 0, người dùng gửi tiếp 10 request nữa (tính cho phút 10:01).
>   - Cả 2 lần đều đúng luật đếm theo phút, nhưng thực tế server phải gánh dồn 20 request chỉ trong vòng 2 giây.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> - **Khác nhau:**
>   - **Rate limit:** Giới hạn **tần suất gọi** (số request / phút) để bảo vệ server khỏi nghẽn mạng và chống spam.
>   - **Cost guard:** Giới hạn **tổng chi phí tiền bạc** (USD / tháng) để tránh cạn kiệt ngân sách gọi API LLM.
> - **Rate limit cho qua nhưng Cost guard chặn:** Người dùng hỏi rất thong thả (chỉ 1 request/phút nên rate limit cho qua), nhưng câu hỏi rất dài và ép LLM trả lời hàng chục nghìn token làm hóa đơn tháng vượt quá hạn mức ngân sách $\rightarrow$ Cost guard chặn (lỗi 402).
> - **Cost guard cho qua nhưng Rate limit chặn:** Đầu tháng ngân sách còn nguyên $10 (chưa tiêu đồng nào), nhưng người dùng chạy script bắn liên tiếp 15 request trong 3 giây. Tiền còn nhiều nên cost guard cho qua, nhưng gọi quá dồn dập nên bị rate limit chặn ngay từ request thứ 11 (lỗi 429).

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Thứ tự sự kiện:
> 1. Redis mất kết nối trong 30 giây.
> 2. Do endpoint kiểm tra phụ thuộc vào Redis, cả 3 container agent đều đồng loạt trả về lỗi (503 / unhealthy).
> 3. Hệ thống điều phối (Orchestrator) tưởng process của cả 3 container bị chết (liveness fail) nên lập tức **restart toàn bộ 3 container cùng lúc**.
> 4. Trong suốt 30 giây Redis chết, cả cụm container bị restart liên tục (CrashLoop), hệ thống hoàn toàn sập (100% downtime).
> 5. Đến khi Redis sống lại, các container vẫn đang loay hoay khởi động lại, làm kéo dài thời gian gián đoạn dịch vụ thay vì chỉ tạm ngừng nhận request như khi dùng `/ready`.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> - **Khi dùng Redis (stateless):** `history_length` tăng đều liên tục (0 $\rightarrow$ 2 $\rightarrow$ 4 $\rightarrow$ 6...) vì cả 3 container đều đọc/ghi chung một lịch sử trên Redis.
> - **Nếu dùng dict Python trong RAM:** `history_length` sẽ **nhảy lung tung, không đều và agent bị "mất trí nhớ"**.
>   - Lý do: Load balancer chia request ngẫu nhiên vào 3 container (A, B, C). Mỗi container chỉ giữ bộ nhớ riêng của nó, ví dụ câu 1 vào A (A lưu), câu 2 vào B thì B không biết gì (`history_length = 0`), câu 3 lại vào A thì A mới nhớ lại câu 1 (`history_length = 2`).

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> - **Thông báo lỗi:** Service Redis bị crash với log `/bin/sh: 1: exec: docker-entrypoint.sh: not found` và khi gọi `/ready` bị trả về lỗi `503 Service Unavailable` (`{"status":"not ready","redis":false}`).
> - **Nguyên nhân:** Khi chạy lệnh `railway up`, do chưa chỉ định service nên CLI đã vô tình deploy code app FastAPI đè lên chính service Redis. Service này vẫn giữ lệnh chạy mặc định của Redis (`docker-entrypoint.sh`), nhưng image Python app không có file đó nên bị sập.
> - **Cách sửa:** Tôi xóa service Redis bị lỗi, tạo lại service Redis chuẩn và tạo thêm một service riêng tên là `agent` (`railway add --service agent`). Sau đó cấu hình biến môi trường `REDIS_URL=${{Redis.REDIS_URL}}` cho `agent` và deploy code vào đúng service `agent`. Cả 2 service đều online và `/ready` trả về `200 OK`.
