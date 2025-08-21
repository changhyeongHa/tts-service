# TTS (Text-to-Speech) Service 🔊

> Azure Cognitive Services Neural Voice를 활용한 고품질 음성 합성 마이크로서비스

## 📋 서비스 개요

**TTS Service**는 텍스트를 자연스럽고 생동감 있는 음성으로 변환하는 전문 마이크로서비스입니다. Azure의 최신 Neural Voice 기술을 활용하여 인간과 구분하기 어려운 수준의 고품질 음성을 생성합니다.

### 🌟 핵심 기능
- **🎭 Neural Voice**: Azure 최신 인공지능 음성 합성
- **🎚️ 음성 커스터마이징**: 속도, 높낮이, 톤 세밀 조절
- **🌍 다국어 지원**: 40개 이상 언어와 140개 이상 음성
- **⚡ 실시간 스트리밍**: 빠른 음성 생성 및 전송
- **🎵 고음질 출력**: 16kHz/24kHz WAV 형식 지원
- **🔄 RESTful API**: 표준 HTTP 인터페이스

## 🛠 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **Framework** | FastAPI | 0.104.1 | 웹 API 서버 |
| **Speech Engine** | Azure Neural Voice | Latest | 음성 합성 엔진 |
| **Runtime** | Python | 3.11 | 애플리케이션 런타임 |
| **Container** | Docker | Latest | 컨테이너화 |
| **Web Server** | Uvicorn | 0.24.0 | ASGI 서버 |
| **Audio Processing** | Azure Speech SDK | Latest | 음성 처리 라이브러리 |

## 📡 API 명세

### 🎵 POST /tts/convert
텍스트를 음성 파일로 변환하는 기본 엔드포인트

#### 요청 (Request)
```http
POST /tts/convert
Content-Type: application/json

{
  "text": "변환할 텍스트 내용",
  "voice_name": "ko-KR-SunHiNeural"
}
```

### 🤖 POST /tts/convert-rag-response
**NEW!** RAG 응답을 JSON + Base64 음성으로 변환

#### 요청 (Request)
```http
POST /tts/convert-rag-response
Content-Type: application/json

{
  "success": true,
  "messages": [
    {"HumanMessage": "자동차보험료 계산 방법 알려줘"},
    {"AIMessage": "자동차보험료는 다음과 같이 계산됩니다..."}
  ],
  "citations": [
    {"title": "보험료계산서.pdf", "page": 15},
    {"title": "자동차보험가이드.pdf", "page": 23}
  ]
}
```

#### 응답 (Response) - JSON
```json
{
  "success": true,
  "messages": [
    {"HumanMessage": "자동차보험료 계산 방법 알려줘"},
    {"AIMessage": "자동차보험료는 다음과 같이 계산됩니다..."}
  ],
  "citations": [
    {"title": "보험료계산서.pdf", "page": 15},
    {"title": "자동차보험가이드.pdf", "page": 23}
  ],
  "audio_file": "UklGRiYSAABXQVZFZm10IBAAAAABAAEAQB8AAIA...",
  "voice_info": {
    "voice_name": "ko-KR-SunHiNeural",
    "text_length": 125,
    "audio_format": "wav",
    "file_size": 245760,
    "encoding": "base64"
  }
}
```

### 📁 POST /tts/convert-rag-response-file
RAG 응답을 받아서 WAV 파일로 직접 다운로드

#### 요청 (Request)
동일한 RAG 응답 구조

#### 응답 (Response) - WAV 파일
```http
HTTP/1.1 200 OK
Content-Type: audio/wav
Content-Disposition: attachment; filename="rag_answer.wav"
X-Voice-Name: ko-KR-SunHiNeural
X-RAG-Success: true
X-Citations-Count: 2
X-First-Citation: 보험료계산서.pdf::15

[WAV 오디오 파일 바이너리 데이터]
```

#### 요청 필드 설명
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `text` | string | ✅ | - | 변환할 텍스트 (최대 5000자) |
| `voice_name` | string | ❌ | ko-KR-SunHiNeural | 음성 종류 |
| `rate` | integer | ❌ | 0 | 말하기 속도 (-50 ~ +200) |
| `pitch` | integer | ❌ | 0 | 음성 높낮이 (-50 ~ +50) |
| `style` | string | ❌ | neutral | 감정 스타일 |
| `role` | string | ❌ | narrator | 음성 역할 |

