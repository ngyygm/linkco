import os
import json
import torch
import faiss
import pickle
from tqdm import tqdm

import numpy as np
import sentence_transformers as st

from ...main import setting
from .utils_file import read_file
from .utils_data import get_text_split

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# embedding 模型
default_model = None
default_model_config = None


# 初始化文本向量化模型
def init_vector_model(model_config=None):
    temp_config = setting['vector_model']
    if model_config is not None:
        for key in model_config:
            temp_config[key] = model_config[key]
    temp_model = st.SentenceTransformer(
        temp_config['model_path'], device=temp_config['device'])
    return temp_model


# 设置默认的vector_model
def set_default_vector_model(model_config=None):
    global default_model, default_model_config

    if default_model is None or (model_config is not None and model_config != default_model_config):
        default_model_config = model_config or setting['vector_model']
        default_model = init_vector_model(default_model_config)


# 将文本转换为向量
def get_text_to_vector(text: str or list, model=None) -> np.ndarray:
    global default_model
    if model is None:
        if default_model is None:
            set_default_vector_model()
        temp_model = default_model
    elif isinstance(model, str):
        temp_model = init_vector_model(model)
    else:
        temp_model = model

    return temp_model.encode(text)


# 保存向量库到本地文件
def save_vector_to_database(database: dict, database_path: str):

    temp_database_path = os.path.join(database_path)
    if not os.path.exists(temp_database_path):
        os.mkdir(temp_database_path)
    with open(os.path.join(temp_database_path, 'texts.pkl'), 'wb') as f:
        pickle.dump(database['texts'], f)
    faiss.write_index(database['index'], os.path.join(temp_database_path, 'index.index'))


# 【增】从文本创建向量并将其添加到向量库中
# 【增】从文本创建向量并将其添加到向量库中
def add_vector(database: dict, data):
    if not isinstance(data, (str, dict)):
        raise ValueError("Invalid data format. Expected 'str' or 'dict'.")

    if isinstance(data, str):
        if data not in database['texts']:
            # print('【数据不存在，添加】', data)
            vector = get_text_to_vector(data)
            database['index'].add(np.array([vector]))
            database['texts'].append(data)
    elif isinstance(data, dict):
        if 'texts' not in data or 'vectors' not in data:
            raise ValueError("Invalid data format for dict. 'texts' and 'vectors' keys are required.")

        texts = data['texts']
        vectors = data['vectors']

        if len(texts) != len(vectors):
            raise ValueError("Invalid data format for dict. 'texts' and 'vectors' should have the same length.")

        if len(vectors) > 0:
            database['index'].add(np.array(vectors))
            database['texts'].extend(texts)
    return database


# 【删】删除向量库中的向量
def delete_vector(database: dict, data):

    index = database['index']
    texts = database['texts']

    if isinstance(data, str):
        vector = get_text_to_vector(data)
    elif isinstance(data, np.ndarray):
        vector = data
    else:
        raise ValueError(f"delete_vector Input data mistake!")

    D, I = index.search(np.array([vector]), 1)
    remove_index = int(I[0][0])
    num_vectors = index.ntotal

    if np.array_equal(index.reconstruct(remove_index), vector):
        vectors = np.empty((num_vectors, len(vector)), dtype=np.float32)
        for i in range(num_vectors):
            vector = index.reconstruct(i)
            vectors[i] = vector
        del texts[remove_index]
        vectors = np.delete(vectors, remove_index, axis=0)
        index = faiss.IndexFlatL2(len(vector))
        index.add(vectors)
        database = {'index': index, 'texts': texts}
    else:
        raise ValueError(f"数据库中没找到: {data}")

    return database
    # vector_dbs[database_name] = {'index': index, 'texts': texts}


# 【改】更新向量库中的向量
def update_vector_to_database(database: dict, old_text: str, new_text: str):
    return add_vector(delete_vector(database, old_text), new_text)


# 【查】查询最相关的文本
def search_from_vector_database(database: dict, query: str, top_k: int = 1, min_score: int = 1000):

    query_vector = get_text_to_vector(query)

    index = database['index']
    texts = database['texts']

    D, I = index.search(np.array([query_vector]), top_k)
    # print('【D】', D)
    # print('【I】', I)
    return [{'score': D[0][idx], 'content':texts[i]} for idx, i in enumerate(I[0]) if D[0][idx] < min_score]


# 加载向量库
def load_vector_database(database_path: str):
    if not os.path.exists(database_path):
        raise ValueError(f"Cannot find the database {database_path}")
    database = {
        'index': faiss.read_index(os.path.join(database_path, 'index.index')),
        'texts': pickle.load(open(os.path.join(database_path, 'texts.pkl'), 'rb'))
    }

    return database


# 合并向量库
def merge_database(database0: dict, database1: dict):
    # 把 database1中的数据增量到database0中

    # vector = get_text_to_vector('test')
    # dimension = len(vector)
    # database = {
    #     'index': faiss.IndexFlatL2(dimension),
    #     'texts': [],
    # }

    database0['index'].merge_from(database1['index'])
    database0['texts'].extend(database1['texts'])

    # database['index'].merge_from(database1['index'])
    # database['texts'].extend(database1['texts'])

    return database0




# 创建数据库
def create_vector_database(source_folder: str or list,
                           database_path: str,
                           split_len: int = 512):
    # print('【source_folder】', source_folder)
    vector = get_text_to_vector('test')
    dimension = len(vector)
    database = {
                'index': faiss.IndexFlatL2(dimension),
                'texts': [],
            }

    all_files = []
    if isinstance(source_folder, str):
        source_folder_path = os.path.join(os.getcwd(), source_folder)
        if os.path.isdir(source_folder_path):
            for root, dirs, files in os.walk(source_folder_path):
                for file in files:
                    all_files.append(os.path.join(root, file))
        elif os.path.isfile(source_folder_path):
            all_files.append(source_folder_path)
    else:
        for item in source_folder:
            source_folder_path = os.path.join(os.getcwd(), item)
            if os.path.isdir(source_folder_path):
                for root, dirs, files in os.walk(source_folder_path):
                    for file in files:
                        all_files.append(os.path.join(root, file))
            elif os.path.isfile(source_folder_path):
                all_files.append(source_folder_path)

    batch_size = 512

    range_count = int(len(all_files) / batch_size)
    if range_count == 0:
        range_count = 1
    for i in tqdm(range(range_count)):
        all_datas = []
        for file_path in all_files[i * batch_size: (i + 1) * batch_size]:
            try:
                datas = get_text_split(read_file(file_path), split_len)
                all_datas.extend(datas)
            except:
                continue
        all_datas = list(set(all_datas))

        # 排序
        all_datas.sort(key=len)

        temp_model = init_vector_model()
        temp_vector_dbs = {
            'texts': all_datas,
            'vectors': get_text_to_vector(all_datas, temp_model),
        }

        database = add_vector(database, temp_vector_dbs)
        save_vector_to_database(database, database_path)
    return database

