[中文](README.md "中文")

## Linkco 框架使用介绍说明

这是一个关于Linkco框架的使用介绍说明。Linkco框架提供了一套丰富的功能和插件，以帮助您开发和定制各种应用程序。

### 当前支持功能：

* **大模型加载**：支持加载多个大型模型，包括OpenAI模型、ChatGLM-6B模型和VisualGLM-6B模型。
* **角色选择**：提供了42个不同领域的角色引导，包括聊天对话、金融、医疗、宠物、新闻等。
* **插件拓展**：支持插件的拓展，包括天气查询、网络搜索等功能。
* **语音识别**：集成了Wishper语音转文字接口，实现语音识别功能。
* **功能实现**：提供了一些功能实现的示例，如新闻资讯生成、无人机指令控制、智能聊天策略等。

## 目录

1. [function](#function)
   1.1 [chat](#func_chat)
   1.2 [drones](#func_drones)
   1.3 [news](#func_news)
2. [plugins](#plugins)
   2.1 [llm](#plug_llm)
   2.2 [role](#plug_role)
   2.3 [tool](#plug_tool)
   2.4 [utils](#plug_utils)
3. config.json
4. main.py

### 1. function

这个目录包含了Linkco框架的各种功能实现代码。下面是该目录中的几个子目录及其功能的简要说明：

#### 1.1 chat
在这个子目录中，您可以找到与聊天对话相关的功能实现代码。

#### 1.2 drones
这个子目录中包含了与无人机指令控制相关的功能实现代码。

#### 1.3 news
在这个子目录中，您可以找到与新闻资讯生成相关的功能实现代码。

### 2. plugins

这个目录包含了Linkco框架的各种插件代码。下面是该目录中的几个子目录及其功能的简要说明：

#### 2.1 llm
在这个子目录中，您可以找到与语言模型加载相关的插件代码。

#### 2.2 role
这个子目录中包含了与角色选择相关的插件代码。

#### 2.3 tools
在这个子目录中，您可以找到一些工具类插件的代码，如天气查询和网络搜索等。

##### main.py

这个文件提供了一些与工具相关的函数，用于获取工具字典和判断使用哪个工具。

* `get_tool_dict(tool_list: list = None) -> dict`：
  该函数用于获取工具字典，可以根据指定的工具列表返回相应的工具字典。
  
  ```python
  tool_list = ['tool_1', 'tool_2']
  tool_dict = get_tool_dict(tool_list)
  ```

* `get_switch_tool(prompt: str, history: str = None, system: str = None, tool_dict_list: list = None, model_nickname: str = None) -> list`：
  该函数用于判断使用哪个工具。根据输入的提示内容、对话的历史记录、系统名称、工具字典列表和模型昵称，判断并返回应该使用的工具列表。
  
  ```python
  prompt = "今天天气如何？"
  history = "历史对话记录"
  system = "系统名称"
  tool_dict_list = ['tool_1', 'tool_2']
  model_nickname = "模型昵称"
  tool_list = get_switch_tool(prompt, history, system, tool_dict_list, model_nickname)
  ```

以上是该文件中的函数功能的简要说明。您可以根据需要使用这些函数来获取工具字典和判断使用哪个工具。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。

如果您有其他问题或需要进一步的帮助，请随时提问。


#### 2.4 utils

这个子目录中包含了一些辅助工具类的插件代码。

##### utils_chat.py

这个文件提供了一些与对话相关的工具函数。

* `get_cut_history(history, cut_len: int = -1, his_len: int = -1, max_length: int = 8192) -> list or None`：
  该函数用于缩减历史对话内容，以减少字数消耗。它接收历史对话列表以及一些可选参数，如截断每个对话内容的长度、历史对话长度和最大总长度。返回缩减后的历史对话列表。如果输入的历史对话为None，则返回None。
  
  ```python
  history = [
      {'role': 'user', 'content': '用户的对话内容1'},
      {'role': 'assistant', 'content': '助手的回复内容1'},
      {'role': 'user', 'content': '用户的对话内容2'},
      {'role': 'assistant', 'content': '助手的回复内容2'}
  ]
  cut_len = 50
  his_len = 2
  max_length = 8192
  result = get_cut_history(history, cut_len, his_len, max_length)
  print(result)  # 输出：缩减后的历史对话列表
  ```

* `get_relate_history(prompt: str, history_data_list: list) -> list`：
  该函数用于判断与问题有关的历史对话，并截取与当前的提示相关的历史对话信息。它接收当前的问题和历史对话列表作为输入，并返回与当前问题相关的历史对话信息列表。
  
  ```python
  prompt = "当前的问题"
  history_data_list = [
      ("历史问题1", "历史回答1"),
      ("历史问题2", "历史回答2"),
      ("历史问题3", "历史回答3")
  ]
  result = get_relate_history(prompt, history_data_list)
  print(result)  # 输出：与当前问题相关的历史对话信息列表
  ```

* `get_item_history(query: str, response: str) -> list`：
  该函数用于获取一问一答形式的历史对话列表。它接收用户提问和机器人回答作为输入，并返回历史对话列表。
  
  ```python
  query = "用户提问"
  response = "机器人回答"
  result = get_item_history(query, response)
  print(result)  # 输出：历史对话列表
  ```

* `get_update_history(query: str, response: str, history: list) -> list`：
  该函数用于获取更新的历史对话列表。它接收用户提问、机器人回答和当前的历史对话列表作为输入，并返回更新后的历史对话列表。
  
  ```python
  query = "用户提问"
  response = "机器人回答"
  history = [
      {'role': 'user', 'content': '用户的对话内容1'},
      {'role': 'assistant', 'content': '助手的回复内容1'}
  ]
  result = get_update_history(query, response, history)
  print(result)  # 输出：更新后的历史对话列表
  ```

您可以根据需要使用这些工具函数来处理对话数据。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


##### tool_search_weather.py

这个文件实现了一个天气查询工具，可以根据指定的城市名称获取天气信息。

* `Tool`类：
  * `__init__(self)`：构造函数，初始化工具的名称和描述。
  * `search_city(self, city_name: str) -> str`：搜索指定城市的天气URL，并返回城市天气URL。
  * `parse_forecast7(self, city_url: str) -> list`：解析7天天气预报信息，并返回7天天气预报列表。
  * `parse(self, city_url: str) -> dict`：解析天气信息，并返回天气信息字典。
  * `get_response(self, prompt: str, history=None, system=None, model_nickname=None) -> str`：根据输入的提示内容，获取天气查询的回复。
  
  ```python
  tool = Tool()
  city_name = "北京"
  city_url = tool.search_city(city_name)
  forecast = tool.parse_forecast7(city_url)
  weather_info = tool.parse(city_url)
  
  print(forecast)  # 输出7天天气预报列表
  print(weather_info)  # 输出天气信息字典
  
  prompt = "北京明天天气如何？"
  response = tool.get_response(prompt)
  print(response)  # 输出天气查询的回复
  ```

您可以使用这个天气查询工具来获取指定城市的天气信息。如果您有其他问题或需要进一步的帮助，请随时提问。




#### utils_data.py

这个文件提供了一些用于数据处理和计算的工具函数。

* `save_data(response: str, prompt: str, history: str, system: str, save_path: str = llm_response_path) -> None`：
  该函数将生成的回复内容、输入的提示内容、对话的历史记录以及系统名称保存到指定路径的JSON文件中。默认保存路径为`llm_response_path`。
  
  ```python
  response = "这是生成的回复内容"
  prompt = "这是输入的提示内容"
  history = "这是对话的历史记录"
  system = "系统名称"
  save_data(response, prompt, history, system)
  ```

* `get_remove_noun(inp_data: str) -> str`：
  该函数用于从输入数据中去除所有的标点符号，并返回处理后的结果。
  
  ```python
  inp_data = "这是包含标点符号的输入数据！"
  result = get_remove_noun(inp_data)
  print(result)  # 输出：这是包含标点符号的输入数据
  ```

* `get_hash(inp_data: str) -> str`：
  该函数用于计算输入数据的哈希值，并返回结果。
  
  ```python
  inp_data = "这是输入数据"
  result = get_hash(inp_data)
  print(result)  # 输出：计算得到的哈希值
  ```

您可以根据需要使用这些工具函数来处理数据和进行计算。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


#### utils_file.py

这个文件提供了一些用于读取和写入文件的工具函数。

* `read_csv_file(file_path: str) -> dict`：
  该函数用于读取CSV文件并将数据保存到字典中，并返回字典对象。
  
  ```python
  file_path = "data.csv"
  data = read_csv_file(file_path)
  print(data)  # 输出：保存了CSV文件数据的字典
  ```

* `read_xlsx_file(file_path: str, sheet_name: str = None) -> dict`：
  该函数用于读取xlsx文件并将数据保存到字典中，并返回字典对象。
  
  ```python
  file_path = "data.xlsx"
  sheet_name = "Sheet1"  # 可选参数，指定要读取的Sheet名称
  data = read_xlsx_file(file_path, sheet_name)
  print(data)  # 输出：保存了xlsx文件数据的字典
  ```

* `save_dict_to_csv_file(data: dict, save_path: str) -> None`：
  该函数用于将字典数据保存为CSV文件。
  
  ```python
  data = {"name": ["John", "Jane"], "age": [25, 30]}
  save_path = "data.csv"
  save_dict_to_csv_file(data, save_path)
  ```

* `save_dict_to_xlsx_file(data: dict, save_path: str, sheet_name: str = 'Sheet1') -> None`：
  该函数用于将字典数据保存为xlsx文件。
  
  ```python
  data = {"name": ["John", "Jane"], "age": [25, 30]}
  save_path = "data.xlsx"
  sheet_name = "Sheet1"  # 可选参数，指定要写入的Sheet名称
  save_dict_to_xlsx_file(data, save_path, sheet_name)
  ```

* `save_dict_to_json_file(data: dict, save_path: str) -> None`：
  该函数用于将字典数据保存为JSON文件。
  
  ```python
  data = {"name": "John", "age": 25}
  file_path = "data.json"
  save_dict_to_json_file(data, file_path)
  ```

* `read_file(file_path: str) -> str`：
  该函数用于读取各种类型的文件，并提取文本内容。支持的文件格式包括PDF、TXT、DOCX和PPTX。
  
  ```python
  file_path = "document.pdf"
  text = read_file(file_path)
  print(text)  # 输出：从文件中提取的文本内容
  ```

您可以根据需要使用这些工具函数来处理文件和提取文本内容。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


#### utils_prompt.py

这个文件提供了一些用于生成提示字符串的工具函数，用于构建对话系统的输入提示。

* `get_select_prompt(select: list or dict or str) -> str`：
  该函数根据选择项生成相应的提示字符串。支持列表、字典和字符串类型的选择项。
  ```python
  select = ['选项1', '选项2', '选项3']
  result = get_select_prompt(select)
  print(result)  # 输出：'[{}] - 选项1\n[{}] - 选项2\n[{}] - 选项3\n'

  select = {'选项1': '描述1', '选项2': '描述2', '选项3': '描述3'}
  result = get_select_prompt(select)
  print(result)  # 输出：'[{}] - 描述1\n[{}] - 描述2\n[{}] - 描述3\n'
  ```

* `get_system_prompt(system: str) -> str`：
  该函数根据系统信息生成系统信息的提示字符串。
  ```python
  system = '这是系统信息'
  result = get_system_prompt(system)
  print(result)  # 输出：'【SYSTEM START】\n这是系统信息\n【SYSTEM END】\n\n'
  ```

* `get_history_prompt(history: list) -> str`：
  该函数根据历史对话记录生成历史对话的提示字符串。
  ```python
  history = [{'role': 'user', 'content': '用户对话内容'}, {'role': 'assistant', 'content': '助手回复内容'}]
  result = get_history_prompt(history)
  print(result)  # 输出：'[Round 0]\n[user]:用户对话内容\n[assistant]:助手回复内容\n----------\n'
  ```

* `get_query_prompt(query: dict or str, response: str = '') -> str`：
  该函数根据当前问题和回复内容生成当前问题的提示字符串。
  ```python
  query = {'问题1': '回答1', '问题2': '回答2'}
  response = '这是回复内容'
  result = get_query_prompt(query, response)
  print(result)  # 输出：'[问题1]:回答1\n[问题2]:回答2\n'
  ```

* `get_example_prompt(example: list or dict or str, history: list or None) -> str`：
  该函数根据示例内容和历史对话记录生成示例的提示字符串。
  ```python
  example = ['示例1', '示例2', '示例3']
  history = [{'role': 'user', 'content': '用户对话内容'}, {'role': 'assistant', 'content': '助手回复内容'}]
  result = get_example_prompt(example, history)
  print(result)  # 输出：'[Round 0]\n[user]:用户对话内容\n[assistant]:助手回复内容\n示例1\n示例2\n示


#### utils_system.py

这个文件提供了一些通用的工具函数。

* `load_module(module_path)`：
  该函数用于动态加载指定路径下的模块，并返回加载的模块对象。
  
  ```python
  module_path = "my_module"
  module = load_module(module_path)
  ```

* `merge_dicts(dict1: dict, dict2: dict) -> dict`：
  该函数用于合并两个字典，并返回合并后的结果。
  
  ```python
  dict1 = {"key1": "value1"}
  dict2 = {"key2": "value2"}
  merged_dict = merge_dicts(dict1, dict2)
  print(merged_dict)  # 输出：{"key1": "value1", "key2": "value2"}
  ```

您可以根据需要使用这些工具函数来处理数据、进行计算和加载模块。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


#### utils_time.py

这个文件提供了用于处理时间相关操作的工具函数。

* `get_now_datetime(now_time='', format='%Y年%m月%d日 %H:%M:%S') -> str`：
  该函数用于获取当前时间，并返回格式化后的时间字符串。可以通过`now_time`参数指定特定的时间，也可以使用当前时间。默认的时间格式为`'%Y年%m月%d日 %H:%M:%S'`。
  
  ```python
  now = get_now_datetime()
  print(now)  # 输出：当前时间的格式化字符串，如：2023年06月20日 15:30:45
  ```

  ```python
  specific_time = 1624158945  # 时间戳表示的特定时间
  now = get_now_datetime(specific_time, format='%Y-%m-%d %H:%M:%S')
  print(now)  # 输出：特定时间的格式化字符串，如：2021-06-20 15:30:45
  ```

您可以使用这个工具函数来获取当前时间或特定时间，并将其格式化为所需的时间字符串。如果您需要进一步了解函数的用法和参数，请查看函数的注释。


#### utils_vector.py

这个文件提供了一些用于文本向量化和向量库操作的工具函数。

* `init_vector_model(emb_config=None)`：
  该函数用于初始化文本向量化模型，并返回模型对象。可以通过传入`emb_config`参数来配置模型的参数。
  
  ```python
  model = init_vector_model()
  ```

* `get_text_to_vector(text: str) -> np.ndarray`：
  该函数用于将文本转换为向量表示，返回一个NumPy数组。
  
  ```python
  text = "这是要转换为向量的文本"
  vector = get_text_to_vector(text)
  ```

* `save_to_vector_database(database_name: str)`：
  该函数用于将向量库保存到本地文件。向量库的名称由`database_name`指定。
  
  ```python
  database_name = "vector_database"
  save_to_vector_database(database_name)
  ```

* `add_to_vector_database(database_name: str, text: str)`：
  该函数用于从文本创建向量并将其添加到指定的向量库中。向量库的名称由`database_name`指定。
  
  ```python
  database_name = "vector_database"
  text = "这是要添加到向量库的文本"
  add_to_vector_database(database_name, text)
  ```

* `delete_from_vector_database(database_name: str, vector: np.ndarray)`：
  该函数用于从指定的向量库中删除指定的向量。向量库的名称由`database_name`指定，要删除的向量由`vector`指定。
  
  ```python
  database_name = "vector_database"
  vector = np.array([0.1, 0.2, 0.3])  # 要删除的向量
  delete_from_vector_database(database_name, vector)
  ```

* `update_to_vector_database(database_name: str, old_text: str, new_text: str)`：
  该函数用于更新向量库中的向量。向量库的名称由`database_name`指定，要更新的向量由`old_text`指定，更新后的向量由`new_text`指定。
  
  ```python
  database_name = "vector_database"
  old_text = "要更新的旧文本"
  new_text = "更新后的新文本"
  update_to_vector_database(database_name, old_text, new_text)
  ```

* `search_from_vector_database(database_name: str, query: str)`：
  该函数用于在指定的向量库中查询与给定查询文本最相关的文本。向量库的名称由`database_name`指定，查询文本由`query`指定。
  
  ```python
  database_name = "vector_database"
  query = "查询文本"
  result = search_from_vector_database(database_name, query)
  ```

* `load_vector_database(database_name: str)`：
  该函数用于加载指定名称的向量库。向量库的名称由`database_name`指定。
  
  ```python
  database_name = "vector_database"
  load_vector_database(database_name)
  ```

* `get_score(inp_data, tar_data)`：
  该函数用于计算两个文本之间的相似度分数。`inp_data`为输入文本，`tar_data`为目标文本。返回相似度分数。
  
  ```python
  inp_data = "输入文本"
  tar_data = "目标文本"
  score = get_score(inp_data, tar_data)
  ```

* `get_score_list(q, inp_datas, min_score=0.50)`：
  该函数用于计算一个列表中的文本与给定问题文本的相似度分数，并按照分数排序。`q`为问题文本，`inp_datas`为待计算相似度的文本列表，`min_score`为相似度的最小阈值，默认为0.50。返回排序后的文本列表。
  
  ```python
  q = "问题文本"
  inp_datas = ["文本1", "文本2", "文本3"]
  result_list = get_score_list(q, inp_datas)
  ```

您可以根据需要使用这些工具函数来处理文本向量化和向量库操作。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


#### utils_voice.py

这个文件提供了一些用于语音处理的工具函数。

* `init_v2t_model(model_name: str = 'whisper', model_nickname: str = None, model_config: dict = None) -> dict`：
  该函数用于初始化语音转文字模型。您可以指定模型名称、模型昵称和模型配置参数。返回一个字典，包含初始化后的语音转文字模型相关信息。
  
  ```python
  v2t_model = init_v2t_model(model_name='whisper', model_nickname='my_v2t_model', model_config={'param1': value1, 'param2': value2})
  ```

* `init_t2v_model(model_name: str = 'pyttsx3', model_nickname: str = None, model_config: dict = None) -> dict`：
  该函数用于初始化文字转语音模型。您可以指定模型名称、模型昵称和模型配置参数。返回一个字典，包含初始化后的文字转语音模型相关信息。
  
  ```python
  t2v_model = init_t2v_model(model_name='pyttsx3', model_nickname='my_t2v_model', model_config={'param1': value1, 'param2': value2})
  ```

* `get_voice2text(audio_path: str, language: str = 'Chinese', model_nickname: str = None) -> str`：
  该函数用于将声音文件转换为文本。您需要提供声音文件的路径、语言类型和可选的模型昵称。返回转换后的文本。
  
  ```python
  audio_path = "声音文件路径"
  text = get_voice2text(audio_path, language='Chinese', model_nickname='my_v2t_model')
  ```

* `get_text2voice(text: str, wavFile: str, model_nickname: str = None) -> bool`：
  该函数用于将文本转换为声音文件并保存到指定路径。您需要提供要转换的文本、保存的声音文件路径和可选的模型昵称。返回一个布尔值，表示转换是否成功。
  
  ```python
  text = "要转换的文本"
  wavFile = "保存的声音文件路径"
  success = get_text2voice(text, wavFile, model_nickname='my_t2v_model')
  ```

您可以根据需要使用这些工具函数来进行语音转换和处理。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。


#### utils_web.py

这个文件提供了一些用于网络请求和数据处理的工具函数。

* `get_real_url(url: str, headers: dict) -> str`：
  该函数用于获取百度链接的真实地址。接受一个百度链接地址和请求头作为参数，返回真实地址。
  
  ```python
  url = "https://www.baidu.com"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
  }
  real_url = get_real_url(url, headers)
  print(real_url)  # 输出：百度链接的真实地址
  ```

* `get_url_real_content(url: str) -> str`：
  该函数用于获取网页的爬取结果。接受一个网页地址作为参数，返回网页内容。
  
  ```python
  url = "https://www.example.com"
  content = get_url_real_content(url)
  print(content)  # 输出：网页的内容
  ```

* `get_html_content(url: str) -> str`：
  该函数用于获取网页的 HTML 内容。接受一个网页地址作为参数，返回网页的 HTML 内容。
  
  ```python
  url = "https://www.example.com"
  html_content = get_html_content(url)
  print(html_content)  # 输出：网页的 HTML 内容
  ```

* `get_json_content(url: str) -> dict`：
  该函数用于获取网页返回的 JSON 数据。接受一个网页地址作为参数，返回解析后的 JSON 数据。
  
  ```python
  url = "https://www.example.com/api/data"
  json_data = get_json_content(url)
  print(json_data)  # 输出：解析后的 JSON 数据
  ```

* `download_file(url: str, save_path: str) -> bool`：
  该函数用于下载文件到本地。接受文件地址和保存路径作为参数，返回下载是否成功的布尔值。
  
  ```python
  url = "https://www.example.com/files/sample.pdf"
  save_path = "/path/to/save/sample.pdf"
  success = download_file(url, save_path)
  if success:
      print("文件下载成功")
  else:
      print("文件下载失败")
  ```

您可以根据需要使用这些工具函数进行网络请求、数据处理和文件下载操作。如果您需要进一步了解每个函数的具体用法和参数，请查看相应的函数注释。



### config.json

这是Linkco框架的配置文件，您可以根据需要进行相应的配置调整。

这个文件是一个配置文件，包含了一些参数和路径的设置。下面是其中的一些重要配置项：

* `"llm"`：这是一个字典，包含了不同的语言模型的配置信息。其中包括了OpenAI模型、VisualGLM-6B模型、ChatGLM-6B模型等。每个模型都有一个名称、相应的模型路径、设备、精度等信息。

* `"vector_model"`：这是用于文本向量化的模型的配置信息。包括了模型名称、模型路径和设备。

* `"v2t_model"`：这是语音转文字模型的配置信息。目前只有一个配置项，使用了名为"whisper"的模型，具体的模型路径和设备配置在其他地方。

* `"t2v_model"`：这是文字转语音模型的配置信息。目前只有一个配置项，使用了名为"pyttsx3"的模型，具体的模型路径和设备配置在其他地方。

* `"save_data"`：这是一些保存数据的路径配置项。包括了基础路径、向量数据库路径、缓存数据路径和LLM回复数据路径等。

您可以根据需要修改这些配置项以适应您的环境和需求。如果您需要进一步了解每个配置项的具体含义和用法，请参考相应的注释或文档。