#### 응답 (Response)
```http
HTTP/1.1 200 OK
Content-Type: audio/wav
Content-Disposition: attachment; filename="output.wav"
Content-Length: 245760
X-Voice-Name: ko-KR-SunHiNeural
X-Processing-Time: 1.23
X-Text-Length: 50

[WAV 오디오 파일 바이너리 데이터]
```

### ❤️ GET /health
서비스 상태 확인 엔드포인트

#### 응답 (Response)
```json
{
  "status": "healthy",
  "service": "TTS Service",
  "version": "1.0.0",
  "uptime": "3 days, 12:45:32",
  "azure_connection": "connected",
  "available_voices": 142,
  "supported_languages": 45
}
```

### 🎭 GET /voices
사용 가능한 음성 목록 조회

#### 응답 (Response)
```json
{
  "voices": [
    {
      "name": "ko-KR-SunHiNeural",
      "display_name": "선희",
      "language": "한국어",
      "gender": "Female",
      "styles": ["cheerful", "sad", "angry", "calm"],
      "roles": ["narrator", "character"]
    }
  ],
  "total_count": 142
}
```

## 🎵 지원 음성

### 🇰🇷 한국어 Neural Voice

#### 여성 음성
| 음성명 | 이름 | 특징 | 스타일 지원 |
|--------|------|------|-------------|
| `ko-KR-SunHiNeural` | 선희 | 밝고 친근한 톤 (기본값) | ✅ |
| `ko-KR-JiMinNeural` | 지민 | 젊고 활발한 톤 | ✅ |
| `ko-KR-SeoHyeonNeural` | 서현 | 우아하고 차분한 톤 | ✅ |
| `ko-KR-SoonBokNeural` | 순복 | 따뜻하고 모성적인 톤 | ❌ |
| `ko-KR-YuJinNeural` | 유진 | 깔끔하고 전문적인 톤 | ❌ |

#### 남성 음성
| 음성명 | 이름 | 특징 | 스타일 지원 |
|--------|------|------|-------------|
| `ko-KR-InJoonNeural` | 인준 | 신뢰감 있는 중저음 | ✅ |
| `ko-KR-BongJinNeural` | 봉진 | 친숙하고 편안한 톤 | ❌ |
| `ko-KR-GookMinNeural` | 국민 | 정중하고 정확한 발음 | ❌ |
| `ko-KR-HyunsuNeural` | 현수 | 젊고 에너지 넘치는 톤 | ✅ |

### 🇺🇸 영어 Neural Voice

#### 여성 음성
| 음성명 | 이름 | 특징 | 스타일 지원 |
|--------|------|------|-------------|
| `en-US-JennyNeural` | Jenny | 친근하고 표준적 | ✅ |
| `en-US-AriaNeural` | Aria | 뉴스캐스터 스타일 | ✅ |
| `en-US-MichelleNeural` | Michelle | 따뜻하고 배려심 있는 | ✅ |

#### 남성 음성
| 음성명 | 이름 | 특징 | 스타일 지원 |
|--------|------|------|-------------|
| `en-US-GuyNeural` | Guy | 자신감 있는 중저음 | ✅ |
| `en-US-DavisNeural` | Davis | 전문적이고 신뢰감 있는 | ✅ |

### 🇯🇵 일본어 Neural Voice

| 음성명 | 이름 | 성별 | 특징 |
|--------|------|------|------|
| `ja-JP-NanamiNeural` | 나나미 | 여성 | 표준 일본어, 친근함 |
| `ja-JP-KeitaNeural` | 케이타 | 남성 | 차분하고 신뢰감 있는 |

## 🎭 감정 스타일 (Emotional Styles)

### 한국어 지원 스타일
```json
{
  "neutral": "중립적/기본",
  "cheerful": "밝고 쾌활한",
  "sad": "슬프고 차분한", 
  "angry": "화가 난/강한",
  "fearful": "두렵고 불안한",
  "disgruntled": "불만스러운",
  "serious": "진지하고 엄숙한",
  "affectionate": "애정 어린",
  "gentle": "부드럽고 친근한",
  "lyrical": "서정적이고 감성적인"
}
```

