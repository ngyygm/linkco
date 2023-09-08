# -*- coding: utf-8 -*-
import linkco
import time

# 基于网络搜索的新闻生成demo，只要输入一个标题即可
if __name__ == '__main__':
    # 初始化使用的大模型
    linkco.init_llm_model('glm26b')

    db_name = 'news_db'
    db_path = 'linkco_data/vector_database'
    print('【加载向量库】', db_name)
    linkco.load_vector_database(db_name, db_path)

    # 构建测试数据集
    history = []
    system = "作为一名新闻与媒体专家，您将在接下来的对话中提供专业建议和见解。请根据您在新闻采编、新闻报道、新闻传播、媒体战略、数字媒体、社交媒体、公关策略、广告策略、媒体法律与伦理、新闻评论、新闻分析等方面的丰富经验，给予我高质量的回答。请牢记，您的专业知识包括但不限于新闻业态、新闻传播渠道、媒体创新、媒体分析、新闻价值、信息传播和媒体市场。请在回答中注重实用性、客观性和深度，以便帮助我解决实际问题并优化新闻与媒体策略。"

    # 加载功能
    while True:
        prompt = input('【问】\n')

        # 这个是用夸克网络搜索生成新闻
        # res = linkco.func_news_WriteByWeb.get_response(prompt, [], system)
        start = time.time()
        # 这是用本地数据库
        res = linkco.func_news_WriteByDB.get_response(db_name=db_name,
                                                      prompt=prompt,
                                                      system=system)
        print(time.time() - start)
        print('【答】\n', res)
    # 中华田园猫崛起了
    # 人工智能大会开幕
    # 2023世界人工智能大会以“智联世界 元生无界”为主题,以“高端化、国际化、专业化、市场化、智能化”为特色,将集聚全球智能领域最具影响力的科学家和企业家,以及相关政府的领导人,围绕智能领域的
