# reporter.py

import platform
import subprocess
import sys
import os
import re
from datetime import datetime

# --- 유틸리티 함수 (이전과 동일) ---
def safe_decode(byte_string):
    if isinstance(byte_string, bytes):
        try: return byte_string.decode('utf-8')
        except UnicodeDecodeError: return byte_string.decode('cp949', errors='ignore')
    return byte_string

# --- 정보 수집 함수 (네트워크 포함) ---
def get_os_info():
    info = {'os_type': platform.system()}
    if info['os_type'] == 'Windows': info['os_version'] = platform.release()
    elif info['os_type'] == 'Darwin': info['os_version'] = platform.mac_ver()[0]
    else: info['os_version'] = " ".join(platform.uname()[2:4])
    info['cpu_arch'] = platform.machine()
    return info

def get_hardware_info():
    info = {}
    try:
        import cpuinfo
        info['cpu_model'] = cpuinfo.get_cpu_info()['brand_raw']
    except Exception: info['cpu_model'] = platform.processor()
    try:
        import psutil
        info['ram_total_gb'] = round(psutil.virtual_memory().total / (1024**3), 2)
    except Exception: info['cpu_ram_info'] = "psutil/cpuinfo 라이브러리 문제"
    return info

def get_gpu_info():
    info = {}
    try:
        import pynvml
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        gpus = [f"{safe_decode(pynvml.nvmlDeviceGetName(i))} ({round(pynvml.nvmlDeviceGetMemoryInfo(i).total / (1024**3), 2)} GB)" for i in range(count)]
        info['gpu'] = ", ".join(gpus) if gpus else "N/A"
        info['cuda_driver_version'] = safe_decode(pynvml.nvmlSystemGetDriverVersion())
        pynvml.nvmlShutdown()
    except Exception:
        info['gpu'], info['cuda_driver_version'] = "N/A", "N/A"
    try:
        output = subprocess.check_output(['nvcc', '--version'])
        match = re.search(r'release (\d+\.\d+)', safe_decode(output))
        if match: info['cuda_toolkit_version'] = match.group(1)
    except Exception: info['cuda_toolkit_version'] = "N/A"
    return info

def get_python_details():
    return {
        'version': sys.version.split(' ')[0],
        'executable': sys.executable,
        'is_venv': sys.prefix != sys.base_prefix,
        'pip_freeze': safe_decode(subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']))
    }

def get_network_details():
    system = platform.system()
    try:
        cmd = ["ipconfig", "/all"] if system == "Windows" else ["ip", "addr"]
        return safe_decode(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    except Exception as e: return f"네트워크 상세 정보 조회 실패: {e}"

def get_ping_test():
    system = platform.system()
    count_flag = "-n" if system == "Windows" else "-c"
    try:
        output = subprocess.check_output(["ping", count_flag, "4", "google.com"], stderr=subprocess.STDOUT, timeout=10)
        return {"status": "success", "log": safe_decode(output)}
    except Exception as e: return {"status": "fail", "log": str(e)}

def collect_all_system_info():
    """
    시스템에서 수집 가능한 모든 정보를 수집하여 딕셔너리로 반환합니다.
    """
    return {
        "os_info": get_os_info(),
        "hardware_info": get_hardware_info(),
        "gpu_info": get_gpu_info(),
        "python_details": get_python_details(),
        "network_details": get_network_details(),
        "ping_test": get_ping_test()
    }

# 이 파일이 직접 실행될 때를 위한 테스트용 코드
if __name__ == "__main__":
    import json
    print("수집 가능한 모든 시스템 정보:")
    all_info = collect_all_system_info()
    print(json.dumps(all_info, indent=2, ensure_ascii=False))