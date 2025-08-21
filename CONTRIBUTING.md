# Contributing to TTS Service 🤝

TTS Service에 기여해주셔서 감사합니다! 이 가이드는 프로젝트에 기여하는 방법을 설명합니다.

## 📋 기여 방식

### 🐛 버그 리포트
- GitHub Issues를 통해 버그를 신고해주세요
- 오디오 품질 문제, 음성 합성 오류 등 구체적으로 설명
- 사용한 텍스트, 음성 설정, 환경 정보 포함

### 💡 기능 제안
- 새로운 음성 지원, 감정 스타일 추가 등 제안
- SSML 기능 확장, 음성 커스터마이징 옵션 제안
- 성능 최적화 아이디어

### 🔧 코드 기여
1. Fork 생성
2. Feature branch 생성: `git checkout -b feature/VoiceEnhancement`
3. 변경사항 커밋: `git commit -m 'Add emotional voice styles'`
4. Branch에 Push: `git push origin feature/VoiceEnhancement`
5. Pull Request 생성

## 🛠 개발 환경 설정

### 필요 조건
- Python 3.11+
- Azure Speech Service 구독
- Docker (선택사항)
- 오디오 테스트를 위한 스피커/헤드폰

### 로컬 설정
```bash
# 저장소 클론
git clone https://github.com/your-username/tts-service.git
cd tts-service

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 시스템 의존성 설치 (Linux/Ubuntu)
sudo apt-get install libasound2-dev

# Python 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 환경변수 설정
cp env.example .env
# .env 파일에 Azure Speech Service 인증 정보 입력

# 개발 서버 실행
uvicorn tts_service:app --reload --port 8003
```

## 🧪 테스트

### 단위 테스트 실행
```bash
pytest tests/ -v
```

### 오디오 품질 테스트
```bash
# 다양한 음성으로 오디오 생성 테스트
python tests/test_voice_quality.py

# 감정 스타일 테스트
python tests/test_emotional_styles.py

# 성능 벤치마크
python tests/benchmark_synthesis.py
```

### 커버리지 테스트
```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

## 🎵 음성 품질 가이드라인

### 음성 테스트 체크리스트
- [ ] 발음 정확성 확인
- [ ] 자연스러운 억양과 리듬
- [ ] 적절한 속도와 볼륨
- [ ] 감정 표현의 적절성
- [ ] 다양한 텍스트 길이에서 일관성

### 새로운 음성 추가시
```python
# 음성 설정 예시
VOICE_CONFIG = {
    "name": "ko-KR-NewVoiceNeural",
    "language": "Korean",
    "gender": "Female",
    "styles": ["neutral", "cheerful", "sad"],
    "roles": ["narrator", "character"],
    "sample_rate": 24000
}
```

### SSML 테스트
```xml
<!-- 복잡한 SSML 예시 테스트 -->
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ko-KR">
  <voice name="ko-KR-SunHiNeural">
    <prosody rate="medium" pitch="+5%">
      안녕하세요!
    </prosody>
    <break time="500ms"/>
    <prosody volume="loud" rate="fast">
      빠르고 큰 소리로!
    </prosody>
  </voice>
</speak>
```

## 📏 코딩 스타일

### Python 스타일 가이드
- PEP 8 준수
- Black 포맷터 사용: `black .`
- isort 사용: `isort .`
- Type hints 사용 권장

### 오디오 관련 코딩 규칙
```python
# 좋은 예시
async def synthesize_text(
    text: str,
    voice_name: str = "ko-KR-SunHiNeural",
    rate: int = 0,
    pitch: int = 0
) -> bytes:
    """텍스트를 음성으로 변환"""
    # 입력 검증
    if not text.strip():
        raise ValueError("Empty text provided")
    
    # 음성 합성 로직
    ...
    
    return audio_data

# 나쁜 예시
def tts(txt, voice):  # 타입 힌트 없음, 불명확한 이름
    return do_synthesis(txt, voice)  # 검증 없음
```

## 📝 커밋 메시지 규칙

### TTS 관련 커밋 타입
- `feat(voice)`: 새로운 음성 추가
- `feat(style)`: 감정 스타일 추가
- `fix(synthesis)`: 음성 합성 버그 수정
- `perf(audio)`: 오디오 처리 성능 개선
- `docs(api)`: API 문서 업데이트

### 예시
```
feat(voice): add ko-KR-HyunsuNeural male voice support

- Add new Korean male neural voice option
- Implement emotional styles for HyunsuNeural
- Update voice selection API documentation
- Add comprehensive voice quality tests

Closes #45
```

## 🏗 Pull Request 가이드라인

### TTS PR 체크리스트
- [ ] 오디오 품질 테스트 통과
- [ ] 새로운 음성/스타일 문서화
- [ ] 성능 영향 분석 완료
- [ ] 다양한 텍스트 길이 테스트
- [ ] 메모리 누수 검사

### 오디오 샘플 첨부
PR에 다음 오디오 샘플을 첨부해주세요:
- 기본 음성 샘플 (30초 이내)
- 새로운 기능 시연 샘플
- Before/After 비교 샘플 (성능 개선시)

## 🎯 성능 기준

### 합성 성능 목표
- **처리 시간**: 1000자당 2초 이내
- **메모리 사용**: 요청당 50MB 이하
- **음질**: 16kHz/24kHz WAV 지원
- **동시 처리**: 20개 요청

### 품질 기준
- **자연스러움**: 평균 4.0/5.0 이상
- **발음 정확도**: 95% 이상
- **감정 표현**: 의도한 감정 90% 전달
- **일관성**: 같은 텍스트 반복시 동일한 품질

## 🔄 릴리스 프로세스

### 음성 모델 버전 관리
- 새로운 음성 추가시 마이너 버전 업
- 기존 음성 개선시 패치 버전 업
- API 변경시 메이저 버전 업

### 호환성 유지
- 기존 음성 이름 변경 금지
- API 파라미터 하위 호환성 유지
- 음성 품질 회귀 방지

## 📞 커뮤니케이션

### 음성 관련 이슈 라벨
- `voice-quality`: 음성 품질 문제
- `new-voice`: 새로운 음성 요청
- `performance`: 성능 관련 이슈
- `ssml`: SSML 기능 관련
- `audio-format`: 오디오 포맷 관련

### 이슈 템플릿
```markdown
## 🎵 음성 관련 이슈
**음성 이름**: ko-KR-SunHiNeural
**텍스트**: "문제가 있는 텍스트"
**설정**: rate=0, pitch=0, style=neutral
**문제**: 발음이 부정확함
**기대 결과**: 정확한 발음
**환경**: Python 3.11, Azure 리전 등
```

## 🎨 UI/UX 가이드라인

### API 응답 설계
```json
{
  "success": true,
  "audio_url": "https://example.com/generated.wav",
  "metadata": {
    "voice_name": "ko-KR-SunHiNeural",
    "text_length": 150,
    "duration": "5.2s",
    "file_size": "245KB"
  }
}
```

### 오류 메시지 가이드
- 사용자 친화적인 메시지
- 해결 방법 제시
- 적절한 HTTP 상태 코드

## 📄 라이선스

기여하신 코드는 [MIT License](LICENSE)에 따라 배포됩니다.

---

TTS Service를 더욱 좋게 만들어주셔서 감사합니다! 🎉🔊
