import linkco

if __name__ == '__main__':

    # docx, pdf, pptx, txt, csv, xlsx

    # 读取docx
    data = linkco.read_docx_file('./data/demo.docx')
    print('【docx】\n', data)

    # 读取pdf
    data = linkco.read_pdf_file('./data/demo.pdf')
    print('【pdf】\n', data)

    # 读取pptx
    data = linkco.read_pptx_file('./data/demo.pptx')
    print('【pptx】\n', data)

    # 读取txt
    data = linkco.read_txt_file('./data/demo.txt')
    print('【txt】\n', data)

    # 读取csv
    data = linkco.read_csv_file('./data/demo.csv')
    print('【csv】\n', data)

    # 读取xlsx
    data = linkco.read_xlsx_file('./data/demo.xlsx')
    print('【xlsx】\n', data)

    # 智能读取，自动判断读取什么格式的数据
    data = linkco.read_file('./data/demo.docx')
    print('【read】\n', data)