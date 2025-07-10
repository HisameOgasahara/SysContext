# CHANGELOG

모든 변경사항은 이 파일에 기록됩니다.

이 프로젝트는 [시맨틱 버전닝(Semantic Versioning)](https://semver.org/lang/ko/)을 따릅니다.

사용법: 앞으로 새로운 기능을 추가하거나 버그를 수정하면, 가장 아래의 [Unreleased] 섹션에 내용을 추가하세요. 나중에 새로운 버전을 배포할 때 [Unreleased]를 [1.1.0] - YYYY-MM-DD와 같이 바꾸고, 새로운 [Unreleased] 섹션을 위에 추가하면 됩니다.

## [Unreleased]

## [1.1.0] - 2025-07-10

### Added
- OS(Windows/Unix)에 따른 코드 생성 가이드(`llm_instruction_for_code_generation`)를 `data.json`에 추가.
- 네트워크 정보(IP, MAC 주소 등)를 마스킹하는 기능 추가.
- 최종 `data.json` 내용을 영문/한글 키 버전으로 나누어 볼 수 있는 탭 기능 구현.
- 배포 대상 옵션에 `Cloudflare Tunnel`, `Hugging Face Spaces` 추가 및 순서 조정.
- `st.session_state`를 도입하여 폼 제출 후 UI 상태가 즉시 반영되도록 개선.

### Changed
- `useCI` 체크박스를 제거하고 CI 도구 선택 `selectbox`에 `None` 옵션을 추가하여 UI를 간소화.
- `app.py`가 `reporter.py`를 내부적으로 호출하고 모든 인터페이스를 관리하도록 메인 로직을 통합.
- `README.md` 내용을 `streamlit` 기반의 GUI 사용법 중심으로 전면 개편.
- 생성되는 데이터 파일 경로를 `data/data.json`으로 표준화.
- `pandas` 라이브러리 의존성 제거.

## [1.0.0] - 2025-07-10

### Added
- Streamlit을 사용한 GUI 인터페이스 (`app.py`).
- 시스템 정보(OS, H/W, GPU) 수집 기능.
- 네트워크 정보(ipconfig, ping) 수집 기능.
- 현재 Python 환경 정보 수집 기능.
- `reporter.py`와 `app.py`의 기능/UI 분리 아키텍처 도입.
- Linux/macOS용 CLI 스크립트 (`get_system_info.sh`, `get_python_env.sh`).
- 프로젝트 `README.md` 및 `requirements.txt` 파일.