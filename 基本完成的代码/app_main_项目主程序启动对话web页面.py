import streamlit as st
import app_file_upload_上传文件网页服务 as upload_page
import rag_rag核心服务 as rag_page
st.title("主程序页面")
page = st.sidebar.selectbox("选择功能", ["知识库上传", "智能问答"])
if page == "知识库上传":
    upload_page.main()      # 调用上传页面的 main()
elif page == "智能问答":
    rag_page.main()