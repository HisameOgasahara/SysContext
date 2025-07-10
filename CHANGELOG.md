# CHANGELOG

모든 변경사항은 이 파일에 기록됩니다.

이 프로젝트는 [시맨틱 버전닝(Semantic Versioning)](https://semver.org/lang/ko/)을 따릅니다.

사용법: 앞으로 새로운 기능을 추가하거나 버그를 수정하면, 가장 아래의 [Unreleased] 섹션에 내용을 추가하세요. 나중에 새로운 버전을 배포할 때 [Unreleased]를 [1.1.0] - YYYY-MM-DD와 같이 바꾸고, 새로운 [Unreleased] 섹션을 위에 추가하면 됩니다.

## [Unreleased]

### Added
- `reporter.py`에 특정 경로의 Python 환경 분석 기능 추가.
- `app.py`에 `reporter.py` 자동 실행 기능 추가.

## [1.0.0] - 2025-07-10

### Added
- Streamlit을 사용한 GUI 인터페이스 (`app.py`).
- 시스템 정보(OS, H/W, GPU) 수집 기능.
- 네트워크 정보(ipconfig, ping) 수집 기능.
- 현재 Python 환경 정보 수집 기능.
- `reporter.py`와 `app.py`의 기능/UI 분리 아키텍처 도입.
- Linux/macOS용 CLI 스크립트 (`get_system_info.sh`, `get_python_env.sh`).
- 프로젝트 `README.md` 및 `requirements.txt` 파일.