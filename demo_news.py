# -*- coding: utf-8 -*-
import linkco
from function.news import func_news_WriteByDB, func_news_WriteByWeb

# 基于网络搜索的新闻生成demo，只要输入一个标题即可
if __name__ == '__main__':
    # 初始化使用的大模型
    linkco.init_llm_model('glm')

    # 构建测试数据集
    history = []
    system = "作为一名新闻与媒体专家，您将在接下来的对话中提供专业建议和见解。请根据您在新闻采编、新闻报道、新闻传播、媒体战略、数字媒体、社交媒体、公关策略、广告策略、媒体法律与伦理、新闻评论、新闻分析等方面的丰富经验，给予我高质量的回答。请牢记，您的专业知识包括但不限于新闻业态、新闻传播渠道、媒体创新、媒体分析、新闻价值、信息传播和媒体市场。请在回答中注重实用性、客观性和深度，以便帮助我解决实际问题并优化新闻与媒体策略。"

    # 加载功能
    while True:
        prompt = input('【问】\n')

        # 这个是用夸克网络搜索生成新闻
        res = func_news_WriteByWeb.get_response(prompt, [], system)
        print('【夸克网络搜索答】\n', res)

        # 这是用本地数据库
        database = linkco.load_vector_database('linkco_data/vector_database/news_db0')
        res = func_news_WriteByDB.get_response(prompt=prompt,
                                               system=system,
                                               database=database)

        print('【本地数据库答】\n', res)
    # 中华田园猫崛起了