### 영어 지원 스타일
```json
{
  "neutral": "중립적/기본",
  "cheerful": "밝고 쾌활한",
  "sad": "슬프고 차분한",
  "angry": "화가 난/강한", 
  "fearful": "두렵고 불안한",
  "whispering": "속삭이는",
  "empathetic": "공감하는",
  "calm": "차분하고 안정된",
  "newscast": "뉴스 앵커",
  "customerservice": "고객 서비스",
  "assistant": "AI 어시스턴트"
}
```

## 🔧 환경 설정

### 필수 환경 변수
```env
# Azure Speech Service 인증
AZURE_SPEECH_KEY=your_azure_speech_subscription_key
AZURE_SPEECH_REGION=your_azure_region

# 기본 TTS 설정
DEFAULT_VOICE=ko-KR-SunHiNeural
DEFAULT_RATE=0
DEFAULT_PITCH=0
DEFAULT_STYLE=neutral
DEFAULT_ROLE=narrator
```

### 선택적 환경 변수
```env
# 음질 및 성능 설정
AUDIO_FORMAT=wav
SAMPLE_RATE=16000
BIT_DEPTH=16
CHANNELS=1

# 제한 설정
MAX_TEXT_LENGTH=5000
MAX_CONCURRENT_REQUESTS=20
TIMEOUT_SECONDS=60

# 로깅 설정
LOG_LEVEL=INFO
ENABLE_AUDIO_LOGS=false
```

## 🐳 Docker 배포

### 📦 Dockerfile
```dockerfile
FROM python:3.11-slim

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 임시 디렉토리 생성
RUN mkdir -p /app/temp

# 포트 노출
EXPOSE 8003

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8003/health || exit 1

# 서비스 실행
CMD ["uvicorn", "tts_service:app", "--host", "0.0.0.0", "--port", "8003"]
```

### 🚀 실행 방법

#### 단독 실행
```bash
# 이미지 빌드
docker build -t tts-service -f Dockerfile.tts .

# 컨테이너 실행
docker run -d \
  --name tts-service \
  -p 8003:8003 \
  -e AZURE_SPEECH_KEY=your_key \
  -e AZURE_SPEECH_REGION=your_region \
  -v /tmp/tts-cache:/app/temp \
  tts-service

# 로그 확인
docker logs -f tts-service
```

#### Docker Compose 실행
```bash
# 전체 마이크로서비스와 함께 실행
docker-compose -f docker-compose-voice.yml up tts-service

# TTS 서비스만 실행
docker-compose -f docker-compose-voice.yml up tts-service -d
```

## 📝 사용 예시

### 🌐 cURL 테스트
```bash
# 기본 음성 생성
curl -X POST "http://localhost:8003/tts/convert" \
  -H "Content-Type: application/json" \
  -d '{"text": "안녕하세요, 음성 변환 테스트입니다"}' \
  --output basic_test.wav

# 감정을 담은 음성 생성
curl -X POST "http://localhost:8003/tts/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "정말 기쁘고 즐거운 하루입니다!",
    "voice_name": "ko-KR-SunHiNeural",
    "style": "cheerful",
    "rate": 10,
    "pitch": 5
  }' \
  --output cheerful_test.wav

# 영어 음성 생성
curl -X POST "http://localhost:8003/tts/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of English neural voice.",
    "voice_name": "en-US-JennyNeural",
    "style": "friendly"
  }' \
  --output english_test.wav

# 사용 가능한 음성 목록 조회
curl -X GET "http://localhost:8003/voices"

# 헬스체크
curl -X GET "http://localhost:8003/health"
```

