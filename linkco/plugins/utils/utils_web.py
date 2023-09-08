import re
import requests
from bs4 import BeautifulSoup


wait_time = 3


def get_real_url(url: str, headers: dict) -> str:
    """
    获取百度链接真实地址

    Args:
        url (str): 百度链接地址
        headers (dict): 请求头

    Returns:
        str: 真实地址
    """
    try:
        r = requests.get(url,
                         headers=headers,
                         allow_redirects=False,
                         timeout=wait_time,
                         verify=False)
        r.raise_for_status()  # 检查请求是否成功
        if r.status_code == 302:
            real_url = r.headers.get('Location')
        else:
            real_url = re.findall("URL='(.*?)'", r.text)[0]
        return real_url
    except (requests.RequestException, IndexError):
        return ''


def get_url_real_content(url: str) -> str:
    """
    获取网页爬取结果

    Args:
        url (str): 网页地址

    Returns:
        str: 网页内容
    """
    try:
        response = requests.get(url,
                                timeout=wait_time,
                                verify=False)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            s = re.sub(r'\n+', '\n', text)
            s = s.split('\n')
            s = [" ".join(item.split()) for item in s if len(" ".join(item.split())) > 64]
            s = '\n\n'.join(s)
            regStr = ".*?([\u4E00-\u9FA5]+).*?"
            temp_s = re.findall(regStr, s)
            temp_s = ''.join(temp_s)
            if len(temp_s) < 256:
                s = ''
            return s
        else:
            return ''
    except (requests.RequestException, IndexError):
        return ''


def get_html_content(url: str) -> str:
    """
    获取网页的 HTML 内容

    Args:
        url (str): 网页地址

    Returns:
        str: 网页的 HTML 内容
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        html_content = response.text
        return html_content
    except requests.RequestException:
        return ''


def get_json_content(url: str) -> dict:
    """
    获取网页返回的 JSON 数据

    Args:
        url (str): 网页地址

    Returns:
        dict: 解析后的 JSON 数据
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        json_data = response.json()
        return json_data
    except (requests.RequestException, ValueError):
        return {}


def download_file(url: str, save_path: str) -> bool:
    """
    下载文件到本地

    Args:
        url (str): 文件地址
        save_path (str): 保存路径

    Returns:
        bool: 下载是否成功
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    except requests.RequestException:
        return False
