<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

<p align="center">
  <strong>OpenManus: 당신의 다재다능한 AI 에이전트 프레임워크</strong>
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README_zh.md">中文</a> | 한국어 | <a href="README_ja.md">日本語</a>
</p>

<p align="center">
  <a href="https://github.com/mannaandpoem/OpenManus/stargazers"><img src="https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social" alt="GitHub stars"></a>
  &amp;ensp;
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  &amp;ensp;
  <a href="https://discord.gg/DYn29wFk9z"><img src="https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat" alt="Discord Follow"></a>
  &amp;ensp;
  <a href="https://huggingface.co/spaces/lyh-917/OpenManusDemo"><img src="https://img.shields.io/badge/Demo-Hugging%20Face-yellow" alt="Demo"></a>
</p>

---

## 👋 소개

Manus에서 영감을 받은 **OpenManus**는 다양한 작업을 처리할 수 있는 다재다능한 AI 에이전트를 구축하기 위한 오픈 소스 프레임워크를 제공합니다. 초대 코드 없이 사용자가 아이디어를 실현할 수 있도록 지원하는 것을 목표로 합니다.

이 버전은 대화형 채팅 및 세션 관리를 위한 사용자 친화적인 **웹 UI**(Gradio로 구축)와 프로그래밍 방식 액세스를 위한 **OpenAI 호환 API**(FastAPI로 구축)를 통합합니다.

