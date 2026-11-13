# recall-rag

基于 LangChain + Streamlit 的本地 RAG 问答系统，支持向量检索、多轮对话记忆与文件级历史持久化。

## 功能特性

- 📄 本地知识库检索：通过 Chroma 向量数据库对自定义文档进行语义搜索
- 💬 多轮对话：当前页面内的对话记忆（刷新后清空，不影响文件历史）
- 🗂️ 历史持久化：每次对话自动保存至文件，便于回溯
- ⚡ 流式输出：模型回答逐字显示，提升交互体验
- 🎨 清爽界面：简洁风格的气泡聊天 UI

## 核心架构与工作流程

用户输入 → Streamlit 前端 → Chain 组合层（1. 向量检索 Retriever → 2. 格式化上下文 → 3. 注入多轮历史 History → 4. Prompt 组装） → LLM 推理 → 流式输出 → 前端渲染 → 异步保存到文件 FileHistoryStore

## 项目结构

recall-rag/
├── data_数据文档/                # 知识库原始文档（.txt）
├── chroma_db_向量数据库/         # 向量存储（自动生成，已 gitignore）
├── chat_histories/               # 对话历史文件（自动生成，已 gitignore）
├── 基本完成的代码/
│   ├── rag_rag核心服务.py        # 主入口（Streamlit 应用）
│   ├── config_data_配置文件.py   # 全局配置（检索参数、路径等）
│   ├── vector_stores_向量存储服务.py  # 向量库封装
│   └── file_history_store_长期会话记忆存储服务.py  # 文件持久化
├── .gitignore
├── requirements.txt
└── README.md

## 环境要求

- Python 3.9+
- 可用的 LLM API（如 OpenAI、DeepSeek 等）

## 快速开始

1. 克隆仓库
git clone https://github.com/1emon21/recall-rag.git
cd recall-rag

2. 安装依赖
pip install -r requirements.txt

3. 配置环境变量
创建 .env 文件并填入 API Key。

4. 启动应用
streamlit run 基本完成的代码/rag_rag核心服务.py

浏览器访问 http://localhost:8501 即可使用。

## License

MIT
