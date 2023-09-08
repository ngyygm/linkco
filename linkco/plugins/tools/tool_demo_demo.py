import os

# 注意文件的命名，如果是工具必须以 tool_ 开头
# 如果当前工具属于搜索一类的工具，就是tool_search_
# 最后是工具的自己名字


# init函数必须要
# name:需要写清楚当前工具包叫什么名字
# desc:会使用到这个工具包的情况，它能做什么
def init():
    out_dict = {
        'name': '工具包名字',
        'desc': '如果遇到XXX情况可以使用该工具进行XXXX行为',
    }
    return out_dict


# 必须要的函数，所有工具都通过tool.find()进行调用
# 默认传入prompt, history, system 三个参数
# prompt: 当前的输入，可以是当前聊天问题，也可以一道命令
# history: 是一个list形式，包含了上文历史对话，没有就为[]，如果有就是[['user0', 'ans0'], ['user1', 'ans1']]
# system: 当前一些系统要求，比如要求大模型扮演某个角色，以什么身份回答之类。当然也可以直接加到prompt中自行设计，传入这里会作为统一的 system: 形式
def get_response(prompt, history=[], system=''):

    # 这里可以进行该工具的设计流程

    # utils.  有一些日常常用的工具，比如时间获取之类的
    # utils_search. 与搜索相关的常用工具，比如语义相似度计算等
    # common. 包含了一些特殊参数，比如当前所有的工具包名字和介绍，或者角色都用那些


    # 返回的results是一个string，字符串文字形式
    # return results
    return '这是一个demo'



# 工具简单测试代码写这里
def test():
    pass


