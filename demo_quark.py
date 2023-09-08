# -*- coding: utf-8 -*-
import linkco

# 基于网络搜索的新闻生成demo，只要输入一个标题即可
if __name__ == '__main__':
    history = [{"role": "user", "content": '你好'},
               {"role": "assistant", "content": '你好，请问需要什么帮助？'},
               ]

    # 初始化使用的大模型
    # linkco.init_llm_model('glm6b')
    tool = linkco.tool_search_quark.Tool()
    prompt = input('【问】\n')
    results = tool.get_response(prompt, if_query=True)
    print('【资料】\n', results)
    print('【history】\n', history)

    # 蔡徐坤发生什么事情了，他是谁？