# MD5 文件路径（用于记录已上传文件的哈希值，避免重复上传）
md5_path = "D:/AI大模型RAG与智能体开发/md5.txt"

# 向量数据库集合名称
COLLECTION_NAME = "knowledge_base"

# 嵌入模型名称（用于将文本转换为向量）
EMBEDDING_MODEL = "text-embedding-v4"

# 大语言模型 API 基础地址
LLM_BASE_URL = "https://llm-d0hkl8l6tbh20szt.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"

# 大语言模型名称
LLM_MODEL = "qwen3.8-flash"

# 允许上传的文件扩展名列表
ALLOWED_EXTENSIONS = ["csv", "pdf", "txt"]

# Chroma 向量数据库持久化目录（存储向量数据的文件夹）
PERSIST_DIR = "D:/AI大模型RAG与智能体开发/11月9日-11月12日/RAG项目/chroma_db_向量数据库"

# 长期会话记忆文件的存储目录（用于保存多轮对话历史，每个会话一个 JSON 文件）
HISTORY_STORAGE_PATH = "D:/AI大模型RAG与智能体开发/11月9日-11月12日/RAG项目/chat_histories"

SEARCH_KWARGS={"k": 10}

SESSION_ID="user1"