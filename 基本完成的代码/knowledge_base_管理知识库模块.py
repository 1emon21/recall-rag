"""
知识库
"""

import hashlib
import config_data_配置文件 as config
import os
import vector_stores_向量存储服务 as vs


def check_md5(data):
    """检查给定数据的MD5是否已在md5.txt中存在"""
    if not os.path.exists(config.md5_path):
        return True  # 文件不存在视为无重复
    with open(config.md5_path, "r", encoding="utf-8") as f:
        current_md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
        for line in f:
            if current_md5 == line.strip():
                return False  # 已存在
    return True  # 未重复

def get_sing_md5(data):
    """计算数据的MD5字符串（纯计算，不判断重复）"""
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def save_md5(md5_str):
    """将MD5字符串追加写入文件"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


class KnowledgeBaseService:
    model = vs.get_model()

    def __init__(self, data, file_name):
        self.file_name = file_name
        self.data = data
        self.spliter = None
        self.chroma =vs.get_chroma()

    def upload_by_str(self):
        """将文本数据存入向量库，并记录MD5"""
        if check_md5(self.data):          # 调用判断是否存在
            md5_val = get_sing_md5(self.data)  # 获取md5值
            self.chroma.add_texts([self.data], ids=[md5_val])#存入到向量库中
            save_md5(md5_val)             # md5值写入文件中
            return True
        else:
            print("文本已存在，跳过存储")
            return False


		
	
		
	
	