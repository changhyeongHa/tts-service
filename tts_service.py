import os
import tempfile
from fastapi import FastAPI, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import List, Dict, Any
import azure.cognitiveservices.speech as speechsdk
import logging
import json
import base64

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TTS Service",
    description="Azure Speech Services를 사용한 텍스트-음성 변환 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Speech 설정
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "ko-KR-SunHiNeural")

if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
    logger.error("환경변수 AZURE_SPEECH_KEY / AZURE_SPEECH_REGION 이(가) 필요합니다.")
    raise RuntimeError("환경변수 AZURE_SPEECH_KEY / AZURE_SPEECH_REGION 이(가) 필요합니다.")

class TTSRequest(BaseModel):
    text: str
    voice_name: str = DEFAULT_VOICE

class MessageDict(BaseModel):
    HumanMessage: str = None
    AIMessage: str = None

class Citation(BaseModel):
    title: str
    page: str  # RAG에서 str로 반환되므로 타입 맞춤
    download_link: str = ""  # 다운로드 링크 추가

class RAGResponse(BaseModel):
    success: bool
    messages: List[MessageDict]
    citations: List[Citation] = []

# RAGTTSRequest는 RAGResponse와 동일
RAGTTSRequest = RAGResponse
    
class TTSResponse(BaseModel):
    success: bool
    message: str
    filename: str = None

class RAGTTSResponse(BaseModel):
    # RAG 응답 구조 유지
    success: bool
    messages: List[MessageDict]
    citations: List[Citation] = []
    
    # TTS 추가 정보
    audio_file: str  # base64 encoded audio data
    voice_info: Dict[str, Any] = {}

def synthesize_to_wav(text: str, filename: str = None, voice_name: str = None) -> dict:
    """텍스트를 음성으로 변환해 wav 파일로 저장"""
    
    if not filename:
        # 임시 파일 생성
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = tmp_file.name
        tmp_file.close()
    
    voice = voice_name or DEFAULT_VOICE
    
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_SPEECH_KEY, 
            region=AZURE_SPEECH_REGION
        )
        speech_config.speech_synthesis_voice_name = voice

        audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )

        logger.info(f"TTS 변환 시작: {text[:50]}...")
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info(f"TTS 변환 완료: {filename}")
            return {
                "success": True,
                "message": "음성 합성 완료",
                "filename": filename,
                "voice_name": voice,
                "text_length": len(text)
            }
        else:
            error_msg = f"음성 합성 실패: {result.reason}"
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg += f" - {cancellation.reason}: {cancellation.error_details}"
            
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "filename": None
            }
            
    except Exception as e:
        logger.error(f"TTS 변환 중 오류: {str(e)}")
        return {
            "success": False,
            "message": f"TTS 변환 오류: {str(e)}",
            "filename": None
        }

@app.get("/")
async def root():
    """TTS 서비스 상태 확인"""
    return {"message": "TTS Service is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    try:
        # Azure Speech 서비스 연결 테스트
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_SPEECH_KEY,
            region=AZURE_SPEECH_REGION
        )
        
        return {
            "status": "healthy",
            "service": "TTS Service",
            "version": "1.0.0",
            "azure_speech_region": AZURE_SPEECH_REGION,
            "default_voice": DEFAULT_VOICE
        }
    except Exception as e:
        logger.error(f"헬스체크 실패: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/tts/convert")
async def convert_text_to_speech(request: TTSRequest):
    """
    텍스트를 음성으로 변환
    
    Args:
        request: {"text": "변환할 텍스트", "voice_name": "음성 이름(선택)"}
    
    Returns:
        WAV 파일을 직접 응답으로 반환
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="변환할 텍스트가 비어있습니다.")
    
    if len(request.text) > 1000:
        raise HTTPException(status_code=400, detail="텍스트가 너무 깁니다. (최대 1000자)")
    
    try:
        result = synthesize_to_wav(
            text=request.text,
            voice_name=request.voice_name
        )
        
        if result["success"]:
            # WAV 파일을 응답으로 반환
            return FileResponse(
                path=result["filename"],
                media_type="audio/wav",
                filename="tts_output.wav",
                headers={
                    "Content-Disposition": "attachment; filename=tts_output.wav",
                    "X-Voice-Name": result["voice_name"],
                    "X-Text-Length": str(result["text_length"]),
                    "X-TTS-Success": "true",
                    "X-TTS-Message": "음성 합성 완료"
                }
            )
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS API 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS 변환 실패: {str(e)}")

@app.post("/tts/convert-json")
async def convert_text_to_speech_json(request: TTSRequest):
    """
    텍스트를 음성으로 변환 (JSON 응답)
    
    Args:
        request: {"text": "변환할 텍스트", "voice_name": "음성 이름(선택)"}
    
    Returns:
        {"success": true, "message": "완료", "filename": "파일경로"}
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="변환할 텍스트가 비어있습니다.")
    
    try:
        result = synthesize_to_wav(
            text=request.text,
            voice_name=request.voice_name
        )
        
        return TTSResponse(**result)
        
    except Exception as e:
        logger.error(f"TTS JSON API 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS 변환 실패: {str(e)}")

