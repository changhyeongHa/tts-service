import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def synthesize_to_wav(text: str, filename: str = "output.wav") -> bool:
    """텍스트를 음성으로 변환해 wav 파일로 저장합니다.
    
    Args:
        text (str): 변환할 텍스트
        filename (str): 저장할 경로 (기본값: /output.wav)
    
    Returns:
        bool: 성공(True) 또는 실패(False)
    """
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = "ko-KR-SunHiNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"생성 완료: {filename}")
        return True
    else:
        print("실패:", result.reason)
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print("에러:", cancellation.reason, cancellation.error_details)
        return False