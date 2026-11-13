
recall-rag

这是一个基于 LangChain 和 Streamlit 做的本地 RAG 问答系统。可以把自定义的文档放进去，然后通过自然语言提问，系统会从文档里找到相关内容并结合大模型来回答。

功能

• 本地知识库检索：用 Chroma 向量数据库对文档做语义搜索

• 多轮对话：在当前页面内保持对话记忆，刷新页面后清空，不影响文件记录

• 历史持久化：每次对话都会自动保存到文件，方便以后查看

• 流式输出：模型的回答会逐字显示，不用等全部生成完才看到

• 界面风格：仿豆包和元宝的气泡聊天样式

架构和工作流程

用户输入问题后，经过 Streamlit 前端传给 Chain 组合层。这一层会依次做这几件事：先用向量检索找到相关文档，然后把检索结果格式化成上下文，再把当前对话的历史记录注入进去，最后组装成完整的 Prompt 发给大模型。模型推理的结果以流式方式返回给前端渲染，同时异步保存到文件里。

项目结构

recall-rag/
├── data_数据文档/                存放知识库的原始文档，目前是 txt 格式
├── chroma_db_向量数据库/         向量存储，运行时会自动生成，已加入 gitignore
├── chat_histories/               对话历史文件，运行时会自动生成，已加入 gitignore
├── 基本完成的代码/
│   ├── rag_rag核心服务.py        主入口文件，Streamlit 应用
│   ├── config_data_配置文件.py   全局配置，包括检索参数和路径设置
│   ├── vector_stores_向量存储服务.py   向量库的封装
│   └── file_history_store_长期会话记忆存储服务.py  文件持久化的实现
├── .gitignore
├── requirements.txt
└── README.md

环境要求

• Python 3.9 或更高版本

• 需要一个可用的 LLM API，比如 OpenAI 或 DeepSeek

快速开始

1. 克隆仓库
   git clone https://github.com/1emon21/recall-rag.git
   cd recall-rag

2. 安装依赖
   pip install -r requirements.txt

3. 配置环境变量
   在项目根目录创建一个 .env 文件，在里面填上你的 API Key

4. 启动应用
   streamlit run 基本完成的代码/rag_rag核心服务.py

   然后在浏览器里打开 http://localhost:8501 就可以用了

License

MIT
