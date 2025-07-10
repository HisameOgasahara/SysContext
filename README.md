# 💻 SysContext: Execution Environment Reporter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LLM과의 대화 효율을 극대화하기 위한 실행 환경 정보 리포터입니다.**

이 도구는 복잡한 개발 환경(OS, 하드웨어, Python 라이브러리 등) 정보를 체계적으로 수집하고, LLM에게 정확한 컨텍스트를 제공하여 문제 해결 시간을 단축시키기 위해 만들어졌습니다.

---

## ✨ 핵심 아키텍처: 기능과 UI의 분리

이 프로젝트는 안정성과 확장성을 위해 **"관심사의 분리"** 원칙에 따라 설계되었습니다.

`데이터 수집 (Backend)` ↔ `JSON 데이터 파일` ↔ `UI (Frontend)`

*   **`reporter.py`**: 모든 시스템 정보를 수집하여 표준 `data.json` 파일로 저장하는 순수 Python 스크립트.
*   **`app.py`**: `data.json` 파일을 읽어 시각적으로 보여주는 역할만 하는 안정적인 Streamlit UI.

이 구조 덕분에 데이터 수집 로직과 UI 렌더링이 서로 영향을 주지 않아 매우 견고하게 작동합니다.

---

## 🚀 시작하기

### 🔧 설치

**사전 준비**:
*   Python 3.8 이상
*   `git`

**설치 과정**:
1.  프로젝트를 클론합니다.
    ```bash
    git clone https://github.com/YourUsername/SysContext.git
    cd SysContext
    ```
2.  가상환경을 생성하고 활성화합니다.
    ```bash
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows PowerShell
    .\venv\Scripts\Activate.ps1
    ```
3.  `requirements.txt`를 사용하여 필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

### ⚠️ 중요: 보안 유의사항

이 도구는 실행 시 사용자의 시스템 정보를 담은 리포트 파일들(**`data.json`**, **`system_info.md`** 등)을 생성합니다. 이 파일들에는 IP 주소, 컴퓨터 이름 등 민감할 수 있는 정보가 포함됩니다.

**`.gitignore` 파일에 이러한 생성 파일들이 기본적으로 등록되어 있어, 실수로 GitHub에 업로드되는 것을 방지합니다.**

- **절대로 `.gitignore` 파일에서 이 항목들을 삭제하지 마세요.**
- 만약 이 프로젝트를 포크(Fork)하거나 직접 관리할 경우, 생성된 리포트 파일들이 공개되지 않도록 항상 주의하십시오.

---

## 📖 기능 및 사용법

이 도구는 사용자의 목적에 따라 세 가지 방식으로 활용할 수 있습니다.

### 1) GUI - 가장 편리한 올인원(All-in-One) 방식

> 복잡한 과정 없이 웹 UI로 모든 정보를 한 번에 보고 싶을 때 사용합니다.

`streamlit run app.py` 명령어 하나만 실행하면, 앱이 시작될 때 자동으로 `reporter.py`를 호출하여 최신 시스템 정보로 `data.json`을 갱신하고, 그 결과를 즉시 화면에 보여줍니다.

**실행 방법:**
```bash
# (가상환경 활성화 후)
streamlit run app.py
```

### 2) 리포터 - 독립적인 데이터 수집기

> UI 없이 순수하게 시스템 정보 데이터(`data.json`)만 생성하고 싶을 때 사용합니다.

`reporter.py`를 직접 실행하면 시스템 정보를 수집하여 `data.json` 파일로 저장합니다. 다른 프로그램에서 이 데이터를 활용하거나, 단순히 텍스트 파일로 정보를 확인하고 싶을 때 유용합니다.

**실행 방법:**
```bash
# (가상환경 활성화 후)
python reporter.py
# -> data.json 파일이 생성되거나 갱신됩니다.
```
**팁**: `reporter.py` 파일을 직접 수정하여 특정 경로의 Python 환경을 분석할 수도 있습니다.

### 3) CLI - 순수 터미널 환경용 스크립트

> Python이나 GUI 환경이 없는 원격 서버 등 순수 CLI 환경에서 시스템 정보를 확인하고 싶을 때 사용합니다.

**Linux / macOS 용 쉘 스크립트:**
*   **시스템 정보 수집**:
    ```bash
    chmod +x get_system_info.sh
    ./get_system_info.sh
    # -> system_info.md 파일이 생성됩니다. (이 파일은 .gitignore에 의해 추적되지 않습니다)
    ```
*   **Python 환경 정보 수집**:
    ```bash
    # (1) get_python_env.sh 파일의 PYTHON_EXEC_PATH 변수에 분석할 경로를 입력합니다.
    # (2) 스크립트를 실행합니다.
    chmod +x get_python_env.sh
    ./get_python_env.sh
    # -> python_env_info.md 파일이 생성됩니다. (이 파일은 .gitignore에 의해 추적되지 않습니다)
    ```

---

## 📝 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.