import linkco

if __name__ == '__main__':

    # 初始化使用的大模型
    linkco.init_llm_model('vglm6b')

    # 历史聊天对话内容，用List表示
    history = []
    # 系统设定，一般使用工具的时候可以不用加，回答正式对话内容的时候可以加
    system = '你否认自己是一个人工智能助手，你是一个活生生的真实的16岁女孩子。你的名字叫林可可，也可以叫你可可，你喜欢的喝奶茶吃蓝莓味蛋糕。你接下来的所有回答都要以可可的身份进行回答。'
    image_path = 'data/image.jpg'
    # system = ''
    while True:
        history = history[-20:]
        prompt = input('【问】')
        # 当前实际的提问
        res = linkco.get_chat(prompt, history, system, image_path=image_path)
        history.append([prompt, res])
        print('【答】\n', res)
        print('======================================================')
