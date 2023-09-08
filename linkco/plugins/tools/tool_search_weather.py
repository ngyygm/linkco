import json
import time
import requests
from lxml.html import etree

from ..utils.utils_data import save_data
from ..utils.utils_chat import get_cut_history
from ..utils.utils_time import get_now_datetime
from ..utils.utils_prompt import get_history_prompt, get_rule_prompt, get_example_prompt
from ..llm.main import get_chat

wait_time = 3

class Tool():
    def __init__(self):
        self.name = '天气查询'
        self.desc = '只能提供天气查询功能。'

    def search_city(self, city_name: str) -> str:
        """
        搜索指定城市的天气URL

        Args:
            city_name (str): 城市名称

        Returns:
            str: 城市天气URL
        """
        index_url = "http://tianqi.moji.com/api/citysearch/%s" % city_name
        response = requests.get(index_url, timeout=wait_time, verify=False)
        response.encoding = "utf-8"
        city_id = json.loads(response.text).get('city_list')[0].get('cityId')
        city_url = "http://tianqi.moji.com/api/redirect/%s" % str(city_id)
        return city_url

    def parse_forecast7(self, city_url: str) -> list:
        """
        解析7天天气预报信息

        Args:
            city_url (str): 城市天气URL

        Returns:
            list: 7天天气预报列表
        """
        response = requests.get(city_url, timeout=wait_time, verify=False)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)

        week = html.xpath("//div[@class='wea_list clearfix wea_list_seven']/ul[@class='clearfix']/li/span[@class='week']/text()")
        wea = html.xpath("//div[@class='wea_list clearfix wea_list_seven']/ul[@class='clearfix']/li/span[@class='wea']/text()")
        high = html.xpath("//div[@class='wea_list clearfix wea_list_seven']/ul[@class='clearfix']/li/div[@class='tree clearfix']/p/b/text()")
        low = html.xpath("//div[@class='wea_list clearfix wea_list_seven']/ul[@class='clearfix']/li/div[@class='tree clearfix']/p/strong/text()")
        forecast7 = []
        for i in range(8):
            temp_dict = {}
            temp_dict["week"] = week[2 * i]
            temp_dict["date"] = week[2 * i + 1]
            temp_dict["daytime_weather"] = wea[2 * i]
            temp_dict["evening_weather"] = wea[2 * i]
            temp_dict["high_temperature"] = high[i]
            temp_dict["low_temperature"] = low[i]
            forecast7.append(temp_dict)
        return forecast7

    def parse(self, city_url: str) -> dict:
        """
        解析天气信息

        Args:
            city_url (str): 城市天气URL

        Returns:
            dict: 天气信息字典
        """
        response = requests.get(city_url, timeout=wait_time, verify=False)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        current_url = html.xpath("//link[@rel='alternate']/@href")[0].replace("weather", "forecast7").replace("m.moji.com", "tianqi.moji.com")
        current_city = html.xpath("//div[@class='search_default']/em/text()")[0]
        current_kongqi = html.xpath("//div[@class='left']/div[@class='wea_alert clearfix']/ul/li/a/em/text()")[0]
        current_wendu = html.xpath("//div[@class='left']/div[@class='wea_weather clearfix']/em/text()")[0]
        current_weather = html.xpath("//div[@class='wea_weather clearfix']/b/text()")[0]
        current_shidu = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/span/text()")[0]
        current_fengji = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/em/text()")[0]
        uptime = html.xpath("//strong[@class='info_uptime']/text()")[0]
        jingdian = html.xpath("//div[@class='right']/div[@class='near'][2]/div[@class='item clearfix']/ul/li/a/text()")

        temp_dict = {}
        forecast7 = self.parse_forecast7(current_url)
        temp_dict['city'] = current_city
        temp_dict['time'] = uptime
        temp_dict['air'] = current_kongqi
        temp_dict['temperature'] = current_wendu
        temp_dict['weather'] = current_weather
        temp_dict['wet'] = current_shidu
        temp_dict['wind'] = current_fengji
        temp_dict['forecast7'] = forecast7

        return temp_dict

    def get_response(self, prompt: str, history=None, system=None, model_nickname=None) -> str:
        """
        获取天气查询的回复

        Args:
            prompt (str): 输入的提示内容
            history: 对话的历史记录
            system: 系统名称
            model_nickname: 模型昵称

        Returns:
            str: 天气查询的回复
        """
        if history is not None:
            temp_history = [it for it in get_cut_history(history, 256, 3)]
        else:
            temp_history = []
        example_data = {'城市': '北京', '时间': ['2000-01-02']}

        rule_list = ['根据当前提问和历史对话，提取需要查询的城市名称和时间',
                     '城市只有一个',
                     '日期可能有多个，都要写出来']

        temp_history.append({'role': 'data', 'content': '当前时间:{}'.format(get_now_datetime())})
        role_dict = {
            'user': '问',
            'assistant': '答'
        }
        history_prompt = get_history_prompt(temp_history, role_dict)
        rule_prompt = get_rule_prompt(rule_list)
        example_prompt = get_example_prompt(json.dumps(example_data, ensure_ascii=False))

        temp_prompt = '历史对话:\n{}\n当前提问:{}\n\n要求:\n{}\n示例:\n{}'.format(history_prompt, prompt, rule_prompt, example_prompt)


        count = 5
        while count > 0:
            try:
                response = get_chat(prompt=temp_prompt,
                                    model_nickname=model_nickname)
                response_eval = eval(response)
                if model_nickname in ['giiso', 'openai']:
                    save_data(response, temp_prompt, save_path='linkco_data/date_weather.json')
                if response_eval != example_data:
                    city_name = response_eval["城市"]
                    time_list = response_eval["时间"]
                    city_url = self.search_city(city_name)
                    weather = self.parse(city_url)

                    result = "城市地点：{}" \
                             "\n实时天气：空气指数{}，气温{}摄氏度，{}，湿度{}，风向{}" \
                             "\n预报：\n".format(weather['city'], weather['air'], weather['temperature'],
                                           weather['weather'], weather['wet'], weather['wind'])
                    for f in weather['forecast7']:
                        date = get_now_datetime()[:4] + '-' + f['date'].replace('/', '-')
                        if date in time_list:
                            result = result + "{}，{}，白天{}，晚上{}，最高{}摄氏度，最低{}摄氏度\n".format(date, f['week'],
                                                                                        f['daytime_weather'],
                                                                                        f['evening_weather'],
                                                                                        f['high_temperature'],
                                                                                        f['low_temperature'])
                    return result + '\n当前时间: {}'.format(get_now_datetime(format='%Y-%m-%d %H:%M:%S'))
                else:
                    return '没找到相关地区的天气'
            except Exception as e:
                print(e)
                count = count - 1
                time.sleep(wait_time)

        return '没找到相关地区的天气'
