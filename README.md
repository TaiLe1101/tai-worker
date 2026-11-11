# TAI TTS server

Viết lại theo worker Colab: làm sạch văn bản → Gemini `gemini-2.5-flash` → deep-translator → Google Translate endpoint → Edge TTS `vi-VN-HoaiMyNeural`. Khi cả ba dịch vụ dịch thất bại, đọc nguyên văn như mẫu Colab. TTS thử tối đa 4 lần với thời gian chờ tăng dần.

Chỉ hỗ trợ `target_lang: "vi"`. API trả MP3 và header `X-Translated-Text` được URL encode.

## Chạy trên Windows

Từ thư mục gốc dự án:

```powershell
.\.venv\Scripts\python.exe -m pip install -r tts-server/requirements.txt
Copy-Item tts-server/.env.example tts-server/.env
# Sửa GEMINI_API_KEY trong tts-server/.env trước khi chạy.
.\.venv\Scripts\python.exe -m uvicorn app:app --app-dir tts-server --env-file tts-server/.env --host 127.0.0.1 --port 8000
```

Nếu `.env` đã tồn tại, dùng file đó thay vì chép đè. Không có Gemini key thì server vẫn chạy bằng hai dịch vụ dịch dự phòng. Dùng key mới thay cho key đã chia sẻ trong đoạn Colab.

```powershell
Invoke-WebRequest -Method Post -Uri http://127.0.0.1:8000/process-tts -ContentType application/json -Body '{"text":"Deploy the cache service.","target_lang":"vi"}' -OutFile voice.mp3
```

Mở `http://127.0.0.1:8000/docs` để thử API. `GET /health` kiểm tra server còn chạy, không gọi dịch vụ ngoài.

`WORKER_API_KEY` mặc định trống để gọi giống Colab. Nếu đặt giá trị, mọi request tới `/health` và `/process-tts` cần header `Authorization: Bearer <WORKER_API_KEY>`. Gemini key chỉ đặt trên server.

## Kết nối client

Server mở tại `http://127.0.0.1:8000` khi chạy bằng lệnh Python ở trên. Nếu client có timeout 35 giây, cần tăng để chờ đủ các lần thử TTS khi dịch vụ chậm.

Cloudflare tunnel chỉ cần khi muốn cấp URL công khai cho server chạy cục bộ.
