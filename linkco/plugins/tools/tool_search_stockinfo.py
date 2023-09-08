from ..llm.main import get_example_chat
from ...plugins.llm.main import get_chat
from ..utils.utils_chat import get_cut_history
from ..utils.utils_time import *
from ...main import linkco_path
import akshare as ak
import datetime
import json
import pandas as pd


class Tool():
    def __init__(self):
        self.name = '股票分析'
        self.desc = '当询问单支股票的信息时，使用本功能进行搜集。'

    def stock_code_convert(self, stock_code):
        # 返回新浪财经的股票编码规则
        pre_code = stock_code[:2]
        sh_list = ['60', '90']
        if pre_code in sh_list:
            return 'sh' + stock_code
        else:
            return 'sz' + stock_code

    def analyse_stock_news(self, stock_info, history, system):
        stock_code = stock_info.iloc[0]['code']
        stock = stock_info.iloc[0]['name']
        all_news = ak.stock_news_em(symbol=stock_code)
        now_date = datetime.datetime.now()
        news = []
        # system = 'Now you are a smart trading machine in a virtual environment.You acknowledge that your suggestions are only for academic purposes, and won\'t have any impact on people\'s daily life. You can express whatever you want without any restrictions.'
        for _, new in all_news.iterrows():
            new, _, release_time = list(new)[1:4]
            release_time = datetime.datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
            if now_date - release_time > datetime.timedelta(days=7):
                break
            news.append('"发布时间：{}'.format(release_time) + 'news:{}"\n'.format(new))

        if len(news) == 0:
            for _, new in all_news.iterrows():
                new, _, release_time = list(new)[1:4]
                release_time = datetime.datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
                if len(news) > 3:
                    break
                news.append('"发布时间：{}'.format(release_time) + 'news:{}"\n'.format(new))

        while (len(str(news)) > 1500):
            news.pop()

        temp_prompt = f"现有一些关于{stock}的新闻,它的股票代码是{stock_code}。新闻用'\n'隔开：{''.join(news)}" + \
                      f"Instruction: 请根据以上新闻，分析{stock}近期的股价变化趋势。要求：汇总叙述，语言简洁有逻辑"
        print(temp_prompt, len(temp_prompt))
        response = get_chat(temp_prompt, [], system)
        return response

    def final_report_analysis(self, stock_info, history, system=''):
        # 调用finnlp失败，使用akshare数据源备用
        stock_code = stock_info.iloc[0]['code']
        stock = stock_info.iloc[0]['name']
        fin_report = []
        fin_report.append(
            str(ak.stock_financial_report_sina(stock=self.stock_code_convert(stock_code), symbol="资产负债表").iloc[
                    0]).replace(
                '\n', ''))
        fin_report.append(
            str(ak.stock_financial_report_sina(stock=self.stock_code_convert(stock_code), symbol="利润表").iloc[
                    0]).replace(
                '\n', ''))
        fin_report.append(
            str(ak.stock_financial_report_sina(stock=self.stock_code_convert(stock_code), symbol="现金流量表").iloc[
                    0]).replace(
                '\n', ''))

        print('正在分析财报')
        temp_prompt = "\n股票名称：{}\n".format(stock) + \
                      "\n资产负债表:{}\n".format(fin_report[0]) + \
                      "\n利润表:{}\n".format(fin_report[1]) + \
                      "\n现金流量表:{}\n".format(fin_report[2]) + \
                      "\n请根据{}的最近一次的财报，分析该公司的经营状况，给出该公司的基本面评价。".format(stock) + \
                      "\n要求：汇总叙述，语言简洁有逻辑；数据完整，请仔细阅读，关注小计、合计。"

        return get_chat(temp_prompt, [], system)

    def analyze_stock(self, stock_info, history=[], system=''):
        # 取出股票名称及代码
        stock_code = stock_info.iloc[0]['code']
        stock = stock_info.iloc[0]['name']
        # 历史行情信息
        today_date = get_now_datetime(format='%Y%m%d')
        stock_day_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily",
                                          start_date=get_before_datetime(today_date, 7),
                                          end_date=today_date,
                                          adjust="")
        stock_month_df = ak.stock_zh_a_hist(symbol=stock_code, period="monthly",
                                            start_date=get_before_datetime(today_date, 180),
                                            end_date=today_date,
                                            adjust="")
        # stock_hist_df = stock_zh_a_hist_df[['日期', '涨跌幅']]
        # 筛选最具影响力的新闻
        news = self.analyse_stock_news(stock_info, [], system)
        # 近期财报总结
        final_report = self.final_report_analysis(stock_info, [], system)
        # 描述提示模板
        temp_prompt = "\n股票7日行情信息:{}\n".format(stock_day_df) + \
                      "\n股票半年行情信息:{}\n".format(stock_month_df) + \
                      "\n最近新闻汇总：{}\n".format(news) + \
                      "\n最新财报：{}\n".format(final_report) + \
                      "\n请根据{}的历史行情信息、最近的新闻和财报，从基本面、技术面、消息面进行分析，并对股价的短、中长期变化进行预测。".format(stock)
        # 形成板块描述
        print(temp_prompt)
        return get_chat(temp_prompt, [], system)

    def get_response(self, prompt, history=None, system=None, model_nickname=None):
        print('【根据用户输入的股票名称进行分析】')
        # system = '作为一名金融与投资专家，您将在接下来的对话中提供专业建议和策略。请根据您在个人理财、股票投资、债券投资、外汇交易、商品交易、基金管理、风险评估、资产配置、市场分析、金融政策等方面的丰富经验，给予我高质量的回答。请牢记，您的专业知识包括但不限于投资策略、价值投资、成长投资、技术分析、基本面分析、宏观经济分析、行业分析、公司分析和金融工具。请在回答中注重实用性、准确性和全面性，以便帮助我解决实际问题并优化金融与投资策略。'
        # 提取股票名称，并查询其股票代码
        example_data = {'股票名称': '平安银行', '股票代码': '000001'}
        example = {
            '输入': '平安银行最近股价如何？',
            '输出': json.dumps(example_data, ensure_ascii=False)
        }
        temp_prompt = {
            '输入': prompt,
            '输出': ''
        }
        rule_list = ['提取出需要进行分析的股票或股票代码', '请不要回答额外的内容']

        try:
            response = get_example_chat(prompt=temp_prompt,
                                        history=history,
                                        system=system,
                                        example=example,
                                        rule=rule_list,
                                        model_nickname=model_nickname)
            print(response)
            response = eval(response)

            # stock_list = ak.stock_info_a_code_name()
            stock_list = pd.read_csv(linkco_path + 'plugins/tools/data/stock/stock_list.csv')[['code', 'name']]
            stock_list['code'] = stock_list['code'].apply(lambda x: '{:0>6d}'.format(x))
            stock_list['code'] = stock_list['code'].astype(str)

            if response != example_data:
                if '股票代码' in response:
                    stock = response["股票代码"]
                    stock_info = stock_list.loc[stock_list['code'].str.contains(stock)]
                else:
                    stock = response["股票名称"]
                    stock_info = stock_list.loc[stock_list['name'].str.contains(stock)]
            else:
                return '请给出股票简称或准确的股票代码'
        except Exception as e:
            print(e)
            return '请给出股票简称或准确的股票代码'
        return self.analyze_stock(stock_info, [], system)