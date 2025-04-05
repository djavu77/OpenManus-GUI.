<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

<p align="center">
  <strong>OpenManus: 您的多功能 AI 智能体框架</strong>
</p>

<p align="center">
  <a href="README.md">English</a> | 中文 | <a href="README_ko.md">한국어</a> | <a href="README_ja.md">日本語</a>
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

## 👋 简介

受到 Manus 的启发，**OpenManus** 提供了一个开源框架，用于构建能够处理各种任务的多功能 AI 智能体。我们的目标是让用户无需邀请码即可将创意变为现实。

此版本集成了用户友好的 **Web UI**（使用 Gradio 构建），用于交互式聊天和会话管理，同时还提供了**兼容 OpenAI 的 API**（使用 FastAPI 构建），以便通过编程方式访问。

我们的团队成员 [@Xinbin Liang](https://github.com/mannaandpoem) 和 [@Jinyu Xiang](https://github.com/XiangJinyu)（核心作者），以及 [@Zhaoyang Yu](https://github.com/MoshiQAQ)、[@Jiayi Zhang](https://github.com/didiforgithub) 和 [@Sirui Hong](https://github.com/stellaHSR)（来自 [@MetaGPT](https://github.com/geekan/MetaGPT) 团队）发起了这个项目并持续进行开发。我们欢迎任何建议、贡献和反馈！

## ✨ 功能特性

*   **多轮对话**: 支持带有上下文记忆的扩展对话。
*   **Web UI**: 通过直观的网页界面与智能体交互，包含：
    *   流式响应，实时更新。
    *   会话管理（创建、重命名、删除、切换对话）。
    *   持久化聊天记录，自动保存在本地 `chatsHistory/` 目录中。
*   **兼容 OpenAI 的 API**: 使用熟悉的 OpenAI SDK 格式（`/v1/chat/completions` 端点）将 OpenManus 集成到您的应用程序中。支持流式和非流式模式。
*   **多功能工具集**: 配备了用于以下任务的工具：
    *   网页浏览 (`BrowserUseTool`)
    *   代码执行 (沙箱环境中的 Python)
    *   文件操作 (字符串替换编辑器)
    *   网页搜索 (Google, Bing, DuckDuckGo, Baidu)
    *   Bash 命令执行 (通过沙箱终端)
*   **可扩展框架**: 基于清晰的面向对象结构构建 (`BaseAgent` -> `ReActAgent` -> `ToolCallAgent` -> `BrowserAgent` -> `Manus`)。

## 📸 界面截图

**Web UI:**
![OpenManus Web UI 截图 1](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753144854.png?raw=true)

**会话管理:**
![OpenManus Web UI 截图 2](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753160804.png?raw=true)

## 🚀 安装指南

我们推荐使用 `uv` 以获得更快的安装速度和更好的依赖管理。

**方式一：使用 `uv` (推荐)**

1.  安装 `uv` (如果尚未安装):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # 或参考 https://github.com/astral-sh/uv 的说明
    ```
2.  克隆仓库:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  创建并激活虚拟环境:
    ```bash
    uv venv --python 3.12 # 或您偏好的 Python 3.10+ 版本
    source .venv/bin/activate  # Unix/macOS
    # .venv\Scripts\activate    # Windows
    ```
4.  安装依赖:
    ```bash
    uv pip install -r requirements.txt
    ```

**方式二：使用 `conda`**

1.  创建并激活 conda 环境:
    ```bash
    conda create -n open_manus python=3.12 -y
    conda activate open_manus
    ```
2.  克隆仓库:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```

**安装 Playwright 浏览器 (浏览器工具必需)**
```bash
playwright install --with-deps
```

## ⚙️ 配置说明

OpenManus 需要配置您打算使用的大语言模型 (LLM)。

1.  复制示例配置文件:
    ```bash
    cp config/config.example.toml config/config.toml
    ```
2.  编辑 `config/config.toml` 文件，添加您的 API 密钥并自定义设置（例如，模型名称、基础 URL）。智能体主要使用 `[llm.default]` 部分的配置，除非代码中明确指定了其他配置。
    ```toml
    # 默认 OpenAI 设置示例
    [llm.default]
    model = "gpt-4o" # 或 gpt-3.5-turbo 等
    api_type = "openai" # 或 "azure", "aws"
    base_url = "https://api.openai.com/v1"
    api_key = "sk-..."  # 重要：替换为您真实的 OpenAI API 密钥
    max_tokens = 4096
    temperature = 0.0
    # api_version = "..." # Azure 服务需要

    # 视觉模型示例 (如果单独需要)
    # [llm.vision]
    # model = "gpt-4o"
    # ... 其他设置 ...
    ```
    **注意:** 尽管 Web UI 允许在运行时覆盖这些设置，但初始配置仍然从此文件加载。

## ▶️ 运行应用

只需运行 `main.py` 脚本：

```bash
python main.py
```

此命令将：
1.  初始化 Manus 智能体。
2.  启动一个 Web 服务器，同时托管 Gradio UI 和 FastAPI API。
3.  尝试在您的默认浏览器中自动打开 Gradio Web UI (通常是 `http://127.0.0.1:7860`)。
4.  使兼容 OpenAI 的 API 在 `http://127.0.0.1:7860/v1/chat/completions` 可用。

您应该会在终端看到类似以下的输出：
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

## 💻 使用 Web UI

*   如果浏览器没有自动打开，请手动访问 `http://127.0.0.1:7860`。
*   **聊天**: 在底部的消息框中输入您的请求，然后按 Enter 或点击“发送”。智能体的思考过程、工具使用情况和最终响应将流式传输到聊天窗口中。
*   **会话管理**:
    *   使用左侧边栏管理对话。
    *   点击“➕ 新建聊天”开始一个新的对话。
    *   从列表中选择一个会话以加载其历史记录。
    *   使用列表下方的“管理选定会话”部分来重命名或删除当前选中的聊天（无法删除最后一个聊天）。
*   **持久化**: 聊天记录和会话名称会自动以 JSON 文件形式保存在 `chatsHistory/` 目录中，并在您重新启动应用程序时重新加载。

## 🔌 使用 API

服务器在 `/v1/chat/completions` 暴露了一个兼容 OpenAI 的 API 端点。您可以使用标准的 OpenAI 客户端库（例如官方的 Python `openai` 库）与其交互。

**客户端配置:**

*   **Base URL**: `http://127.0.0.1:7860/v1`
*   **API Key**: 任何非空字符串（例如 `"not-needed"`）。服务器不验证此密钥。
*   **Model**: 任何非空字符串（例如 `"openmanus"`）。服务器会忽略此名称并使用配置的 Manus 智能体。

**使用 `openai` Python 库的示例:**

```python
# test_api.py
import openai

# 配置客户端
client = openai.OpenAI(
    base_url="http://127.0.0.1:7860/v1",
    api_key="not-needed", # 提供一个虚拟密钥
)

# 非流式请求
try:
    completion = client.chat.completions.create(
        model="openmanus-local", # 模型名称是必需的，但会被服务器忽略
        messages=[
            {"role": "user", "content": "法国的首都是哪里？"}
        ]
    )
    print("非流式响应:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"API 错误: {e}")

# 流式请求
try:
    stream = client.chat.completions.create(
        model="openmanus-local",
        messages=[
            {"role": "user", "content": "简单解释一下量子纠缠。"}
        ],
        stream=True
    )
    print("\n流式响应:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
except Exception as e:
    print(f"API 流式错误: {e}")
```

## 🙌 贡献指南

我们欢迎各种贡献！请随时提交 issue 或 pull request。

在提交 pull request 之前，请确保您的更改通过 pre-commit 检查：
```bash
# 安装 pre-commit 钩子 (如果尚未安装)
pre-commit install
# 对所有文件运行检查
pre-commit run --all-files
```

您也可以通过邮件联系我们：mannaandpoem@gmail.com

## 💬 社区交流

加入我们的社区交流群组 (如果可用，请提供详细信息/链接，否则删除或更新此部分)。
*(社区链接/图片的占位符)*

## 🙏 致谢

特别感谢 [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) 和 [browser-use](https://github.com/browser-use/browser-use) 为本项目提供的基础支持！

我们同样感谢 [AAAJ](https://github.com/metauto-ai/agent-as-a-judge)、[MetaGPT](https://github.com/geekan/MetaGPT)、[OpenHands](https://github.com/All-Hands-AI/OpenHands) 和 [SWE-agent](https://github.com/SWE-agent/SWE-agent) 的工作。



OpenManus 由 MetaGPT 社区的贡献者共同构建。

## 📜 引用

如果您在研究或工作中使用 OpenManus，请按如下方式引用：

```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and 您的名字 (如果贡献)},
  title = {OpenManus: 一个带有 UI 和 API 的多功能 AI 智能体开源框架},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}
<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/mannaandpoem/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)
[![Demo](https://img.shields.io/badge/Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/lyh-917/OpenManusDemo)

# 👋 OpenManus

Manus 非常棒，但 OpenManus 无需邀请码即可实现任何创意 🛫！
**此版本新增了用户友好的 Web UI、兼容 OpenAI 的 API 接口以及独立的命令行界面。**

我们的团队成员 [@Xinbin Liang](https://github.com/mannaandpoem) 和 [@Jinyu Xiang](https://github.com/XiangJinyu)（核心作者），以及 [@Zhaoyang Yu](https://github.com/MoshiQAQ)、[@Jiayi Zhang](https://github.com/didiforgithub) 和 [@Sirui Hong](https://github.com/stellaHSR)，来自 [@MetaGPT](https://github.com/geekan/MetaGPT)团队。我们在 3 小时内完成了开发并持续迭代中！

这是一个简洁的实现方案，欢迎任何建议、贡献和反馈！

用 OpenManus 开启你的智能体之旅吧！

我们也非常高兴地向大家介绍 [OpenManus-RL](https://github.com/OpenManus/OpenManus-RL)，这是一个专注于基于强化学习（RL，例如 GRPO）的方法来优化大语言模型（LLM）智能体的开源项目，由来自UIUC 和 OpenManus 的研究人员合作开发。

## ✨ 新增功能特性

*   **多轮对话**: 支持带有上下文记忆的扩展对话。
*   **Web UI (Gradio)**: 通过直观的网页界面与智能体交互，包含：
    *   流式响应，实时更新思考和执行过程。
    *   会话管理（创建、重命名、删除、切换对话）。
    *   持久化聊天记录，自动保存在本地 `chatsHistory/` 目录中。
*   **兼容 OpenAI 的 API (FastAPI)**: 使用熟悉的 OpenAI SDK 格式（`/v1/chat/completions` 端点）将 OpenManus 集成到您的应用程序中。支持流式和非流式模式。
*   **命令行界面 (CLI)**: 提供纯粹的终端交互方式 (`cli_main.py`)。
*   **多功能工具集**: 配备了用于以下任务的工具：
    *   网页浏览 (`BrowserUseTool`)
    *   代码执行 (沙箱环境中的 Python)
    *   文件操作 (字符串替换编辑器)
    *   网页搜索 (Google, Bing, DuckDuckGo, Baidu)
    *   Bash 命令执行 (通过沙箱终端)
*   **启动器**: 使用 `main.py` 脚本通过参数启动不同的服务组合。

## 📸 界面截图

**Web UI:**
![OpenManus Web UI 截图 1](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753144854.png?raw=true)

**会话管理:**
![OpenManus Web UI 截图 2](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753160804.png?raw=true)

## 🚀 安装指南

我们提供两种安装方式。推荐使用方式二（uv），因为它能提供更快的安装速度和更好的依赖管理。

### 方式一：使用 conda

1.  创建新的 conda 环境：
    ```bash
    conda create -n open_manus python=3.12 -y
    conda activate open_manus
    ```
2.  克隆仓库：
    ```bash
    git clone https://github.com/Hank-Chromela/OpenManus-GUI.git # 注意：克隆您的 Fork
    cd OpenManus-GUI
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

### 方式二：使用 uv（推荐）

1.  安装 uv（一个快速的 Python 包管理器）：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  克隆仓库：
    ```bash
    git clone https://github.com/Hank-Chromela/OpenManus-GUI.git # 注意：克隆您的 Fork
    cd OpenManus-GUI
    ```
3.  创建并激活虚拟环境：
    ```bash
    uv venv --python 3.12
    source .venv/bin/activate  # Unix/macOS 系统
    # .venv\Scripts\activate    # Windows 系统使用
    ```
4.  安装依赖：
    ```bash
    uv pip install -r requirements.txt
    ```

### 浏览器自动化工具（必需）

```bash
playwright install --with-deps
⚙️ 配置说明
OpenManus 需要配置使用的 LLM API，请按以下步骤设置：

确保 config/config.example.toml 存在: 此文件为配置模板。
创建 config/config.toml 文件:
cp config/config.example.toml config/config.toml
编辑 config/config.toml 添加您的 API 密钥和自定义设置：
# 全局 LLM 配置 (主要使用 default)
[llm.default]
model = "gpt-4o" # 例如: gpt-4o, gpt-3.5-turbo, claude-3-opus-20240229 等
api_type = "openai" # 支持 "openai", "azure", "aws" (Bedrock) 等，取决于您的 LLM 配置
base_url = "https://api.openai.com/v1" # 替换为您的 API 地址
api_key = "sk-..."  # 重要：替换为您的真实 API 密钥！
max_tokens = 4096
temperature = 0.0
# api_version = "..." # 如果使用 Azure OpenAI，需要此项

# 可选特定 LLM 模型配置 (例如用于视觉任务)
# [llm.vision]
# model = "gpt-4o"
# base_url = "https://api.openai.com/v1"
# api_key = "sk-..."
注意: config/config.toml 文件包含敏感信息，已被添加到 .gitignore 中，不会被提交到版本库。
▶️ 运行应用
现在可以通过不同的入口文件或使用启动器脚本启动不同模式：

1. 启动 Web UI 和 API 服务器 (推荐)

运行 main.py 脚本（默认启动所有服务）：

python main.py
# 或者明确指定 all
# python main.py --service all
这将：

启动 Gradio Web UI 服务器（默认监听 http://127.0.0.1:7860）。
启动 FastAPI API 服务器（默认监听 http://0.0.0.0:8000）。
自动尝试在浏览器中打开 Web UI。
2. 仅启动 Web UI

python main.py --service ui
仅启动 Gradio Web UI 服务器（默认 http://127.0.0.1:7860）。
自动尝试打开浏览器。
3. 仅启动 API 服务器

python main.py --service api
仅启动 FastAPI API 服务器（默认 http://0.0.0.0:8000）。
4. 运行命令行界面 (CLI)

python cli_main.py
启动纯命令行交互界面。
💻 使用 Web UI
如果浏览器没有自动打开，请手动访问 http://127.0.0.1:7860。
聊天: 在底部的消息框中输入您的请求，然后按 Enter 或点击“发送”。智能体的思考过程、工具使用情况和最终响应将流式传输到聊天窗口中。
会话管理:
使用左侧边栏管理对话。
点击“➕ 新建聊天”开始一个新的对话。
从列表中选择一个会话以加载其历史记录。
使用列表下方的“管理选定会话”部分来重命名或删除当前选中的聊天（无法删除最后一个聊天）。
持久化: 聊天记录和会话名称会自动以 JSON 文件形式保存在 chatsHistory/ 目录中，并在您重新启动应用程序时重新加载。
🔌 使用 API
服务器在 /v1/chat/completions 暴露了一个兼容 OpenAI 的 API 端点（默认运行在 http://0.0.0.0:8000）。您可以使用标准的 OpenAI 客户端库（例如官方的 Python openai 库）与其交互。

客户端配置:

Base URL: http://<您的服务器IP或localhost>:8000/v1 (例如 http://127.0.0.1:8000/v1)
API Key: 任何非空字符串（例如 "not-needed"）。服务器不验证此密钥。
Model: 任何非空字符串（例如 "openmanus"）。服务器会忽略此名称并使用配置的 Manus 智能体。
使用 openai Python 库的示例:

# test_api.py
import openai

# 配置客户端 (假设 API 服务器运行在本地 8000 端口)
client = openai.OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="not-needed", # 提供一个虚拟密钥
)

# 非流式请求
try:
    completion = client.chat.completions.create(
        model="openmanus-local", # 模型名称是必需的，但会被服务器忽略
        messages=[
            {"role": "user", "content": "法国的首都是哪里？"}
        ]
    )
    print("非流式响应:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"API 错误: {e}")

# 流式请求
try:
    stream = client.chat.completions.create(
        model="openmanus-local",
        messages=[
            {"role": "user", "content": "简单解释一下量子纠缠。"}
        ],
        stream=True
    )
    print("\n流式响应:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
except Exception as e:
    print(f"API 流式错误: {e}")
🙌 贡献指南
我们欢迎任何友好的建议和有价值的贡献！可以直接创建 issue 或提交 pull request。

或通过 📧 邮件联系 @mannaandpoem：mannaandpoem@gmail.com

注意: 在提交 pull request 之前，请使用 pre-commit 工具检查您的更改。运行 pre-commit run --all-files 来执行检查。

💬 交流群
加入我们的飞书交流群，与其他开发者分享经验！

⭐ Star 数量
Star History Chart

🙏 致谢
特别感谢 anthropic-computer-use 和 browser-use 为本项目提供的基础支持！

此外，我们感谢 AAAJ，MetaGPT，OpenHands 和 SWE-agent.

我们也感谢阶跃星辰 (stepfun) 提供的 Hugging Face 演示空间支持。

OpenManus 由 MetaGPT 社区的贡献者共同构建，感谢这个充满活力的智能体开发者社区！

📜 引用我们
如果您在研究或工作中使用 OpenManus，请按如下方式引用：

@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and Hank-Chromela (UI/API Integration)},
  title = {OpenManus: An open-source framework for building general AI agents with UI and API},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}