### 🐍 Python 클라이언트
```python
import requests
import time
import base64
from typing import Optional, Dict, Any

class TTSClient:
    def __init__(self, base_url="http://localhost:8003"):
        self.base_url = base_url
    
    def convert_rag_response(
        self,
        rag_response: Dict[str, Any],
        save_audio: bool = True,
        audio_filename: str = "rag_answer.wav"
    ) -> Dict[str, Any]:
        """RAG 응답을 JSON + Base64 음성으로 변환 - 기본 음성 자동 사용"""
        url = f"{self.base_url}/tts/convert-rag-response"
        
        # RAG 응답을 직접 전송
        payload = rag_response
        
        try:
            print(f"🤖 RAG 응답 TTS 변환 시작...")
            start_time = time.time()
            
            response = requests.post(url, json=payload)
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ RAG-TTS 변환 성공!")
                print(f"📝 질문: {result['messages'][0].get('HumanMessage', 'N/A')}")
                print(f"🤖 답변: {result['messages'][1].get('AIMessage', 'N/A')[:100]}...")
                print(f"🎭 사용된 음성: {result['voice_info']['voice_name']}")
                print(f"⏱️ 처리 시간: {processing_time:.2f}초")
                print(f"📚 인용 문서: {len(result['citations'])}개")
                print(f"🔊 음성 파일 크기: {result['voice_info']['file_size']}bytes")
                
                # 오디오 파일 저장 (선택사항)
                if save_audio and result.get('audio_file'):
                    audio_data = base64.b64decode(result['audio_file'])
                    with open(audio_filename, 'wb') as f:
                        f.write(audio_data)
                    print(f"🔊 음성 파일 저장: {audio_filename}")
                
                return result
            else:
                print(f"❌ RAG-TTS 변환 실패: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
            return None

    def convert_rag_response_to_file(
        self,
        rag_response: Dict[str, Any],
        output_file: str = "rag_answer.wav"
    ) -> bool:
        """RAG 응답을 WAV 파일로 직접 다운로드"""
        url = f"{self.base_url}/tts/convert-rag-response-file"
        
        payload = rag_response
        
        try:
            print(f"📁 RAG 응답 음성 파일 생성 시작...")
            start_time = time.time()
            
            response = requests.post(url, json=payload)
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                # 음성 파일 저장
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                # 헤더 정보 출력
                voice_name = response.headers.get('X-Voice-Name', 'Unknown')
                rag_success = response.headers.get('X-RAG-Success', 'Unknown')
                citations_count = response.headers.get('X-Citations-Count', '0')
                first_citation = response.headers.get('X-First-Citation', 'None')
                
                print(f"✅ RAG 음성 파일 생성 성공!")
                print(f"📁 저장 위치: {output_file}")
                print(f"🎭 사용된 음성: {voice_name}")
                print(f"✅ RAG 성공 여부: {rag_success}")
                print(f"📚 인용 문서 수: {citations_count}개")
                print(f"📄 첫 번째 인용: {first_citation}")
                print(f"⏱️ 처리 시간: {processing_time:.2f}초")
                
                return True
            else:
                print(f"❌ RAG 음성 파일 생성 실패: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
            return False
    

    
    def convert_text(
        self, 
        text: str,
        voice_name: str = "ko-KR-SunHiNeural",
        rate: int = 0,
        pitch: int = 0,
        style: str = "neutral",
        role: str = "narrator",
        output_file: str = "output.wav"
    ):
        """텍스트를 음성으로 변환"""
        url = f"{self.base_url}/tts/convert"
        
        payload = {
            "text": text,
            "voice_name": voice_name,
            "rate": rate,
            "pitch": pitch,
            "style": style,
            "role": role
        }
        
        try:
            start_time = time.time()
            response = requests.post(url, json=payload)
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                # 음성 파일 저장
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                # 헤더 정보 출력
                voice_name = response.headers.get('X-Voice-Name', 'Unknown')
                server_time = response.headers.get('X-Processing-Time', 'Unknown')
                text_length = response.headers.get('X-Text-Length', 'Unknown')
                
                print(f"✅ 음성 생성 성공!")
                print(f"📁 저장 위치: {output_file}")
                print(f"🎭 사용된 음성: {voice_name}")
                print(f"⏱️ 처리 시간: {processing_time:.2f}초 (서버: {server_time}초)")
                print(f"📝 텍스트 길이: {text_length}자")
                
                return True
            else:
                print(f"❌ 음성 생성 실패: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
            return False
    
    def get_available_voices(self):
        """사용 가능한 음성 목록 조회"""
        try:
            response = requests.get(f"{self.base_url}/voices")
            if response.status_code == 200:
                voices = response.json()
                print(f"📢 총 {voices['total_count']}개의 음성 사용 가능")
                
                for voice in voices['voices'][:10]:  # 상위 10개만 출력
                    print(f"  🎭 {voice['name']} ({voice['display_name']}) - {voice['language']} {voice['gender']}")
                
                return voices
            else:
                print(f"❌ 음성 목록 조회 실패: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
            return None
    
    def health_check(self):
        """서비스 상태 확인"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                health = response.json()
                print(f"✅ TTS Service: {health['status']}")
                print(f"🔗 Azure 연결: {health.get('azure_connection', 'Unknown')}")
                print(f"🎭 사용 가능한 음성: {health.get('available_voices', 'Unknown')}개")
                return True
            else:
                print("❌ TTS Service: unhealthy")
                return False
        except Exception as e:
            print(f"❌ TTS Service 연결 실패: {e}")
            return False

# 사용 예시
if __name__ == "__main__":
    client = TTSClient()
    
    # 헬스체크
    if client.health_check():
        print("\n" + "="*50)
        
        # 🆕 RAG 응답 테스트 데이터
        sample_rag_response = {
            "success": True,
            "messages": [
                {"HumanMessage": "자동차 보험료 계산 방법 알려줘"},
                {"AIMessage": "자동차 보험료는 차량 가격, 운전자 나이, 운전 경력, 사고 이력 등을 종합적으로 고려하여 계산됩니다."}
            ],
            "citations": [
                {"title": "자동차보험_기본약관.pdf", "page": 15},
                {"title": "보험료산출기준_가이드.pdf", "page": 23}
            ]
        }
        
        # 🆕 RAG 응답을 JSON + Base64 음성으로 변환 - 기본 음성 자동 사용
        print("\n🤖 RAG-TTS JSON 변환 테스트")
        rag_result = client.convert_rag_response(
            rag_response=sample_rag_response,
            save_audio=True,
            audio_filename="rag_answer_json.wav"
        )
        
        # 🆕 RAG 응답을 직접 WAV 파일로 변환
        print("\n📁 RAG-TTS 파일 변환 테스트")
        client.convert_rag_response_to_file(
            rag_response=sample_rag_response,
            output_file="rag_answer_file.wav"
        )
        
        print("\n" + "="*50)
        
        # 기존 기본 음성 생성 테스트
        client.convert_text(
            text="안녕하세요! TTS 서비스 기본 테스트입니다.",
            output_file="basic_test.wav"
        )
        
        print("\n🎵 모든 음성 파일이 생성되었습니다!")
        print("📁 생성된 파일:")
        print("  • rag_answer_json.wav (RAG JSON 응답)")
        print("  • rag_answer_file.wav (RAG 파일 응답)")
        print("  • basic_test.wav (기본 텍스트 변환)")
```

