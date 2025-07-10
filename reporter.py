# reporter.py

import platform
import subprocess
import sys
import os
import re
from datetime import datetime
import json
import socket

# --- 유틸리티 함수 ---
def safe_decode(byte_string):
    if isinstance(byte_string, bytes):
        try: return byte_string.decode('utf-8')
        except UnicodeDecodeError: return byte_string.decode('cp949', errors='ignore')
    return byte_string

# --- 정보 수집 함수 (기존과 동일) ---
def get_os_info():
    info = {'OS 종류': platform.system()}
    if info['OS 종류'] == 'Windows': info['OS 버전'] = f"{platform.system()} {platform.release()} {platform.version()}"
    else: info['OS 버전'] = f"{platform.system()} {platform.release()}"
    info['아키텍처'] = platform.machine()
    return info

def get_hardware_info():
    info = {}
    try:
        import cpuinfo
        info['CPU 모델'] = cpuinfo.get_cpu_info()['brand_raw']
    except Exception: info['CPU 모델'] = platform.processor()
    try:
        import psutil
        info['CPU 논리 코어 수'] = psutil.cpu_count(logical=True)
        info['CPU 물리 코어 수'] = psutil.cpu_count(logical=False)
        info['RAM 전체 크기 (GB)'] = round(psutil.virtual_memory().total / (1024**3), 2)
    except Exception: info['CPU/RAM 정보'] = "psutil 또는 cpuinfo 라이브러리 문제"
    return info

def get_gpu_info():
    info = {}
    try:
        import pynvml
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        gpus = [f"{safe_decode(pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(i)))} (VRAM: {round(pynvml.nvmlDeviceGetMemoryInfo(pynvml.nvmlDeviceGetHandleByIndex(i)).total / (1024**3), 2)} GB)" for i in range(count)]
        info['GPU'] = ", ".join(gpus) if gpus else "감지된 NVIDIA GPU 없음"
        info['CUDA 드라이버 버전'] = safe_decode(pynvml.nvmlSystemGetDriverVersion())
        pynvml.nvmlShutdown()
    except Exception as e:
        info['GPU'], info['CUDA 드라이버 버전'] = "NVIDIA GPU 정보를 가져올 수 없습니다.", "확인 불가"
        info['오류 상세'] = str(e)
    try:
        output = subprocess.check_output(['nvcc', '--version'])
        match = re.search(r'release (\d+\.\d+)', safe_decode(output))
        if match: info['CUDA Toolkit 버전'] = match.group(1)
    except Exception: info['CUDA Toolkit 버전'] = "nvcc 확인 불가"
    return info

def get_network_details():
    system = platform.system()
    try:
        cmd = ["ipconfig", "/all"] if system == "Windows" else (["ifconfig"] if system == "Darwin" else ["ip", "addr"])
        return safe_decode(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    except Exception as e: return f"네트워크 정보 조회 중 오류 발생:\n{e}"

def get_ping_test():
    system = platform.system()
    count_flag = "-n" if system == "Windows" else "-c"
    try:
        output = subprocess.check_output(["ping", count_flag, "4", "google.com"], stderr=subprocess.STDOUT, timeout=10)
        return {"status": "success", "log": safe_decode(output)}
    except Exception as e: return {"status": "fail", "log": safe_decode(e.output) if hasattr(e, 'output') else str(e)}

def get_current_python_info():
    return {
        '버전': sys.version,
        '실행 파일 경로': sys.executable,
        '가상환경 여부': "예" if sys.prefix != sys.base_prefix else "아니오",
        '설치된 라이브러리': safe_decode(subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']))
    }

# [!!!] 새로운 함수: 지정된 경로의 Python 환경 분석
def analyze_specific_python():
    """사용자가 지정한 경로의 Python 환경을 분석합니다."""
    # --- ❗ [수정 필요] ❗ ---
    # 다른 Python 환경을 분석하고 싶다면, 아래 변수에 해당 Python 실행 파일의 '전체 경로'를 입력하세요.
    # 경로를 비워두면 ("") 이 기능은 실행되지 않습니다.
    # 예시 (Windows):   PYTHON_EXEC_PATH = r"C:\Projects\another-project\venv\Scripts\python.exe"
    # 예시 (Linux/macOS): PYTHON_EXEC_PATH = "/home/user/another-project/venv/bin/python"
    
    PYTHON_EXEC_PATH = ""
    # -------------------------

    if not PYTHON_EXEC_PATH or not os.path.exists(PYTHON_EXEC_PATH):
        return None # 경로가 비어있거나 파일이 없으면 아무것도 반환하지 않음

    try:
        version = safe_decode(subprocess.check_output([PYTHON_EXEC_PATH, '--version']))
        packages = safe_decode(subprocess.check_output([PYTHON_EXEC_PATH, '-m', 'pip', 'freeze']))
        return {
            '분석 대상 경로': PYTHON_EXEC_PATH,
            '버전': version.strip(),
            '설치된 라이브러리': packages
        }
    except Exception as e:
        return {
            '분석 대상 경로': PYTHON_EXEC_PATH,
            '오류': f"분석 중 오류 발생: {e}"
        }

def main():
    """모든 정보를 수집하여 data.json 파일로 저장합니다."""
    all_info = {
        "metadata": {
            "report_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "reporter_script": "reporter.py"
        },
        "system_profile": {
            "os": get_os_info(),
            "hardware": get_hardware_info(),
            "gpu": get_gpu_info()
        },
        "network": {
            "details": get_network_details(),
            "ping_test": get_ping_test()
        },
        "current_python": get_current_python_info(),
        "specific_python": analyze_specific_python() # 지정 경로 분석 결과 추가
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(all_info, f, ensure_ascii=False, indent=4)
    
    # 이 스크립트가 단독으로 실행될 때만 메시지 출력
    if __name__ == "__main__":
        print("✅ 정보 수집 완료! 'data.json' 파일이 생성되었습니다.")
        print("이제 'streamlit run app.py'를 실행하여 웹 UI를 확인하세요.")

if __name__ == "__main__":
    main()