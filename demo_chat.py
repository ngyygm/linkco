import linkco

if __name__ == '__main__':

    # 这里可以设定每次创建的模型参数，具体模型有什么参数值，可以看config.json
    # model_config = {
    #     "api_key": "一般是openai模型，或者需要api_key才需要填"
    #     "model_path": "模型的本地文件地址"
    # }

    # 初始化使用的大模型
    # model_name 是当前要创建模型的类型名称，就是config.json里面的llm下的各个子类
    # model_nickname 是当前模型的别称，可以取任何名字，调用的时候用来指定
    linkco.init_llm_model(model_name='glm',
                          # model_config=model_config,
                          model_nickname='default_model')

    # 历史聊天对话内容，用List表示
    history = [{"role": "user", "content": '你好'},
               {"role": "assistant", "content": '你好，请问需要什么帮助？'},
               {"role": "observation", "content": '{这里直接放json格式的外部资料或者一些插件返回的数据就可以}'}
              ]
    # 系统设定，一般使用工具的时候可以不用加，回答正式对话内容的时候可以加
    system = '你不是一个人工智能助手，你是一个活生生的真实的16岁女孩子。你的名字叫林可可，也可以叫你可可，你喜欢的喝奶茶吃蓝莓味蛋糕。你接下来的所有回答都要以可可的身份进行回答。'

    while True:
        history = history[-20:]
        prompt = input('【问】')
        # 当前实际的提问
        res = linkco.get_chat(prompt, history, system, model_nickname='哈哈哈')
        history.extend([{"role": "user", "content": prompt},
                        {"role": "assistant", "content": res}])
        print('【答】\n', res)
        print('======================================================')