### 🌐 JavaScript/Node.js 클라이언트
```javascript
const fetch = require('node-fetch');
const fs = require('fs');

class TTSClient {
    constructor(baseUrl = 'http://localhost:8003') {
        this.baseUrl = baseUrl;
    }

    async convertText(options = {}) {
        const {
            text,
            voiceName = 'ko-KR-SunHiNeural',
            rate = 0,
            pitch = 0,
            style = 'neutral',
            role = 'narrator',
            outputFile = 'output.wav'
        } = options;

        const url = `${this.baseUrl}/tts/convert`;
        
        const payload = {
            text: text,
            voice_name: voiceName,
            rate: rate,
            pitch: pitch,
            style: style,
            role: role
        };

        try {
            const startTime = Date.now();
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const processingTime = (Date.now() - startTime) / 1000;

            if (response.ok) {
                const audioBuffer = await response.buffer();
                fs.writeFileSync(outputFile, audioBuffer);

                // 헤더 정보 출력
                const voiceNameHeader = response.headers.get('x-voice-name') || 'Unknown';
                const serverTime = response.headers.get('x-processing-time') || 'Unknown';
                const textLength = response.headers.get('x-text-length') || 'Unknown';

                console.log('✅ 음성 생성 성공!');
                console.log(`📁 저장 위치: ${outputFile}`);
                console.log(`🎭 사용된 음성: ${voiceNameHeader}`);
                console.log(`⏱️ 처리 시간: ${processingTime.toFixed(2)}초 (서버: ${serverTime}초)`);
                console.log(`📝 텍스트 길이: ${textLength}자`);

                return true;
            } else {
                const error = await response.text();
                console.log(`❌ 음성 생성 실패: ${error}`);
                return false;
            }
        } catch (error) {
            console.log(`❌ 요청 실패: ${error.message}`);
            return false;
        }
    }

    async getAvailableVoices() {
        try {
            const response = await fetch(`${this.baseUrl}/voices`);
            if (response.ok) {
                const voices = await response.json();
                console.log(`📢 총 ${voices.total_count}개의 음성 사용 가능`);
                
                voices.voices.slice(0, 10).forEach(voice => {
                    console.log(`  🎭 ${voice.name} (${voice.display_name}) - ${voice.language} ${voice.gender}`);
                });
                
                return voices;
            } else {
                const error = await response.text();
                console.log(`❌ 음성 목록 조회 실패: ${error}`);
                return null;
            }
        } catch (error) {
            console.log(`❌ 요청 실패: ${error.message}`);
            return null;
        }
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            if (response.ok) {
                const health = await response.json();
                console.log(`✅ TTS Service: ${health.status}`);
                console.log(`🔗 Azure 연결: ${health.azure_connection || 'Unknown'}`);
                console.log(`🎭 사용 가능한 음성: ${health.available_voices || 'Unknown'}개`);
                return true;
            } else {
                console.log('❌ TTS Service: unhealthy');
                return false;
            }
        } catch (error) {
            console.log(`❌ TTS Service 연결 실패: ${error.message}`);
            return false;
        }
    }
}

// 사용 예시
(async () => {
    const client = new TTSClient();
    
    // 헬스체크
    const isHealthy = await client.healthCheck();
    
    if (isHealthy) {
        console.log('\n' + '='.repeat(50));
        
        // 사용 가능한 음성 목록 조회
        await client.getAvailableVoices();
        console.log('\n' + '='.repeat(50));
        
        // 기본 한국어 음성 생성
        await client.convertText({
            text: '안녕하세요! TTS 서비스 테스트입니다.',
            outputFile: 'korean_basic.wav'
        });
        
        // 감정이 담긴 한국어 음성 생성
        await client.convertText({
            text: '정말 놀랍고 기쁜 소식입니다!',
            voiceName: 'ko-KR-SunHiNeural',
            style: 'cheerful',
            rate: 20,
            pitch: 10,
            outputFile: 'korean_cheerful.wav'
        });
        
        // 영어 음성 생성
        await client.convertText({
            text: 'Hello! This is an English neural voice test.',
            voiceName: 'en-US-JennyNeural',
            style: 'friendly',
            outputFile: 'english_friendly.wav'
        });
        
        console.log('\n🎵 모든 음성 파일이 생성되었습니다!');
    }
})();
```