저희 팀 멤버인 [@Xinbin Liang](https://github.com/mannaandpoem)과 [@Jinyu Xiang](https://github.com/XiangJinyu)(핵심 저자), 그리고 [@Zhaoyang Yu](https://github.com/MoshiQAQ), [@Jiayi Zhang](https://github.com/didiforgithub), [@Sirui Hong](https://github.com/stellaHSR)([@MetaGPT](https://github.com/geekan/MetaGPT) 팀 소속)이 이 프로젝트를 시작했으며 계속 개발 중입니다. 제안, 기여 및 피드백을 환영합니다!

## ✨ 특징

*   **멀티턴 대화**: 컨텍스트를 유지하며 확장된 대화를 진행할 수 있습니다.
*   **웹 UI**: 직관적인 웹 인터페이스를 통해 에이전트와 상호 작용합니다. 다음 기능이 포함됩니다:
    *   실시간 업데이트를 위한 스트리밍 응답.
    *   세션 관리 (대화 생성, 이름 변경, 삭제, 전환).
    *   로컬 `chatsHistory/` 디렉토리에 자동으로 저장되는 영구적인 채팅 기록.
*   **OpenAI 호환 API**: 익숙한 OpenAI SDK 형식(`/v1/chat/completions` 엔드포인트)을 사용하여 OpenManus를 애플리케이션에 통합합니다. 스트리밍 및 비스트리밍 모드를 모두 지원합니다.
*   **다양한 도구**: 다음 작업을 위한 도구를 갖추고 있습니다:
    *   웹 브라우징 (`BrowserUseTool`)
    *   코드 실행 (샌드박스 환경의 Python)
    *   파일 작업 (문자열 교체 편집기)
    *   웹 검색 (Google, Bing, DuckDuckGo, Baidu)
    *   Bash 명령어 실행 (샌드박스 터미널 경유)
*   **확장 가능한 프레임워크**: 명확한 객체 지향 구조로 구축되었습니다 (`BaseAgent` -> `ReActAgent` -> `ToolCallAgent` -> `BrowserAgent` -> `Manus`).

## 📸 스크린샷

**웹 UI:**
![OpenManus 웹 UI 스크린샷 1](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753144854.png?raw=true)

**세션 관리:**
![OpenManus 웹 UI 스크린샷 2](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753160804.png?raw=true)

## 🚀 설치

더 빠른 설치와 종속성 관리를 위해 `uv` 사용을 권장합니다.

**옵션 1: `uv` 사용 (권장)**

1.  `uv`를 설치합니다 (아직 설치하지 않은 경우):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # 또는 https://github.com/astral-sh/uv 의 지침을 따르십시오
    ```
2.  리포지토리를 클론합니다:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  가상 환경을 생성하고 활성화합니다:
    ```bash
    uv venv --python 3.12 # 또는 선호하는 Python 3.10+ 버전
    source .venv/bin/activate  # Unix/macOS
    # .venv\Scripts\activate    # Windows
    ```
4.  종속성을 설치합니다:
    ```bash
    uv pip install -r requirements.txt
    ```

**옵션 2: `conda` 사용**

1.  conda 환경을 생성하고 활성화합니다:
    ```bash
    conda create -n open_manus python=3.12 -y
    conda activate open_manus
    ```
2.  리포지토리를 클론합니다:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  종속성을 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```

**Playwright 브라우저 설치 (브라우저 도구에 필요)**
```bash
playwright install --with-deps
```

## ⚙️ 설정

OpenManus를 사용하려면 사용하려는 대규모 언어 모델(LLM)에 대한 설정이 필요합니다.

1.  설정 파일 예제를 복사합니다:
    ```bash
    cp config/config.example.toml config/config.toml
    ```
2.  `config/config.toml`을 편집하여 API 키를 추가하고 설정(예: 모델 이름, 기본 URL)을 사용자 지정합니다. 에이전트는 코드에서 특정 설정이 다르게 액세스되지 않는 한 주로 `[llm.default]` 섹션의 설정을 사용합니다.
    ```toml
    # 기본 OpenAI 설정 예제
    [llm.default]
    model = "gpt-4o" # 또는 gpt-3.5-turbo 등
    api_type = "openai" # 또는 "azure", "aws"
    base_url = "https://api.openai.com/v1"
    api_key = "sk-..."  # 중요: 실제 OpenAI API 키로 교체하십시오
    max_tokens = 4096
    temperature = 0.0
    # api_version = "..." # Azure에 필요

    # 비전 모델 예제 (별도로 필요한 경우)
    # [llm.vision]
    # model = "gpt-4o"
    # ... 기타 설정 ...
    ```
    **참고:** 웹 UI에서 런타임에 이러한 설정을 재정의할 수 있지만 초기 설정은 여전히 이 파일에서 로드됩니다.

## ▶️ 애플리케이션 실행

`main.py` 스크립트를 실행하기만 하면 됩니다:

```bash
python main.py
```

이 명령은 다음을 수행합니다:
1.  Manus 에이전트를 초기화합니다.
2.  Gradio UI와 FastAPI API를 모두 호스팅하는 웹 서버를 시작합니다.
3.  기본 브라우저에서 Gradio 웹 UI를 자동으로 열려고 시도합니다 (일반적으로 `http://127.0.0.1:7860`).
4.  OpenAI 호환 API를 `http://127.0.0.1:7860/v1/chat/completions`에서 사용할 수 있도록 합니다.

터미널에 다음과 유사한 출력이 표시되어야 합니다:
```
INFO:     Starting server on http://127.0.0.1:7860
INFO:     Gradio UI available at http://127.0.0.1:7860/
INFO:     API Docs available at http://127.0.0.1:7860/docs
INFO:     OpenAI compatible API endpoint at http://127.0.0.1:7860/v1/chat/completions
INFO:     Uvicorn running on http://127.0.0.1:7860 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Attempting to open browser at http://127.0.0.1:7860
INFO:     Browser open command issued for http://127.0.0.1:7860
```

## 💻 웹 UI 사용법

*   브라우저가 자동으로 열리지 않으면 수동으로 `http://127.0.0.1:7860`으로 이동하십시오.
*   **채팅**: 하단의 메시지 상자에 요청을 입력하고 Enter 키를 누르거나 "보내기"를 클릭합니다. 에이전트의 생각 과정, 도구 사용 및 최종 응답이 채팅 창으로 스트리밍됩니다.
*   **세션 관리**:
    *   왼쪽 사이드바를 사용하여 대화를 관리합니다.
    *   "➕ 새 채팅"을 클릭하여 새 대화를 시작합니다.
    *   목록에서 세션을 선택하여 해당 기록을 로드합니다.
    *   목록 아래의 "선택한 세션 관리" 섹션을 사용하여 현재 선택된 채팅의 이름을 변경하거나 삭제합니다 (마지막 남은 채팅은 삭제할 수 없습니다).
*   **영구성**: 채팅 기록 및 세션 이름은 JSON 파일로 `chatsHistory/` 디렉토리에 자동으로 저장되며 애플리케이션을 다시 시작할 때 다시 로드됩니다.

## 🔌 API 사용법

서버는 `/v1/chat/completions`에서 OpenAI 호환 API 엔드포인트를 노출합니다. 표준 OpenAI 클라이언트 라이브러리(예: 공식 Python `openai` 라이브러리)를 사용하여 상호 작용할 수 있습니다.

**클라이언트 설정:**

*   **Base URL**: `http://127.0.0.1:7860/v1`
*   **API Key**: 비어 있지 않은 모든 문자열 (예: `"not-needed"`). 서버는 이 키를 검증하지 않습니다.
*   **Model**: 비어 있지 않은 모든 문자열 (예: `"openmanus"`). 서버는 이 모델 이름을 무시하고 설정된 Manus 에이전트를 사용합니다.

**`openai` Python 라이브러리 사용 예제:**

```python
# test_api.py
import openai

# 클라이언트 설정
client = openai.OpenAI(
    base_url="http://127.0.0.1:7860/v1",
    api_key="not-needed", # 더미 키 제공
)

# 비스트리밍 요청
try:
    completion = client.chat.completions.create(
        model="openmanus-local", # 모델 이름은 필수지만 서버에서 무시됨
        messages=[
            {"role": "user", "content": "프랑스의 수도는 어디인가요?"}
        ]
    )
    print("비스트리밍 응답:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"API 오류: {e}")

# 스트리밍 요청
try:
    stream = client.chat.completions.create(
        model="openmanus-local",
        messages=[
            {"role": "user", "content": "양자 얽힘에 대해 간략하게 설명해주세요."}
        ],
        stream=True
    )
    print("\n스트리밍 응답:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
except Exception as e:
    print(f"API 스트리밍 오류: {e}")
```

## 🙌 기여

기여를 환영합니다! issue나 pull request를 자유롭게 제출해주세요.

pull request를 제출하기 전에 변경 사항이 pre-commit 검사를 통과하는지 확인하십시오:
```bash
# pre-commit 훅 설치 (아직 설치하지 않은 경우)
pre-commit install
# 모든 파일에 대해 검사 실행
pre-commit run --all-files
```

이메일로 연락하실 수도 있습니다: mannaandpoem@gmail.com

## 💬 커뮤니티

저희 커뮤니티 그룹에 참여하세요 (세부 정보/링크가 있는 경우 기재, 없으면 이 섹션 제거 또는 업데이트).
*(커뮤니티 링크/이미지 자리 표시자)*

## 🙏 감사의 말

기반 지원을 제공해주신 [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)와 [browser-use](https://github.com/browser-use/browser-use)에 특별히 감사드립니다.

또한 [AAAJ](https://github.com/metauto-ai/agent-as-a-judge), [MetaGPT](https://github.com/geekan/MetaGPT), [OpenHands](https://github.com/All-Hands-AI/OpenHands), [SWE-agent](https://github.com/SWE-agent/SWE-agent)의 작업에도 감사드립니다.

Hugging Face 데모 공간 지원을 해주신 StepFun(阶跃星辰)에 감사드립니다.

OpenManus는 MetaGPT 커뮤니티 기여자들에 의해 구축되었습니다.

## 📜 인용

연구나 작업에 OpenManus를 사용하는 경우 다음과 같이 인용하십시오:

```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and 당신의 이름 (기여한 경우)},
  title = {OpenManus: UI 및 API를 갖춘 다재다능한 AI 에이전트를 위한 오픈 소스 프레임워크},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}
