from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
import config_data_配置文件 as config

# 创建大语言模型实例（用于生成回答）
model = ChatOpenAI(
    base_url=config.LLM_BASE_URL,
    model=config.LLM_MODEL
)

# 创建 Chroma 向量数据库实例（用于存储和检索文档向量）
chroma = Chroma(
    collection_name=config.COLLECTION_NAME,
    embedding_function=DashScopeEmbeddings(model=config.EMBEDDING_MODEL),
    persist_directory=config.PERSIST_DIR
)

def get_chroma():
    """返回 Chroma 向量数据库实例"""
    return chroma

def get_model():
    """返回大语言模型实例"""
    return model