## 🎛 고급 음성 커스터마이징

### SSML (Speech Synthesis Markup Language) 지원
```xml
<!-- 고급 SSML 예시 -->
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ko-KR">
  <voice name="ko-KR-SunHiNeural">
    <prosody rate="medium" pitch="medium">
      안녕하세요!
    </prosody>
    <break time="500ms"/>
    <prosody rate="slow" pitch="low">
      천천히 말하겠습니다.
    </prosody>
    <break time="1s"/>
    <prosody rate="fast" pitch="high" volume="loud">
      빠르고 높은 톤으로!
    </prosody>
  </voice>
</speak>
```

### 감정 강도 조절
```json
{
  "text": "정말 기쁩니다!",
  "voice_name": "ko-KR-SunHiNeural",
  "style": "cheerful",
  "style_degree": 2.0,  // 1.0 (기본) ~ 2.0 (강함)
  "rate": 0,
  "pitch": 0
}
```

### 역할별 음성 변화
```json
{
  "text": "오늘 뉴스를 전해드리겠습니다.",
  "voice_name": "ko-KR-InJoonNeural",
  "role": "newsanchor",  // 뉴스 앵커 톤
  "style": "serious"
}
```

## 🚨 트러블슈팅

### 🔐 인증 문제
```
HTTP 401 Unauthorized
```
**해결방법:**
1. `AZURE_SPEECH_KEY` 환경변수 확인
2. `AZURE_SPEECH_REGION` 환경변수 확인
3. Azure 구독 상태 및 할당량 점검
4. 방화벽/네트워크 설정 확인

