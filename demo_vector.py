import linkco

if __name__ == '__main__':

    database_path = "linkco_data/vector_database/news_db_0912"


    # # 生成向量数据库
    # # 需要构建向量数据库的文档地址，会自动读取这个文档下的文字文档数据
    # source_folder = 'H:\\AIModel\\Giiso\\ttxt\\data-9-21\\'
    #
    # database = linkco.create_vector_database(source_folder=source_folder,
    #                                           database_path=database_path,
    #                                           split_len=512)

    # 加载数据库
    database = linkco.load_vector_database(database_path)

    while True:
        # 搜索最相关的文本
        # '马塔雷拉与中国有什么关联？'
        query = input('请输入需要查询的语句：')

        print('【搜索最相关的文本】', query)
        # 【查】数据库搜索操作
        result = linkco.search_from_vector_database(database, query, 3)
        for it in result:
            print(it['score'])
            print(it['content'])
            print('---------------------------')
        print('=======================================')
