
class Tool():
    def __init__(self):
        self.name = '聊天对话'
        self.desc = '如果可以直接根据上文对话内容回答，则可使用该功能进行日常回答对话。'

    def get_response(self, prompt, history=None, system=None):
        # 如果是闲聊，则不需要外部内容，直接返回空
        return ''

