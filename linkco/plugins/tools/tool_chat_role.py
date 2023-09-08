from ...main import *
from ..utils.utils_chat import get_cut_history
from ..llm.main import get_example_chat

role_path = linkco_path + 'plugins/tools/data/role/role_rule/'


def get_role_dict(role_list=None):
    defult_rule = '【text】'
    if os.path.exists(role_path + '默认规则.txt'):
        with open(role_path + '默认规则.txt', 'r', encoding='utf-8') as f:
            defult_rule = f.read()
        f.close()
        if len(defult_rule) == 0:
            defult_rule = '【text】'

    temp_dict = {}
    role_file_list = os.listdir(role_path)
    for role_name in role_file_list:
        temp_role_name = role_name.replace('.txt', '')
        if temp_role_name != '默认规则':
            with open(role_path + role_name, 'r', encoding='utf-8') as f:
                temp_data = f.read()
            f.close()
            if role_list is not None:
                if temp_role_name in role_list:
                    temp_dict[temp_role_name] = defult_rule.replace('【text】', temp_data)
            else:
                temp_dict[temp_role_name] = defult_rule.replace('【text】', temp_data)
    return temp_dict

class Tool():
    def __init__(self):
        self.name = '聊天对话'
        self.desc = '如果可以直接根据上文对话内容回答，则可使用该功能进行日常回答对话。'



    def get_response(self, prompt, history=None, system=None, role_dict_list=None, model_nickname=None):
        temp_history = get_cut_history(history, 64, 2)
        role_dict = get_role_dict(role_dict_list)
        select_list = list(role_dict.keys())
        example = json.dumps({'领域': '聊天对话'}, ensure_ascii=False)

        temp_prompt = prompt

        rule_list = ['判断当前输入属于哪个选项',
                     '只能选一个',
                     '无法判断就选聊天对话',
                     '只能输出选项中有的选项，不允许捏造']

        count = 5
        while count > 0:
            try:
                response = get_example_chat(temp_prompt, temp_history, system, example, select_list, rule_list, model_nickname)
                response = eval(response)
                role_name = response["领域"]

                if role_name not in role_dict.keys():
                    for it in role_dict.keys():
                        if role_name[:2] in it:
                            role_name = it
                if role_name not in role_dict.keys():
                    role_name = '聊天对话'
                return role_dict[role_name]
            except Exception as e:
                print(e)
                count = count - 1
                continue
        return role_dict['聊天对话']

