#!/bin/bash
# 시스템의 OS, 하드웨어, 네트워크 정보를 수집하여 Markdown 파일로 저장합니다.
# 실행 권한 부여: chmod +x get_system_info.sh
# 실행 방법: ./get_system_info.sh

OUTPUT_FILE="system_info.md"

# [수정] 'true' 명령어를 사용하여 파일을 명확하게 초기화합니다.
true > "$OUTPUT_FILE"

# [수정] 여러 echo 명령어를 블록으로 묶어 파일에 한 번만 쓰도록 합니다.
{
    echo "## 🖥️ 시스템 정보"
    echo "---"
    echo "### OS 정보"
    echo "- **OS 종류**: $(uname -s)"
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        echo "- **OS 버전**: $PRETTY_NAME"
    else
        echo "- **OS 버전**: $(uname -r)"
    fi
    echo "- **아키텍처**: $(uname -m)"
    echo ""
    echo "### 하드웨어 정보"
    echo "- **CPU 정보**: "
    echo "\`\`\`"
} >> "$OUTPUT_FILE"

# 명령어 결과는 별도로 리디렉션합니다.
lscpu | grep -E 'Model name|CPU\(s\)|Vendor ID|Architecture' >> "$OUTPUT_FILE"

{
    echo "\`\`\`"
    echo "- **RAM 정보**: "
    echo "\`\`\`"
} >> "$OUTPUT_FILE"

free -h >> "$OUTPUT_FILE"

{
    echo "\`\`\`"
    echo ""
} >> "$OUTPUT_FILE"

# GPU 정보 (NVIDIA)
if command -v nvidia-smi &> /dev/null
then
    {
        echo "### GPU & CUDA 정보"
        echo "\`\`\`"
    } >> "$OUTPUT_FILE"
    nvidia-smi >> "$OUTPUT_FILE"
    echo "\`\`\`" >> "$OUTPUT_FILE"
else
    echo "### GPU & CUDA 정보" >> "$OUTPUT_FILE"
    echo "NVIDIA GPU 드라이버(nvidia-smi)를 찾을 수 없습니다." >> "$OUTPUT_FILE"
fi

# 네트워크 정보
{
    echo ""
    echo "### 네트워크 정보"
    echo "- **Hostname**: $(hostname)"
    echo "- **IP 주소**: "
    echo "\`\`\`"
} >> "$OUTPUT_FILE"

ip addr | grep 'inet ' >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"

echo "✅ 정보 수집 완료! 결과가 '$OUTPUT_FILE' 파일에 저장되었습니다."