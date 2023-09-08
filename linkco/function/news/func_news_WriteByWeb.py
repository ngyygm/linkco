from ...plugins.llm.main import get_chat
from ...plugins.tools import tool_search_quark


# 获取回答
def get_response(prompt, history=None, system=None):
    tool = tool_search_quark.Tool()
    results = tool.get_response(prompt, history, system, out_count=3, news_len=768)
    print('【资料】\n', results)
    results = results[:1024]
    if len(results) > 0:
        prompt = '{}\n\n根据上文内容，生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字），不可抄袭上文'.format(results, prompt)
    else:
        prompt = '生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字）'.format(results, prompt)
    return get_chat(prompt, history, system)