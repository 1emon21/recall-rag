# recall-rag —— 基于 LangChain + Streamlit 的本地知识库问答系统

## 项目概述

一个面向个人知识管理的轻量级 RAG（Retrieval-Augmented Generation）系统。用户上传自定义文档后，可通过自然语言进行问答，系统结合向量检索与大模型生成能力，提供精准、可追溯的回答。适用于学习笔记整理、技术文档查询等场景。

**面试关键词**：RAG、LangChain、Chroma、Streamlit、多轮对话、流式输出、会话管理、向量检索

---

## 核心技术栈

| 组件           | 技术选型                  | 选型理由 |
|----------------|--------------------------|----------|
| 前端框架       | Streamlit                | 快速搭建交互式原型，支持实时流式渲染 |
| LLM 编排框架   | LangChain                | 标准化 Chain 组合、Prompt 模板、历史管理 |
| 向量数据库     | Chroma                   | 轻量级、无需独立部署，支持本地持久化 |
| 大语言模型     | DeepSeek / OpenAI（可切换） | 成本可控，支持中文优化 |
| 历史存储       | 自定义 FileHistoryStore   | 基于文件的多会话持久化，便于离线分析 |

---

## 核心架构与工作流程


用户输入 → Streamlit 前端
              ↓
        [Chain 组合层]
     ┌─────────────────────────┐
     │ 1. 向量检索 (Retriever)  │
     │ 2. 格式化上下文          │
     │ 3. 注入多轮历史 (History) │
     │ 4. Prompt 组装           │
     └──────┬──────────────────┘
            ↓
        LLM 推理 → 流式输出 → 前端渲染
            ↓
        异步保存到文件 (FileHistoryStore)


### 关键设计决策

1. **会话隔离**：每个浏览器标签页对应独立 Session，`st.session_state.messages` 仅存储当前页面对话，刷新即清空；文件历史用于持久化备份，两者解耦。
2. **多轮记忆实现**：将当前会话的 User/AI 消息实时转换为 `HumanMessage` / `AIMessage` 列表，通过 `MessagesPlaceholder` 注入 Prompt，模型可感知完整上下文。
3. **流式输出优化**：使用 `st.chat_message().empty()` 创建占位容器，逐 chunk 追加内容并显示光标 `▌`，避免重复渲染。
4. **异常处理**：针对 `add_messages` 拼写错误、`SystemMessage` 误用、`ChatInputValue` 类型不匹配等问题进行了修复，增强健壮性。

---

## 项目亮点（面试时可展开讲）

### 1. 高效的检索增强生成
- 使用 `as_retriever` 封装 Chroma 向量库，支持相似度搜索与 MMR（最大边际相关性）去重。
- 自定义 `format_func` 将检索到的文档片段拼接为结构化上下文，避免信息冗余。

### 2. 灵活的会话管理策略
- 区分“显示历史”与“模型记忆”：界面只展示当前页面对话，模型却拥有完整上下文，兼顾隐私与性能。
- 文件存储采用追加写入模式，支持断点续传与批量导出。

### 3. 流式输出的工程实现
- 利用 LangChain 的 `.stream()` 方法实现 token 级别流式传输。
- 前端通过 `st.empty()` 动态更新，避免全页面重刷，提升用户体验。

### 4. 配置化与可扩展性
- 所有参数（检索数量 `k`、向量库路径、会话 ID 等）集中在 `config_data_配置文件.py`，便于调优。
- 支持更换底层 LLM（只需修改 `get_model()` 实现）。

---

## 难点攻克（面试必问）

### 难点1：多轮对话中历史记忆与显示分离
- **问题**：用户要求刷新页面后聊天框清空，但模型仍需记住之前对话（否则无法连续问答）。
- **方案**：引入 `st.session_state.messages` 存储当前会话（仅用于模型记忆），界面渲染只遍历它；文件历史只做持久化，不参与界面展示。
- **效果**：刷新后界面空白，但文件记录完整；模型在单次会话内保持上下文连贯。

### 难点2：LangChain 历史注入的兼容性
- **问题**：最初使用 `SystemMessage` 和 `ChatInputValue` 导致类型错误，`add_messages` 拼写错误引发运行时异常。
- **方案**：严格遵循 LangChain 消息类型规范（`HumanMessage` / `AIMessage`），修正拼写，并通过单元测试验证。
- **教训**：API 版本迭代快，需关注官方文档变更。

### 难点3：流式输出时的光标闪烁与重复渲染
- **问题**：早期代码中同时使用了 `chain.invoke` 和 `chain.stream`，导致模型被调用两次，输出重复。
- **方案**：移除 `invoke`，仅保留 `stream`；使用 `full_response += chunk` 累加内容，并在末尾添加 `▌` 模拟打字效果。
- **优化**：最终渲染时移除光标，保证界面整洁。

---

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


---

## 部署与运行

bash
1. 克隆仓库

git clone https://github.com/你的用户名/recall-rag.git
cd recall-rag

2. 安装依赖

pip install -r requirements.txt

3. 配置环境变量（创建 .env 文件，填入 API Key）

echo "OPENAI_API_KEY=sk-xxxxx" >> .env

4. 启动应用

streamlit run 基本完成的代码/rag_rag核心服务.py


浏览器访问 `http://localhost:8501` 即可开始问答。

## License
MIT
