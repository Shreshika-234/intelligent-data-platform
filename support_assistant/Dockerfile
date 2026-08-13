FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

# docker build -t support-assistant .
# docker run -d \
#   --name support-assistant-container \
#   --env-file .env \
#   -p 7860:7860 \
#   v "$(pwd)/chroma_db:/app/chroma_db" \
#   support-assistant