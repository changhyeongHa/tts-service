@echo off
echo 🔊 TTS Service Docker 이미지 빌드 중...

REM 기존 이미지 삭제 (선택사항)
docker rmi tts-service:latest 2>nul

REM 이미지 빌드
docker build -t tts-service:latest .

if %errorlevel% equ 0 (
    echo ✅ TTS Service 이미지 빌드 완료!
    echo 이미지 크기:
    docker images tts-service:latest
) else (
    echo ❌ TTS Service 이미지 빌드 실패!
    exit /b 1
)

pause
