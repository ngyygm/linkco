import linkco

if __name__ == '__main__':

    # 马塔雷拉与中国有什么关联？
    text0 = '马塔雷拉与中国有什么关联？'
    text1 = '阿根廷与中国有什么关联？'

    a_vector = linkco.get_text_to_vector(text0)
    print(a_vector.size, a_vector)

    b_vector = linkco.get_text_to_vector(text1)
    print(b_vector.size, b_vector)


    # 向量数据库文件地址
    database_path0 = "linkco_data/vector_database/ttxt_db"

    # 加载向量库
    database = linkco.load_vector_database(database_path0)
    print('【加载向量库】')

    # 还有一些别的操作方法，详细可以跳转进去看看其他的一些方法
    # 【增】从文本创建向量并将其添加到向量库中
    database = linkco.add_vector(database, text0)
    database = linkco.add_vector(database, text1)

    print('\n\n===================添加向量====================')
    for it in database['texts']:
        print(it)
        print('---------------------------')

    # 【删】删除向量库中的向量

    print('\n\n====================删除向量===================')
    database = linkco.delete_vector(database, text0)
    for it in database['texts']:
        print(it)
        print('---------------------------')

    # 【改】更新向量库中的向量
    database = linkco.update_vector_to_database(database, text1, '你好')
    print('\n\n====================修改向量===================')
    for it in database['texts']:
        print(it)
        print('---------------------------')


    # 保存向量
    database_path1 = "linkco_data/vector_database/ttxt_db1"
    linkco.save_vector_to_database(database, database_path1)
    print('\n\n====================保存向量===================')





    # 【合并】合并两个向量数据库
    # 加载向量库
    database0 = linkco.load_vector_database(database_path0)
    database1 = linkco.load_vector_database(database_path1)
    print('【加载向量库】')

    database_result = linkco.merge_database(database0, database1)
    print('\n\n====================合并向量===================')
    for it in database_result['texts']:
        print(it)
        print('---------------------------')

    # 保存向量
    new_database_path = "linkco_data/vector_database/news_db_1010"
    linkco.save_vector_to_database(database_result, new_database_path)
    print('\n\n====================保存向量===================')



