<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

<p align="center">
  <strong>OpenManus: あなたの多機能AIエージェントフレームワーク</strong>
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README_zh.md">中文</a> | <a href="README_ko.md">한국어</a> | 日本語
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

## 👋 はじめに

Manusに触発された**OpenManus**は、様々なタスクに取り組むことができる多機能AIエージェントを構築するためのオープンソースフレームワークを提供します。招待コードなしでユーザーがアイデアを実現できるようにすることを目指しています。

このバージョンでは、インタラクティブなチャットとセッション管理のためのユーザーフレンドリーな**Web UI**（Gradioで構築）と、プログラムによるアクセスのための**OpenAI互換API**（FastAPIで構築）が統合されています。

私たちのチームメンバーである[@Xinbin Liang](https://github.com/mannaandpoem)と[@Jinyu Xiang](https://github.com/XiangJinyu)（コア作者）、そして[@Zhaoyang Yu](https://github.com/MoshiQAQ)、[@Jiayi Zhang](https://github.com/didiforgithub)、[@Sirui Hong](https://github.com/stellaHSR)（[@MetaGPT](https://github.com/geekan/MetaGPT)チーム所属）がこのプロジェクトを開始し、開発を続けています。提案、貢献、フィードバックを歓迎します！

## ✨ 特徴

*   **マルチターン会話**: コンテキストを保持した拡張対話が可能です。
*   **Web UI**: 直感的なWebインターフェースを通じてエージェントと対話できます。以下の機能が含まれます：
    *   リアルタイム更新のためのストリーミング応答。
    *   セッション管理（会話の作成、名前変更、削除、切り替え）。
    *   ローカルの`chatsHistory/`ディレクトリに自動保存される永続的なチャット履歴。
*   **OpenAI互換API**: 使い慣れたOpenAI SDK形式（`/v1/chat/completions`エンドポイント）を使用して、OpenManusをアプリケーションに統合できます。ストリーミングモードと非ストリーミングモードの両方をサポートします。
*   **多機能ツール**: 以下のタスクを実行するためのツールを備えています：
    *   Webブラウジング (`BrowserUseTool`)
    *   コード実行（サンドボックス環境でのPython）
    *   ファイル操作（文字列置換エディタ）
    *   Web検索（Google, Bing, DuckDuckGo, Baidu）
    *   Bashコマンド実行（サンドボックス端末経由）
*   **拡張可能なフレームワーク**: 明確なオブジェクト指向構造で構築されています（`BaseAgent` -> `ReActAgent` -> `ToolCallAgent` -> `BrowserAgent` -> `Manus`）。

## 📸 スクリーンショット

**Web UI:**
![OpenManus Web UI スクリーンショット 1](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753144854.png?raw=true)

**セッション管理:**
![OpenManus Web UI スクリーンショット 2](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753160804.png?raw=true)

## 🚀 インストール

より高速なインストールと依存関係管理のために`uv`の使用を推奨します。

**オプション1：`uv`を使用（推奨）**

1.  `uv`をインストールします（まだの場合）：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # または https://github.com/astral-sh/uv の指示に従ってください
    ```
2.  リポジトリをクローンします：
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  仮想環境を作成してアクティベートします：
    ```bash
    uv venv --python 3.12 # またはお好みの Python 3.10+ バージョン
    source .venv/bin/activate  # Unix/macOS
    # .venv\Scripts\activate    # Windows
    ```
4.  依存関係をインストールします：
    ```bash
    uv pip install -r requirements.txt
    ```

**オプション2：`conda`を使用**

1.  conda環境を作成してアクティベートします：
    ```bash
    conda create -n open_manus python=3.12 -y
    conda activate open_manus
    ```
2.  リポジトリをクローンします：
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  依存関係をインストールします：
    ```bash
    pip install -r requirements.txt
    ```

**Playwrightブラウザのインストール（ブラウザツールに必要）**
```bash
playwright install --with-deps
```

## ⚙️ 設定

OpenManusを使用するには、利用する大規模言語モデル（LLM）の設定が必要です。

1.  設定ファイルの例をコピーします：
    ```bash
    cp config/config.example.toml config/config.toml
    ```
2.  `config/config.toml`を編集して、APIキーを追加し、設定（モデル名、ベースURLなど）をカスタマイズします。エージェントは主に`[llm.default]`セクションの設定を使用しますが、コード内で特定の設定が異なる方法でアクセスされる場合を除きます。
    ```toml
    # デフォルトのOpenAI設定例
    [llm.default]
    model = "gpt-4o" # または gpt-3.5-turbo など
    api_type = "openai" # または "azure", "aws"
    base_url = "https://api.openai.com/v1"
    api_key = "sk-..."  # 重要：実際のOpenAI APIキーに置き換えてください
    max_tokens = 4096
    temperature = 0.0
    # api_version = "..." # Azureに必要

    # ビジョンモデルの例（別途必要な場合）
    # [llm.vision]
    # model = "gpt-4o"
    # ... その他の設定 ...
    ```
    **注意：** Web UIでは実行時にこれらの設定を上書きできますが、初期設定はこのファイルから読み込まれます。

## ▶️ アプリケーションの実行

`main.py`スクリプトを実行するだけです：

```bash
python main.py
```

このコマンドは以下を実行します：
1.  Manusエージェントを初期化します。
2.  Gradio UIとFastAPI APIの両方をホストするWebサーバーを起動します。
3.  デフォルトのブラウザでGradio Web UIを自動的に開こうとします（通常は`http://127.0.0.1:7860`）。
4.  OpenAI互換APIを`http://127.0.0.1:7860/v1/chat/completions`で利用可能にします。

ターミナルには次のような出力が表示されるはずです：
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

## 💻 Web UIの使用方法

*   ブラウザが自動的に開かない場合は、手動で`http://127.0.0.1:7860`にアクセスしてください。
*   **チャット**: 下部のメッセージボックスにリクエストを入力し、Enterキーを押すか「送信」をクリックします。エージェントの思考プロセス、ツールの使用状況、最終的な応答がチャットウィンドウにストリーミング表示されます。
*   **セッション管理**:
    *   左側のサイドバーを使用して会話を管理します。
    *   「➕ 新しいチャット」をクリックして新しい会話を開始します。
    *   リストからセッションを選択して、その履歴を読み込みます。
    *   リストの下にある「選択したセッションを管理」セクションを使用して、現在選択されているチャットの名前を変更したり削除したりします（最後のチャットは削除できません）。
*   **永続性**: チャット履歴とセッション名は、JSONファイルとして`chatsHistory/`ディレクトリに自動的に保存され、アプリケーションを再起動すると再読み込みされます。

## 🔌 APIの使用方法

サーバーは`/v1/chat/completions`でOpenAI互換のAPIエンドポイントを公開しています。標準的なOpenAIクライアントライブラリ（公式のPython `openai`ライブラリなど）を使用して対話できます。

**クライアントの設定:**

*   **Base URL**: `http://127.0.0.1:7860/v1`
*   **API Key**: 任意の空でない文字列（例：`"not-needed"`）。サーバーはこのキーを検証しません。
*   **Model**: 任意の空でない文字列（例：`"openmanus"`）。サーバーはこのモデル名を無視し、設定されたManusエージェントを使用します。

**`openai` Pythonライブラリを使用した例:**

```python
# test_api.py
import openai

# クライアントを設定
client = openai.OpenAI(
    base_url="http://127.0.0.1:7860/v1",
    api_key="not-needed", # ダミーキーを提供
)

# 非ストリーミングリクエスト
try:
    completion = client.chat.completions.create(
        model="openmanus-local", # モデル名は必須ですが、サーバーに無視されます
        messages=[
            {"role": "user", "content": "フランスの首都はどこですか？"}
        ]
    )
    print("非ストリーミング応答:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"APIエラー: {e}")

# ストリーミングリクエスト
try:
    stream = client.chat.completions.create(
        model="openmanus-local",
        messages=[
            {"role": "user", "content": "量子もつれについて簡単に説明してください。"}
        ],
        stream=True
    )
    print("\nストリーミング応答:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
except Exception as e:
    print(f"APIストリーミングエラー: {e}")
```

## 🙌 貢献

貢献を歓迎します！issueやpull requestを自由に提出してください。

pull requestを送信する前に、変更がpre-commitチェックをパスすることを確認してください：
```bash
# pre-commitフックをインストール（まだの場合）
pre-commit install
# すべてのファイルでチェックを実行
pre-commit run --all-files
```

メールでの連絡も可能です：mannaandpoem@gmail.com

## 💬 コミュニティ

私たちのコミュニティグループに参加してください（詳細/リンクがあれば記載、なければ削除または更新）。
*(コミュニティリンク/画像のプレースホルダー)*

## 🙏 謝辞

基盤となるサポートを提供してくださった[anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)と[browser-use](https://github.com/browser-use/browser-use)に特に感謝します。

また、[AAAJ](https://github.com/metauto-ai/agent-as-a-judge)、[MetaGPT](https://github.com/geekan/MetaGPT)、[OpenHands](https://github.com/All-Hands-AI/OpenHands)、[SWE-agent](https://github.com/SWE-agent/SWE-agent)の業績にも感謝します。

Hugging Faceデモスペースのサポートを提供してくださったStepFun（阶跃星辰）に感謝します。

OpenManusはMetaGPTコミュニティの貢献者によって構築されています。

## 📜 引用

研究や業務でOpenManusを使用する場合は、次のように引用してください：

```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and あなたの名前 (貢献した場合)},
  title = {OpenManus: UIとAPIを備えた多機能AIエージェントのためのオープンソースフレームワーク},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}
