import streamlit as st
import time

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
import vector_stores_向量存储服务 as vs
import config_data_配置文件 as config
import file_history_store_长期会话记忆存储服务 as fsh

def main():
	# 创建标题
	st.title("用户提问")
	#页面css样式
	# ===== 美化界面样式（类似豆包/元宝风格） =====
	st.markdown("""
	<style>
	    /* 全局背景 */
	    .stApp {
	        background-color: #f7f8fa;
	    }
	    /* 主容器最大宽度 */
	    .block-container {
	        max-width: 800px;
	        padding-top: 2rem;
	    }
	    /* 标题样式 */
	    h1 {
	        color: #1a1a2e;
	        font-weight: 600;
	        text-align: center;
	        margin-bottom: 1.5rem;
	    }
	    /* 聊天消息容器 - 去除默认边距 */
	    [data-testid="stChatMessage"] {
	        background-color: transparent !important;
	        padding: 0.2rem 0;
	        border: none;
	    }
	    /* 隐藏默认头像（如果不想显示头像） */
	    [data-testid="stChatMessageAvatar"] {
	        display: none;
	    }
	    /* 如果想保留头像但更精致，可注释上面，改用下面的样式
	    [data-testid="stChatMessageAvatar"] img {
	        width: 32px;
	        height: 32px;
	        border-radius: 50%;
	        object-fit: cover;
	    }
	    */
	    /* 用户消息气泡 */
	    [data-testid="stChatMessage"][data-st-message-role="user"] [data-testid="stChatMessageContent"] {
	        background-color: #d9e4ff;   /* 浅蓝色，类似元宝 */
	        color: #1a1a2e;
	        border-radius: 18px 18px 4px 18px;
	        padding: 12px 16px;
	        margin-left: auto;
	        margin-right: 0;
	        max-width: 75%;
	        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
	        font-size: 15px;
	        line-height: 1.5;
	    }
	    /* 助手消息气泡 */
	    [data-testid="stChatMessage"][data-st-message-role="assistant"] [data-testid="stChatMessageContent"] {
	        background-color: #ffffff;
	        color: #1a1a2e;
	        border-radius: 18px 18px 18px 4px;
	        padding: 12px 16px;
	        margin-left: 0;
	        margin-right: auto;
	        max-width: 80%;
	        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
	        border: 1px solid #eaeaea;
	        font-size: 15px;
	        line-height: 1.5;
	    }
	    /* 输入框样式 */
	    .stChatInputContainer {
	        background-color: white;
	        border-radius: 24px;
	        padding: 4px 8px;
	        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
	        border: 1px solid #e0e0e0;
	    }
	    .stChatInputContainer:focus-within {
	        border-color: #4a90d9;
	        box-shadow: 0 0 0 2px rgba(74,144,217,0.2);
	    }
	    .stChatInputContainer input {
	        font-size: 15px;
	        padding: 8px 12px;
	        border: none;
	        outline: none;
	        background: transparent;
	    }
	    /* 发送按钮（如果有） */
	    button[data-testid="baseButton-secondary"] {
	        background-color: #4a90d9;
	        color: white;
	        border-radius: 20px;
	        padding: 6px 14px;
	        font-size: 14px;
	        border: none;
	    }
	    /* 滚动条美化 */
	    ::-webkit-scrollbar {
	        width: 6px;
	    }
	    ::-webkit-scrollbar-thumb {
	        background: #c1c1c1;
	        border-radius: 3px;
	    }
	</style>
	""", unsafe_allow_html=True)
	# 选择模型
	model = vs.get_model()
	# 链接外存储向量库
	vector_store = vs.get_chroma()
	# 创建提示词
	prompt = ChatPromptTemplate.from_messages(
		[
			("system", "以我提供的资料为主，简介和专业的回答用户的问题，参考资料:{context}"),
			MessagesPlaceholder("history"),
			("user", "用户提问：{input}")
		]
	)
	# 将向量存储包装成检索器
	retriever = vector_store.as_retriever(search_kwargs=config.SEARCH_KWARGS)
	
	def format_func(docs):
		if not docs:
			return "无相关查考资料"
		format_str = "["
		for doc in docs:
			format_str += doc.page_content
		format_str += "]"
		return format_str
	#创建历史类实例
	store = fsh.FileHistoryStore(storage_path=config.HISTORY_STORAGE_PATH, session_id=config.SESSION_ID)
	# 调用chain
	chain = (
			{"input": RunnablePassthrough(), "context": retriever | format_func, "history":lambda  x: store.messages}
			| prompt
			| model
			| StrOutputParser()
	)
	# 创建消息容器
	user_str = st.chat_input("请输入你的问题：")
	#初始化session_state
	if "messages" not in st.session_state:
		st.session_state.messages = []
		
	if user_str:
		# 用户提问的问题
		user_text = str(user_str)
		# 显示当前会话的所有消息
		for msg in st.session_state.messages:
			with st.chat_message(msg["role"]):
				st.markdown(msg["content"])
	
		# 添加用户消息并显示
		st.session_state.messages.append({"role": "user", "content": user_text})
		with st.chat_message("user"):
			st.markdown(user_text)

		with st.spinner("思考中....."):
			res = chain.invoke(user_str)
			# 添加历史消息
			store.add_massages([HumanMessage(content=user_text), AIMessage(content=res)])
			#模型回答流式输出
			assistant_msg = st.chat_message("assistant").empty()
			full_response = ""
			for chunk in chain.stream(user_text):
				full_response += chunk  # chunk 本身就是字符串，直接拼接
				assistant_msg.markdown(full_response + "▌")  # 显示到网页
			assistant_msg.markdown(full_response)
			# 保存助手消息到 session_state
			st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':
    main()

	
