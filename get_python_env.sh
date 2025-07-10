#!/bin/bash
# 지정된 Python 가상환경의 정보를 수집하여 Markdown 파일로 저장합니다.
# 실행 권한 부여: chmod +x get_python_env.sh
# 실행 방법: ./get_python_env.sh

# --- ❗ [수정 필요] ❗ ---
# 아래 변수에 분석하고 싶은 Python 가상환경의 'python' 실행 파일의 전체 경로를 입력하세요.
# 예: PYTHON_EXEC_PATH="/home/user/myproject/venv/bin/python"
PYTHON_EXEC_PATH=""
# -------------------------

OUTPUT_FILE="python_env_info.md"

if [ -z "$PYTHON_EXEC_PATH" ]; then
    echo "❌ 오류: 스크립트의 PYTHON_EXEC_PATH 변수에 파이썬 실행 파일 경로를 입력해야 합니다." >&2
    exit 1
fi

if [ ! -f "$PYTHON_EXEC_PATH" ]; then
    echo "❌ 오류: '$PYTHON_EXEC_PATH' 경로에 파일이 존재하지 않습니다." >&2
    exit 1
fi

# [수정] 'true' 명령어를 사용하여 파일을 명확하게 초기화합니다.
true > "$OUTPUT_FILE"

# [수정] 여러 echo 명령어를 블록으로 묶어 파일에 한 번만 쓰도록 합니다.
{
    echo "## 🐍 Python 환경 정보"
    echo "---"
    echo "- **분석 대상 경로**: \`$PYTHON_EXEC_PATH\`"
    echo ""
    echo "### Python 버전"
    echo "\`\`\`"
} >> "$OUTPUT_FILE"

# 명령어 결과는 별도로 리디렉션합니다.
"$PYTHON_EXEC_PATH" --version >> "$OUTPUT_FILE" 2>&1

{
    echo "\`\`\`"
    echo ""
    echo "### 설치된 라이브러리 (pip freeze)"
    echo "\`\`\`"
} >> "$OUTPUT_FILE"

"$PYTHON_EXEC_PATH" -m pip freeze >> "$OUTPUT_FILE" 2>&1
echo "\`\`\`" >> "$OUTPUT_FILE"

echo "✅ 정보 수집 완료! 결과가 '$OUTPUT_FILE' 파일에 저장되었습니다."