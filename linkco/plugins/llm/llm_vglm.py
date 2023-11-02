from transformers import AutoModel, AutoTokenizer, AutoConfig
import torch
import os
import json
from .main import setting
defult_device = 'cuda'

model = ''
tokenizer = ''

def init_model(llm_config=setting['llm']['vglm']):
    model_path = llm_config['model_path']
    lora_path = llm_config['lora_path']
    device = llm_config['device']
    if len(device) > 4:
        device_id = int(device[5])
        device = device[:4]
    elif len(device) == 4:
        device_id = 0
    precision = llm_config['precision']

    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path,
                                              trust_remote_code=True,
                                              use_auth_token=True,
                                              local_files_only=True)
    config = AutoConfig.from_pretrained(model_path,
                                        trust_remote_code=True,
                                        use_auth_token=True,
                                        local_files_only=True)

    if lora_path != '':
        print('【加载微调模型】')
        # 基础的配置参数
        with open(lora_path + '\\config.json', 'r', encoding='utf-8') as f:
            lora_setting = json.load(f)
        f.close()
        config.pre_seq_len = lora_setting['pre_seq_len']
        # Evaluation
        # Loading extra state dict of prefix encoder
        model = AutoModel.from_pretrained(model_path,
                                          config=config,
                                          trust_remote_code=True,
                                          use_auth_token=True,
                                          local_files_only=True)
        prefix_state_dict = torch.load(os.path.join(lora_path, "pytorch_model.bin"))

        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
    else:
        print('【加载原模型】')
        model = AutoModel.from_pretrained(model_path,
                                          config=config,
                                          trust_remote_code=True,
                                          use_auth_token=True,
                                          local_files_only=True)

        # 根据设备执行不同的操作
    if device == 'cpu':
        # 如果是cpu，不做任何操作
        precision = 'fp32'
        pass
    elif device == 'cuda':
        # 如果是gpu，把模型移动到显卡
        if not (precision.startswith('fp16i') and torch.cuda.get_device_properties(0).total_memory < 1.4e+10):
            model = model.cuda(device_id)
    else:
        # 如果是其他设备，报错并退出程序
        print('Error: 不受支持的设备')
        exit()
        # 根据精度执行不同的操作
    if precision == 'fp16':
        # 如果是fp16，把模型转化为半精度
        model = model.half()
    elif precision == 'fp32':
        # 如果是fp32，把模型转化为全精度
        model = model.float()
    elif precision.startswith('fp16i'):
        # 如果是fp16i开头，把模型转化为指定的精度
        # 从字符串中提取精度的数字部分
        bits = int(precision[5:])
        # 调用quantize方法，传入精度参数
        model = model.quantize(bits)
        if device == 'cuda':
            model = model.cuda(device_id)
        model = model.half()
    elif precision.startswith('fp32i'):
        # 如果是fp32i开头，把模型转化为指定的精度
        # 从字符串中提取精度的数字部分
        bits = int(precision[5:])
        # 调用quantize方法，传入精度参数
        model = model.quantize(bits)
        if device == 'cuda':
            model = model.cuda(device_id)
        model = model.float()
    else:
        # 如果是其他精度，报错并退出程序
        print('Error: 不受支持的精度')
        exit()
    model = model.eval()

    return model, tokenizer


def get_chat(prompt,
             history=[],
             system='',
             image_path=None,
             max_length=2048,
             top_p=1, temperature=1,
             num_beams=1, do_sample=True):
    global model, tokenizer
    if model == '':
        model, tokenizer = init_model()

    out_history = []
    if len(system) > 0 and system is not None:
        out_history.append([system,
                            '好的，我会遵循以上内容。'])
    role_flag = 0
    temp_his = []
    for it in history:
        if role_flag == 0 and it['role'] == 'user':
            temp_his.append(it['content'])
            role_flag = 1
        elif role_flag == 1 and it['role'] == 'assistant':
            temp_his.append(it['content'])
            role_flag = 0
        if len(temp_his) == 2:
            out_history.append(temp_his)
            temp_his = []

    if image_path is not None and len(prompt) == 0:
        prompt = '请详细描述这张图片。'

    response, _ = model.chat(tokenizer,
                             query=prompt,
                             image_path=image_path,
                             history=out_history,
                             max_length=max_length,
                             top_p=top_p,
                             temperature=temperature,
                             num_beams=num_beams,
                             do_sample=do_sample)
    torch.cuda.empty_cache()
    return response


