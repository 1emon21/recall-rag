"""
基于Streamlit完成WEB网页上传服务
"""
#导入Streamlit_流式应用框架包
import streamlit as st
import knowledge_base_管理知识库模块  as kb
import config_data_配置文件 as config
def main():
    # 创建标题(title)
    st.title("知识库更新服务")
    # 上传文件按钮
    uploaded_file = st.file_uploader("上传文件", type=config.ALLOWED_EXTENSIONS)
    # 判断是否上传了文件
    if uploaded_file is not None:
        # 拿到用户所上传的文件
        try:
            file_data = uploaded_file.getvalue().decode("utf-8")
        except UnicodeDecodeError:  # 编码不对时执行以下代码
            st.error("文件编码不支持，请上传 UTF-8 编码的文本文件")
            st.stop()  # 文件数据字符串类型
        file_name = uploaded_file.name  # 文件名称
        # 将内容解析为向量存入向量库中
        kbs = kb.KnowledgeBaseService(file_name, file_data)
        if kbs.upload_by_str():
            st.success("上传成功")
        else:
            st.warning("内容重复，未上传")
if __name__ == '__main__':
    main()


     