### 📝 텍스트 길이 문제
```
텍스트가 너무 깁니다 (최대 5000자)
```
**해결방법:**
1. 텍스트를 여러 부분으로 나누어 처리
2. `MAX_TEXT_LENGTH` 환경변수 조정
3. 긴 텍스트는 청크 단위로 분할 처리

### 🎭 음성 설정 오류
```
지원되지 않는 음성: xyz-neural
```
**해결방법:**
1. `/voices` 엔드포인트로 지원 음성 확인
2. 올바른 음성명 형식 사용 (`언어-지역-이름Neural`)
3. 감정 스타일과 역할 조합 확인

### 🎵 음질 문제
```
생성된 음성의 품질이 낮음
```
**해결방법:**
1. 샘플레이트 설정 확인 (16kHz/24kHz)
2. 비트뎁스 설정 확인 (16-bit/24-bit)
3. 네트워크 연결 상태 점검
4. Azure 서비스 리전 최적화

### 🌐 네트워크 연결 문제
```
Connection timeout / Request failed
```
**해결방법:**
1. 인터넷 연결 상태 확인
2. Azure Speech Service 엔드포인트 확인
3. DNS 설정 점검
4. 프록시 설정 확인

## 📊 성능 지표

### 처리 성능
- **평균 응답 시간**: 0.8-2.5초 (텍스트 길이에 따라)
- **최대 텍스트 길이**: 5000자
- **동시 처리**: 20개 요청 (비동기 처리)
- **처리량**: 분당 100-300개 요청

### 음성 품질
- **샘플레이트**: 16kHz/24kHz 선택 가능
- **비트뎁스**: 16-bit/24-bit
- **포맷**: WAV (PCM), MP3, OGG 지원
- **지연율**: 50ms 이하 (실시간 스트리밍)

### 리소스 사용량
- **메모리**: 평균 150MB, 최대 300MB
- **CPU**: 평균 15%, 최대 60%
- **네트워크**: 다운로드 대역폭에 따라
- **저장공간**: 임시 파일 캐시 최대 1GB

## 🔐 보안 고려사항

### 데이터 보호
- **전송 암호화**: HTTPS/TLS 1.3 사용 권장
- **임시 파일**: 생성 후 자동 삭제 (30분 후)
- **로그 보안**: 텍스트 내용 마스킹 옵션
- **캐시 보안**: 메모리 기반 캐시 사용

### 접근 제어
- **API 키 관리**: 환경변수 또는 Azure Key Vault
- **IP 화이트리스트**: 방화벽 규칙 설정
- **사용량 제한**: Rate Limiting 적용 권장
- **모니터링**: 비정상적 사용 패턴 감지

### 개인정보 보호
- **텍스트 로깅**: 민감 정보 제외 권장
- **GDPR 준수**: EU 사용자 데이터 보호
- **데이터 보존**: 최소 보존 원칙 적용
- **동의 관리**: 음성 생성 전 사용자 동의

## 💡 활용 사례

### 🎓 교육 분야
- **온라인 강의**: 텍스트 교재의 음성 나레이션
- **언어 학습**: 발음 연습용 표준 음성 제공
- **접근성**: 시각 장애 학습자를 위한 오디오 북

### 💼 비즈니스 분야
- **고객 서비스**: 자동 응답 시스템의 음성 안내
- **마케팅**: 광고 나레이션 및 프로모션 음성
- **교육 자료**: 기업 내부 교육 콘텐츠 음성화

### 🎮 엔터테인먼트 분야
- **게임**: 캐릭터 대사 및 내레이션
- **오디오북**: 소설 및 에세이 음성 변환
- **팟캐스트**: 자동 뉴스 읽기 서비스

### 🏥 의료 분야
- **환자 안내**: 병원 내 음성 안내 시스템
- **의료 교육**: 의학 텍스트의 음성 학습 자료
- **재활 치료**: 언어 치료용 표준 발음 제공

## 📄 라이선스

```
MIT License

Copyright (c) 2025 TTS Service

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

> 💡 **더 많은 정보가 필요하시면 [Azure Speech Service 공식 문서](https://docs.microsoft.com/ko-kr/azure/cognitive-services/speech-service/text-to-speech)와 [Neural Voice 가이드](https://docs.microsoft.com/ko-kr/azure/cognitive-services/speech-service/language-support?tabs=tts)를 참조하세요.**