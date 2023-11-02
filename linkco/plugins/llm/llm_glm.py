from transformers import AutoModel, AutoTokenizer, AutoConfig
import torch
import os
import json
from .main import setting
from ..utils import utils_prompt


defult_device = 'cuda'


role_dict = {
        'user': '问',
        'assistant': '答'
    }

def init_model(llm_config=setting['llm']['glm']):

    global model, tokenizer, defult_device
    model_path = llm_config['model_path']
    lora_path = llm_config['lora_path']
    device = llm_config['device']
    device_id = 0
    defult_device = device
    if len(device) > 4:
        device_id = int(device[5])
        device = device[:4]


    precision = llm_config['precision']

    tokenizer = AutoTokenizer.from_pretrained(model_path,
                                              trust_remote_code=True)

    if lora_path != '':
        print('【加载微调模型】')
        # 基础的配置参数
        with open(lora_path + '\\config.json', 'r', encoding='utf-8') as f:
            lora_setting = json.load(f)
        f.close()
        # Evaluation
        # Loading extra state dict of prefix encoder
        model = AutoModel.from_pretrained(model_path,
                                          trust_remote_code=True)
        prefix_state_dict = torch.load(os.path.join(lora_path, "pytorch_model.bin"))

        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
    else:
        print('【加载原模型】')
        model = AutoModel.from_pretrained(model_path,
                                          trust_remote_code=True)

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


def get_glm_history(history):
    out_history = []
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

    return out_history


def get_chat(prompt,
             history=None,
             system=None,
             max_length=2048,
             top_p=1,
             temperature=1,
             num_beams=1,
             do_sample=True):
    global model, tokenizer, defult_device

    if model is None:
        model, tokenizer = init_model()

    # inp_prompt = utils_prompt.get_chat_prompt(prompt, history, system, role_dict)
    # print('【当前模型输入】\n', inp_prompt)
    # inputs = tokenizer([inp_prompt], return_tensors="pt")
    # inputs = inputs.to(defult_device)
    # outputs = model.generate(**inputs,
    #                          max_length=max_length,
    #                          top_p=top_p,
    #                          temperature=temperature,
    #                          num_beams=num_beams,
    #                          do_sample=do_sample)
    # outputs = outputs.tolist()[0][len(inputs["input_ids"][0]):]
    # response = tokenizer.decode(outputs)
    # response = model.process_response(response)

    temp_history = []
    if system is not None and len(system) > 0:
        temp_history = [{'role': 'system', 'content': system}]

    if history is not None and len(history) > 0:
        if isinstance(history[0], dict):
            temp_history.extend(history)
        elif isinstance(history[0], list):
            for item in history:
                temp_history.append({'role': 'user', 'content': item[0]})
                temp_history.append({'role': 'assistant', 'content': item[1]})



    response, _ = model.chat(tokenizer=tokenizer,
                             query=prompt,
                             history=temp_history,
                             max_length=max_length,
                             top_p=top_p,
                             temperature=temperature,
                             num_beams=num_beams,
                             do_sample=do_sample)



    # print('【当前模型输出】\n', response)
    # print('=============================')
    torch.cuda.empty_cache()
    return response


def get_stream_chat(prompt,
                    history=None,
                    system=None,
                    max_length=2048,
                    top_p=1,
                    temperature=1,
                    num_beams=1,
                    do_sample=True):
    global model, tokenizer, defult_device

    if model is None:
        model, tokenizer = init_model()

    # inp_prompt = utils_prompt.get_chat_prompt(prompt, history, system, role_dict)
    #
    # print('【inp_prompt】\n', inp_prompt)
    #
    # inputs = tokenizer([inp_prompt], return_tensors="pt")
    # inputs = inputs.to(defult_device)
    #
    # for outputs in model.stream_generate(**inputs,
    #                                      max_length=max_length,
    #                                      top_p=top_p,
    #                                      temperature=temperature,
    #                                      num_beams=num_beams,
    #                                      do_sample=do_sample):
    #     outputs = outputs.tolist()[0][len(inputs["input_ids"][0]):]
    #     response = tokenizer.decode(outputs)
    #     response = model.process_response(response)
    #     yield response

    temp_history = []
    if system is not None and len(system) > 0:
        temp_history = [{'role': 'system', 'content': system}]

    if history is not None and len(history) > 0:
        if isinstance(history[0], dict):
            temp_history.extend(history)
        elif isinstance(history[0], list):
            for item in history:
                temp_history.append({'role': 'user', 'content': item[0]})
                temp_history.append({'role': 'assistant', 'content': item[1]})

    for response, _ in model.stream_chat(tokenizer=tokenizer,
                                         query=prompt,
                                         history=temp_history,
                                         max_length=max_length,
                                         top_p=top_p,
                                         temperature=temperature,
                                         num_beams=num_beams,
                                         do_sample=do_sample):
        yield response