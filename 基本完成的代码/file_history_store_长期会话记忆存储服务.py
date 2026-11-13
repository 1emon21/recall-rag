import json,os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import messages_from_dict, message_to_dict, BaseMessage
from pyarrow.lib import Sequence


class FileHistoryStore(BaseChatMessageHistory):
	def __init__(self, storage_path: str, session_id: str):
		self.stoeage_path = storage_path
		self.session_id = session_id
	# 获取消息
	@property
	def messages(self)->list[BaseMessage]:
		try:
			with open(
				os.path.join(self.stoeage_path, self.session_id),
				'r',
				encoding='utf-8',
			) as f:
				messages_data=json.load(f)
				return messages_from_dict(messages_data)
		except FileNotFoundError:
			return []
		#增加消息
	def add_massages(self,messages:Sequence[BaseMessage])->None:
		all_massages=list(self.messages)
		all_massages.extend(messages)
		serialized=[message_to_dict(message) for message in all_massages]
		file_path=os.path.join(self.stoeage_path, self.session_id)
		os.makedirs(os.path.dirname(file_path), exist_ok=True)
		with open(file_path,'w',encoding='utf-8') as f:
			json.dump(serialized,f)
	
	   #清楚消息
	def clear(self)->None:
		file_path=os.path.join(self.stoeage_path, self.session_id)
		with open(file_path,'w',encoding='utf-8') as f:
			json.dump([],f)
		