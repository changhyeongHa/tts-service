@echo off
echo 🔊 TTS Service 실행 중...

REM 기존 컨테이너 정리
docker stop tts-service 2>nul
docker rm tts-service 2>nul

REM 환경변수 파일 경로 (상위 디렉토리)
set ENV_FILE=..\.env

REM 컨테이너 실행
docker run -d ^
  --name tts-service ^
  -p 8003:8003 ^
  --env-file %ENV_FILE% ^
  --restart unless-stopped ^
  tts-service:latest

if %errorlevel% equ 0 (
    echo ✅ TTS Service 시작 완료!
    echo 포트: http://localhost:8003
    echo 헬스체크: http://localhost:8003/health
    echo API 문서: http://localhost:8003/docs
    echo.
    echo 로그 확인: docker logs -f tts-service
    echo 컨테이너 정지: docker stop tts-service
) else (
    echo ❌ TTS Service 시작 실패!
    exit /b 1
)

pause
