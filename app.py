# app.py

import streamlit as st
import json
import os
import pandas as pd
import platform
import reporter # [!!!] reporter.py를 모듈로 임포트

# [!!!] DataFrame을 안전하게 생성하는 헬퍼 함수
def create_info_df(info_dict):
    items_as_strings = [(key, str(value)) for key, value in info_dict.items()]
    df = pd.DataFrame(items_as_strings, columns=["항목", "정보"])
    return df

# --- Streamlit UI 구성 ---
st.set_page_config(page_title="실행 환경 정보", layout="wide")

# [!!!] 앱 시작 시 자동으로 리포트 생성
with st.spinner("최신 시스템 정보를 수집하는 중..."):
    reporter.main()

st.title("💻 실행 환경 정보 분석기")

DATA_FILE = "data.json"

# 데이터 파일이 있는지 확인
if not os.path.exists(DATA_FILE):
    st.error(f"❌ '{DATA_FILE}' 파일 생성에 실패했습니다. 터미널 로그를 확인해주세요.")
    st.stop()

# 데이터 로드
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

st.caption(f"데이터 생성 시각: {data['metadata']['report_time']}")

# --- 1. 시스템 프로필 ---
st.header("1. 시스템 프로필 (OS, 하드웨어)")
profile = data.get("system_profile", {})
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("OS 정보")
        os_info = profile.get("os", {})
        st.dataframe(create_info_df(os_info), use_container_width=True, hide_index=True)
    with col2:
        st.subheader("하드웨어 정보")
        hw_info = profile.get("hardware", {})
        st.dataframe(create_info_df(hw_info), use_container_width=True, hide_index=True)
    
    st.subheader("GPU & CUDA 정보")
    gpu_info = profile.get("gpu", {})
    gpu_error = gpu_info.pop('오류 상세', None)
    st.dataframe(create_info_df(gpu_info), use_container_width=True, hide_index=True)
    if gpu_error:
        with st.expander("⚠️ GPU 정보 조회 오류 상세 정보"):
            st.error("GPU 정보 조회에 실패했습니다.")
            st.code(gpu_error)

# --- 2. 상세 네트워크 정보 ---
st.header("2. 상세 네트워크 정보")
network = data.get("network", {})
with st.expander("🌐 `ipconfig /all` 또는 `ifconfig` 결과 보기"):
    st.code(network.get("details", "정보 없음"), language='powershell' if platform.system() == 'Windows' else 'bash')

with st.expander("📡 인터넷 연결 확인 (Ping Test)"):
    ping_test = network.get("ping_test", {})
    if ping_test.get("status") == "success": st.success("인터넷 연결이 양호합니다.")
    else: st.error("인터넷 연결을 확인하세요. (Ping 실패)")
    st.code(ping_test.get("log", "정보 없음"))

st.divider()

# --- 3. Python 환경 정보 ---
st.header("3. Python 환경 정보")
tab_current, tab_specific = st.tabs(["현재 실행 환경", "지정 경로 환경 분석"])

with tab_current:
    py_info = data.get("current_python", {})
    py_info_display = py_info.copy()
    packages = py_info_display.pop("설치된 라이브러리", "정보 없음")
    st.dataframe(create_info_df(py_info_display), use_container_width=True, hide_index=True)
    with st.expander("설치된 라이브러리 목록 보기 (pip freeze)"):
        st.code(packages)

with tab_specific:
    specific_py_info = data.get("specific_python")
    if specific_py_info:
        if "오류" in specific_py_info:
            st.error(f"지정된 경로 분석 중 오류 발생: {specific_py_info['분석 대상 경로']}")
            st.code(specific_py_info['오류'])
        else:
            st.info(f"분석 대상: `{specific_py_info['분석 대상 경로']}`")
            st.text(f"버전: {specific_py_info['버전']}")
            with st.expander("설치된 라이브러리 목록 보기"):
                st.code(specific_py_info['설치된 라이브러리'])
    else:
        st.info("분석할 다른 Python 환경이 지정되지 않았습니다. `reporter.py` 파일의 `PYTHON_EXEC_PATH` 변수를 수정하세요.")

st.divider()

# --- 4. LLM 컨텍스트 제공 ---
st.header("4. LLM 컨텍스트 제공용")
# (이전과 동일)
st.info("필요한 정보를 복사하여 LLM에게 질문과 함께 전달하세요.")
system_context = "## 시스템 프로필\n\n"
for k, v in {**os_info, **hw_info, **gpu_info}.items(): system_context += f"- **{k}**: `{v}`\n"
st.text_area("시스템 프로필 복사하기", system_context, height=200)
current_os = platform.system()
if current_os == 'Windows':
    st.warning("**현재 OS는 Windows입니다. LLM에게 코드 요청 시 다음을 명시하세요:**\n\n- `Windows 환경입니다. 경로 구분자는 \\ (백슬래시)를 사용하고, 줄바꿈 문자는 CRLF 입니다.`\n- `쉘 스크립트는 PowerShell 기준으로 작성해주세요.`")
else:
    st.warning("**현재 OS는 Linux/macOS 입니다. LLM에게 코드 요청 시 다음을 명시하세요:**\n\n- `Linux/macOS 환경입니다. 경로 구분자는 / (슬래시)를 사용하고, 줄바꿈 문자는 LF 입니다.`\n- `쉘 스크립트는 bash 기준으로 작성해주세요.`")