@app.post("/tts/convert-rag-response")
async def convert_rag_response_to_speech(request: RAGTTSRequest):
    """
    RAG 응답을 JSON + WAV 파일로 multipart 형태로 반환
    
    Args:
        request: RAG 응답 구조
    
    Returns:
        Multipart Response: Part 1 = 원본 JSON, Part 2 = WAV 파일
    """
    try:
        rag_data = request
        
        # AI 메시지 추출
        ai_message = ""
        for message in rag_data.messages:
            if message.AIMessage:
                ai_message = message.AIMessage
                break
        
        if not ai_message.strip():
            raise HTTPException(status_code=400, detail="AI 메시지가 없습니다.")
        
        # 텍스트를 음성으로 변환
        tts_result = synthesize_to_wav(
            text=ai_message,
            voice_name=DEFAULT_VOICE
        )
        
        if not tts_result["success"]:
            raise HTTPException(status_code=500, detail=tts_result["message"])
        
        # WAV 파일 읽기
        with open(tts_result["filename"], "rb") as audio_file:
            audio_data = audio_file.read()
        
        # 임시 파일 정리
        os.unlink(tts_result["filename"])
        
        # 원본 JSON 구조 그대로 유지
        original_json = {
            "success": rag_data.success,
            "messages": [msg.dict() for msg in rag_data.messages],
            "citations": [citation.dict() for citation in rag_data.citations]
        }
        
        # Multipart boundary 생성
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        
        # Multipart 응답 구성
        json_part = f"""------WebKitFormBoundary7MA4YWxkTrZu0gW\r
Content-Disposition: form-data; name="json"\r
Content-Type: application/json\r
\r
{json.dumps(original_json, ensure_ascii=False)}\r
""".encode('utf-8')

        audio_part_header = f"""------WebKitFormBoundary7MA4YWxkTrZu0gW\r
Content-Disposition: form-data; name="audio"; filename="answer.wav"\r
Content-Type: audio/wav\r
\r
""".encode('utf-8')

        audio_part_footer = b"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"
        
        # 전체 컨텐츠 조합
        content = json_part + audio_part_header + audio_data + audio_part_footer
        
        logger.info(f"RAG-TTS multipart 변환 완료: {len(ai_message)}자 → {len(audio_data)}bytes")
        
        return Response(
            content=content,
            media_type=f"multipart/form-data; boundary={boundary}",
            headers={
                "X-RAG-Success": str(rag_data.success),
                "X-Voice-Name": DEFAULT_VOICE,
                "X-Citations-Count": str(len(rag_data.citations)),
                "X-Audio-Format": "wav",
                "X-Response-Type": "multipart"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"RAG-TTS multipart 변환 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RAG-TTS multipart 변환 실패: {str(e)}")


@app.post("/tts/convert-rag-response-file")
async def convert_rag_response_to_file(request: RAGTTSRequest):
    """
    RAG 응답을 받아서 WAV 파일로 직접 다운로드 제공
    """
    try:
        rag_data = request
        
        # AI 메시지 추출
        ai_message = ""
        for message in rag_data.messages:
            if message.AIMessage:
                ai_message = message.AIMessage
                break
        
        if not ai_message.strip():
            raise HTTPException(status_code=400, detail="AI 메시지가 없습니다.")
        
        # 텍스트를 음성으로 변환
        tts_result = synthesize_to_wav(
            text=ai_message,
            voice_name=DEFAULT_VOICE
        )
        
        if not tts_result["success"]:
            raise HTTPException(status_code=500, detail=tts_result["message"])
        
        # 헤더에 RAG 정보 포함
        headers = {
            "Content-Disposition": "attachment; filename=rag_answer.wav",
            "X-Voice-Name": DEFAULT_VOICE,
            "X-Text-Length": str(len(ai_message)),
            "X-RAG-Success": str(rag_data.success),
            "X-Citations-Count": str(len(rag_data.citations))
        }
        
        # 인용 정보도 헤더에 포함 (첫 번째 인용만)
        if rag_data.citations:
            first_citation = rag_data.citations[0]
            headers["X-First-Citation"] = f"{first_citation.title}::{first_citation.page}"
        
        # RAG 메타데이터를 더 체계적으로 헤더에 포함
        headers.update({
            "X-TTS-Success": "true",
            "X-AI-Message-Preview": ai_message[:100] + "..." if len(ai_message) > 100 else ai_message,
            "X-RAG-Messages-Count": str(len(rag_data.messages))
        })
        
        return FileResponse(
            path=tts_result["filename"],
            media_type="audio/wav",
            filename="rag_answer.wav",
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"RAG-TTS 파일 변환 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RAG-TTS 파일 변환 실패: {str(e)}")






if __name__ == "__main__":
    import uvicorn
    logger.info("TTS Service 시작...")
    uvicorn.run(app, host="0.0.0.0", port=8003)
