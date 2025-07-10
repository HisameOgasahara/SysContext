# app.py

import streamlit as st
import json
import os
from datetime import datetime
import reporter  # reporter.py를 모듈로 임포트
import platform
import re

# --- 0. 유틸리티 함수 ---

def mask_network_details(text: str) -> str:
    """네트워크 정보에서 민감한 부분을 마스킹합니다."""
    sensitive_keywords = [
        "Physical Address", "물리적 주소",
        "IPv6 Address", "IPv6 주소",
        "IPv4 Address", "IPv4 주소",
        "Default Gateway", "기본 게이트웨이",
        "DHCP Server", "DHCP 서버",
        "DHCPv6 IAID",
        "DHCPv6 Client DUID", "DHCPv6 클라이언트 DUID",
        "DNS Servers", "DNS 서버"
    ]
    lines = text.split('\n')
    masked_lines = []
    for line in lines:
        if any(keyword in line for keyword in sensitive_keywords):
            parts = line.split(':', 1)
            if len(parts) == 2:
                masked_line = f"{parts[0]}: **[MASKED]**"
                masked_lines.append(masked_line)
            else:
                masked_lines.append(line)
        else:
            masked_lines.append(line)
    return "\n".join(masked_lines)

def translate_keys_for_display(data, key_map):
    """표시용으로 JSON 데이터의 키를 한글로 변환하는 재귀 함수"""
    if isinstance(data, dict):
        return {key_map.get(k, k): translate_keys_for_display(v, key_map) for k, v in data.items()}
    elif isinstance(data, list):
        return [translate_keys_for_display(elem, key_map) for elem in data]
    else:
        return data

# --- 1. 초기 설정 및 데이터 수집 ---
st.set_page_config(page_title="LLM 컨텍스트 생성기", layout="wide")

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")

os.makedirs(DATA_DIR, exist_ok=True)

@st.cache_data
def get_system_info():
    return reporter.collect_all_system_info()

system_info = get_system_info()

# 세션 상태 초기화
if 'latest_data' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                st.session_state.latest_data = json.load(f)
            except json.JSONDecodeError:
                st.session_state.latest_data = {}
    else:
        st.session_state.latest_data = {}

st.title("🤖 LLM 컨텍스트 생성기")
st.info(f"시스템 정보를 분석하고 개발 계획을 입력하여 **'{DATA_FILE}'** 파일을 생성/관리합니다.")

# --- 2. UI 구성 (st.form) ---

# 기본값은 마지막으로 저장된 데이터(세션 상태)에서 가져옴
env_data = st.session_state.latest_data.get("user_development_environment", {})
devops_data = st.session_state.latest_data.get("devops_and_infrastructure_plan", {})
os_info = system_info["os_info"]
py_info = system_info["python_details"]

ide_options = ["Cursor", "VSCode", "Jupyter Notebook", "Visual Studio", "Other"]
git_account_options = ["HisameOgasahara", "AriannaHeartbell", "직접 입력"]
deployment_options = ["AWS", "Cloudflare Tunnel", "Hugging Face Spaces", "Streamlit Cloud", "GCP", "Azure", "Other", "None"]
ci_options = ["None", "GitHub Actions", "GitLab CI", "Jenkins"]

with st.form("context_form"):
    st.header("1. 기본 환경 정보")
    
    st.subheader("사용자 개발 환경")
    c1, c2 = st.columns(2)
    with c1:
        ide_val = env_data.get("ide", "VSCode")
        ide_idx = ide_options.index(ide_val) if ide_val in ide_options else 0
        ide = st.selectbox("사용하는 IDE/에디터", ide_options, index=ide_idx)
        
        ide_version = st.text_input("IDE 버전 (선택)", value=env_data.get("ideVersion", ""))

    with c2:
        shell_options = ["PowerShell", "cmd", "bash", "zsh", "fish"]
        default_shell = "PowerShell" if platform.system() == "Windows" else "bash"
        shell_val = env_data.get("shell", default_shell)
        shell_idx = shell_options.index(shell_val) if shell_val in shell_options else 0
        shell = st.selectbox("주로 사용하는 쉘", shell_options, index=shell_idx)

    st.subheader("DevOps 및 인프라 계획")
    c3, c4 = st.columns(2)
    with c3:
        use_docker = st.checkbox("🐳 Docker 사용 예정", value=devops_data.get("useDocker", False))
        
    with c4:
        ci_val = devops_data.get("ciProvider", "None")
        ci_idx = ci_options.index(ci_val) if ci_val in ci_options else 0
        ci_provider = st.selectbox("CI 도구 (None 선택 시 미사용)", ci_options, index=ci_idx)

        dep_val = devops_data.get("deploymentTarget", "None")
        dep_idx = deployment_options.index(dep_val) if dep_val in deployment_options else len(deployment_options) - 1
        deployment_target = st.selectbox("배포 대상", deployment_options, index=dep_idx)
    
    st.subheader("Git 저장소 정보")
    selected_git_account = st.radio("GitHub 계정 선택", git_account_options, horizontal=True)
    custom_git_url = st.text_input("Git 계정/저장소 URL 직접 입력", 
                                   placeholder="https://github.com/my-org",
                                   disabled=(selected_git_account != "직접 입력"))

    st.divider()
    
    st.header("2. 선택적 상세 정보")
    st.caption("필요한 경우 추가 정보를 JSON에 포함시킵니다.")
    c5, c6 = st.columns(2)
    with c5:
        include_network = st.checkbox("🌐 네트워크 정보 포함", value="network_info" in st.session_state.latest_data)
        mask_network = st.checkbox("🔒 네트워크 상세 정보의 민감 정보(IP, MAC 등) 가리기", value=True, disabled=not include_network)
    
    with c6:
        include_python_details = st.checkbox("🐍 Python 상세 정보 포함", value="system_details_for_reference" in st.session_state.latest_data)

    submitted = st.form_submit_button("💾 data.json 저장하기", type="primary", use_container_width=True)

