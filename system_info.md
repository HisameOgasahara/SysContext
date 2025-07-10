#!/bin/bash
# 시스템의 OS, 하드웨어, 네트워크 정보를 수집하여 Markdown 파일로 저장합니다.
# 실행 권한 부여: chmod +x get_system_info.sh
# 실행 방법: ./get_system_info.sh

OUTPUT_FILE="system_info.md"

# 파일 초기화
> "$OUTPUT_FILE"

echo "## 🖥️ 시스템 정보" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"

# OS 정보
echo "### OS 정보" >> "$OUTPUT_FILE"
echo "- **OS 종류**: $(uname -s)" >> "$OUTPUT_FILE"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "- **OS 버전**: $PRETTY_NAME" >> "$OUTPUT_FILE"
else
    echo "- **OS 버전**: $(uname -r)" >> "$OUTPUT_FILE"
fi
echo "- **아키텍처**: $(uname -m)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 하드웨어 정보
echo "### 하드웨어 정보" >> "$OUTPUT_FILE"
echo "- **CPU 정보**: " >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"
lscpu | grep -E 'Model name|CPU\(s\)|Vendor ID|Architecture' >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"
echo "- **RAM 정보**: " >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"
free -h >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# GPU 정보 (NVIDIA)
if command -v nvidia-smi &> /dev/null
then
    echo "### GPU & CUDA 정보" >> "$OUTPUT_FILE"
    echo "\`\`\`" >> "$OUTPUT_FILE"
    nvidia-smi >> "$OUTPUT_FILE"
    echo "\`\`\`" >> "$OUTPUT_FILE"
else
    echo "### GPU & CUDA 정보" >> "$OUTPUT_FILE"
    echo "NVIDIA GPU 드라이버(nvidia-smi)를 찾을 수 없습니다." >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 네트워크 정보
echo "### 네트워크 정보" >> "$OUTPUT_FILE"
echo "- **Hostname**: $(hostname)" >> "$OUTPUT_FILE"
echo "- **IP 주소**: " >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"
ip addr | grep 'inet ' >> "$OUTPUT_FILE"
echo "\`\`\`" >> "$OUTPUT_FILE"

echo "✅ 정보 수집 완료! 결과가 '$OUTPUT_FILE' 파일에 저장되었습니다."