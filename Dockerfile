# TTS Service Dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TTS 서비스 파일들 복사
COPY tts_service.py .
COPY tts.py .

# 포트 8003 노출
EXPOSE 8003

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# TTS 서비스 실행
CMD ["uvicorn", "tts_service:app", "--host", "0.0.0.0", "--port", "8003", "--log-level", "info"]
