import time


def get_now_datetime(now_time='', format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，格式为：年月日时分秒

    Args:
        now_time (str or float): 当前时间，可以是字符串表示的时间，也可以是时间戳（默认为空）
        format (str): 时间格式（默认为'%Y年%m月%d日 %H:%M:%S'）

    Returns:
        str: 格式化后的当前时间
    """
    if now_time == '':
        now_time = time.time()
    else:
        now_time = float(now_time)
    return time.strftime(format, time.localtime(now_time))


def get_before_datetime(now_date: str, span: int) -> str:
    """
    获取指定时间前的日期

    Args:
        now_date (str): 当前日期，格式为'YYYYMMDD'
        span (int): 时间跨度，单位为天数

    Returns:
        str: 指定时间前的日期，格式为'YYYYMMDD'
    """
    # 将字符串转换为时间结构
    input_date = time.strptime(now_date, '%Y%m%d')

    # 将时间结构转换为时间戳
    input_timestamp = time.mktime(input_date)

    # 计算固定时长前的时间戳（天数）
    one_month_ago_timestamp = input_timestamp - span * 24 * 60 * 60

    # 将时间戳转换为时间结构
    one_month_ago = time.localtime(one_month_ago_timestamp)

    # 将时间结构转换为字符串
    one_month_ago_str = time.strftime('%Y%m%d', one_month_ago)

    return one_month_ago_str