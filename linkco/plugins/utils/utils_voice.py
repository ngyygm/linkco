import whisper
import pyttsx3
from zhconv import convert
from ...main import setting, v2t_module, t2v_module
from .utils_system import merge_dicts


def init_v2t_model(model_name: str = 'whisper',
                   model_nickname: str = None,
                   model_config: dict = None):
    """
    初始化语音转文字模型

    Args:
        model_name (str): 模型名称，默认为'whisper'
        model_nickname (str): 模型昵称，默认为None
        model_config (dict): 模型配置参数，默认为None

    Returns:
        dict: 初始化后的语音转文字模型
    """
    temp_config = merge_dicts(setting['v2t_model'][model_name], model_config)

    model_nickname = model_nickname or model_name

    print('【当前v2t模型类型】', model_name)
    print('【当前v2t模型昵称】', model_nickname)
    print('【当前v2t模型参数】', temp_config)

    if model_nickname not in v2t_module:
        if model_name == 'whisper':
            v2t_model = whisper.load_model(temp_config['model_path'], device=temp_config['device'])
        else:
            v2t_model = whisper.load_model('large', device='cpu')

        v2t_module[model_nickname] = {
            'name': model_name,
            'module': v2t_model,
            'config': temp_config
        }

    return v2t_module[model_nickname]


def init_t2v_model(model_name: str = 'pyttsx3',
                   model_nickname: str = None,
                   model_config: dict = None):
    """
    初始化文字转语音模型

    Args:
        model_name (str): 模型名称，默认为'pyttsx3'
        model_nickname (str): 模型昵称，默认为None
        model_config (dict): 模型配置参数，默认为None

    Returns:
        dict: 初始化后的文字转语音模型
    """
    temp_config = setting['t2v_model'][model_name]
    if model_config is not None:
        for key in model_config:
            temp_config[key] = model_config[key]

    if temp_config['model_path'] == '':
        temp_config['model_path'] = temp_config['name']

    if model_nickname is None:
        model_nickname = model_name

    print('【当前t2v模型类型】', model_name)
    print('【当前t2v模型昵称】', model_nickname)
    print('【当前t2v模型参数】', temp_config)

    if model_nickname not in t2v_module.keys():
        if model_name == 'pyttsx3':
            t2v_model = pyttsx3.init()
        else:
            t2v_model = pyttsx3.init()

        t2v_module[model_nickname] = {
            'name': model_name,
            'module': t2v_model,
            'config': temp_config
        }

    return t2v_module[model_nickname]


def get_voice_to_text(audio_path: str, language: str = 'Chinese', model_nickname: str = None) -> str:
    """
    把声音文件转换成文本

    Args:
        audio_path (str): 声音文件路径
        language (str): 语言类型，默认为'Chinese'
        model_nickname (str): 模型昵称，默认为None

    Returns:
        str: 转换后的文本
    """
    if model_nickname is None:
        if len(v2t_module) > 0:
            v2t_model = v2t_module[list(v2t_module.keys())[0]]
        else:
            v2t_model = init_v2t_model()
    else:
        if model_nickname in v2t_module.keys():
            v2t_model = v2t_module[model_nickname]
        else:
            v2t_model = init_v2t_model(model_nickname=model_nickname)

    if v2t_model['name'] == 'whisper':
        audio = v2t_model['module'].transcribe(audio_path, fp16=True, language=language)
        return convert(audio['text'], 'zh-cn')
    else:
        audio = v2t_model['module'].transcribe(audio_path, fp16=True, language=language)
        return convert(audio['text'], 'zh-cn')


def get_text_to_voice(text: str, wavFile: str, model_nickname: str = None) -> bool:
    """
    把文本转换成声音文件

    Args:
        text (str): 要转换的文本
        wavFile (str): 保存的声音文件路径
        model_nickname (str): 模型昵称，默认为None

    Returns:
        bool: 转换成功返回True，否则返回False
    """
    if model_nickname is None:
        if len(t2v_module) > 0:
            t2v_model = t2v_module[list(t2v_module.keys())[0]]['module']
        else:
            t2v_model = init_t2v_model()
    else:
        if model_nickname in t2v_module.keys():
            t2v_model = t2v_module[model_nickname]['module']
        else:
            t2v_model = init_t2v_model(model_nickname=model_nickname)
    try:
        if t2v_model['name'] == 'pyttsx3':
            t2v_model['module'].save_to_file(text, wavFile)
            return True
        else:
            t2v_model.save_to_file(text, wavFile)
            return True
    except:
        return False
