import linkco

if __name__ == '__main__':

    # 需要构建向量数据库的文档地址，会自动读取这个文档下左右的文字数据
    source_folder = 'H:\\AIModel\\Giiso\\old_txt\\'

    name = "news_db"

    # 生成向量数据库
    linkco.create_vector_database(database_name=name,
                                  source_folder=source_folder,
                                  split_len=512,
                                  database_path='linkco_data/vector_database')

    # news_db
    name = "news_db"
    # 加载向量库
    linkco.load_vector_database(name)
    print('【加载向量库】')

    # 搜索最相关的文本
    query = '马塔雷拉与中国有什么关联？'

    print('【搜索最相关的文本】', query)
    result = linkco.search_from_vector_database(name, query, 3)
    for it in result:
        print(it['score'])
        print(it['content'])
        print('=========================')