# --- 3. 폼 제출 시 파일 생성 및 상태 업데이트 로직 ---
if submitted:
    if selected_git_account == "직접 입력":
        git_url = custom_git_url
    else:
        git_url = f"https://github.com/{selected_git_account}"
    
    current_os = platform.system()
    if current_os == 'Windows':
        llm_instruction = "You are on a Windows system. Use '\\' as the path separator and expect CRLF line endings."
    else:
        llm_instruction = "You are on a Unix-like system (Linux/macOS). Use '/' as the path separator and expect LF line endings."

    final_data = {
        "metadata": {"last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        "user_development_environment": {
            "os": os_info.get("os_type"), "osVersion": os_info.get("os_version"),
            "pythonVersion": py_info.get("version"), "hardware": {"cpuArch": os_info.get("cpu_arch")},
            "ide": ide, "ideVersion": ide_version if ide_version else None, "shell": shell,
            "llm_instruction_for_code_generation": llm_instruction
        },
        "devops_and_infrastructure_plan": {
            "useDocker": use_docker, "useCI": ci_provider != "None", "ciProvider": ci_provider,
            "deploymentTarget": deployment_target, "gitRepoURL": git_url if git_url else None,
        }
    }
    
    if include_network:
        network_details_content = system_info["network_details"]
        if mask_network:
            network_details_content = mask_network_details(network_details_content)
        final_data["network_info"] = {"details": network_details_content, "ping_test": system_info["ping_test"]}
        
    if include_python_details:
        final_data["system_details_for_reference"] = {
            "hardware_info": system_info["hardware_info"], "gpu_info": system_info["gpu_info"],
            "python_executable": py_info["executable"], "is_venv": py_info["is_venv"],
            "pip_freeze": py_info["pip_freeze"]
        }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    # 세션 상태를 새로운 데이터로 업데이트
    st.session_state.latest_data = final_data
    
    st.success(f"✅ '{DATA_FILE}' 파일이 성공적으로 저장되었습니다!")
    st.balloons()

# --- 4. 생성된 JSON 내용 표시 ---
st.divider()
st.header("3. 최종 `data.json` 내용 확인")

# [수정] 안내 메시지 추가
st.info("현재 저장된 `data.json`의 내용입니다. 폼의 내용을 수정했다면 '저장하기' 버튼을 눌러야 이곳에 반영됩니다.")

if not st.session_state.latest_data:
    st.warning("폼을 제출하여 'data.json' 파일을 생성해주세요.")
else:
    display_data = st.session_state.latest_data
    st.caption(f"마지막 업데이트: {display_data.get('metadata', {}).get('last_updated', 'N/A')}")
    
    tab_en, tab_kr = st.tabs(["🗂️ 저장될 영문 JSON (실제 파일 내용)", "👀 표시용 한글 Key JSON"])

    with tab_en:
        st.json(display_data)
    
    with tab_kr:
        KOREAN_KEY_MAP = {
            "metadata": "메타데이터", "last_updated": "마지막 업데이트",
            "user_development_environment": "사용자 개발 환경",
            "os": "운영체제", "osVersion": "OS 버전", "pythonVersion": "파이썬 버전",
            "hardware": "하드웨어", "cpuArch": "CPU 아키텍처", "ide": "IDE", "ideVersion": "IDE 버전",
            "shell": "쉘", "llm_instruction_for_code_generation": "LLM 코드 생성 가이드",
            "devops_and_infrastructure_plan": "DevOps 및 인프라 계획",
            "useDocker": "Docker 사용 여부", "useCI": "CI 사용 여부", "ciProvider": "CI 도구",
            "deploymentTarget": "배포 대상", "gitRepoURL": "Git 저장소 URL",
            "network_info": "네트워크 정보", "details": "상세 정보", "ping_test": "핑 테스트",
            "system_details_for_reference": "참고용 시스템 상세 정보",
            "hardware_info": "하드웨어 정보", "gpu_info": "GPU 정보",
            "python_executable": "Python 실행파일 경로", "is_venv": "가상환경 사용 여부", "pip_freeze": "pip freeze 결과"
        }
        korean_display_data = translate_keys_for_display(display_data, KOREAN_KEY_MAP)
        st.json(korean_display_data)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            st.download_button(
                label="📥 data.json 파일 다운로드",
                data=f,
                file_name="data.json",
                mime="application/json"
            )