# TAI TTS Worker

FastAPI worker dịch nội dung sang tiếng Việt và tạo file MP3 bằng Edge TTS.

## Cấu trúc

```text
app/
├── api/          # HTTP routes và dependency wiring
├── core/         # Cấu hình, xác thực API key
├── schemas/      # Pydantic request/response models
├── services/     # Translation và TTS business logic
├── utils/        # Hàm tiện ích thuần
└── main.py       # Application factory và lifecycle
```

## Chạy local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Đặt một chuỗi ngẫu nhiên đủ dài vào `WORKER_API_KEY` trong `.env`. Mọi API
worker đều nhận key trực tiếp qua header `X-API-Key`; không dùng Bearer token.

```powershell
curl.exe http://127.0.0.1:8000/health `
  -H "X-API-Key: <WORKER_API_KEY>"

curl.exe http://127.0.0.1:8000/process-tts `
  -X POST `
  -H "Content-Type: application/json" `
  -H "X-API-Key: <WORKER_API_KEY>" `
  -d '{"text":"Hello world","target_lang":"vi"}' `
  --output speech.mp3
```

Swagger UI có tại `http://127.0.0.1:8000/docs`; nút **Authorize** sẽ yêu cầu
giá trị `X-API-Key`.
