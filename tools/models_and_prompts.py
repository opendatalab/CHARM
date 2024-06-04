from functools import cmp_to_key

RENAME_MODEL_DICT = {
    "GPT-3.5-turbo-1106": "GPT-3.5-1106",
    "GPT-3.5-turbo-0125": "GPT-3.5-0125",
    "GPT-4-1106-preview": "GPT-4-1106",
    "GPT-4o-2024-05-13": "GPT-4o-240513",
    "gemini-1.5-flash": "Gemini-1.5-flash",
    "llama-2-7b-chat-hf": "LLaMA-2-7B",
    "llama-2-13b-chat-hf": "LLaMA-2-13B",
    "llama-2-70b-chat-hf": "LLaMA-2-70B",
    "llama-3-8b-instruct-lmdeploy": "LLaMA-3-8B",
    "llama-3-70b-instruct-lmdeploy": "LLaMA-3-70B",
    "mistral-7b-instruct-v0.2-hf": "Mistral-7B",
    "mixtral-8x7b-instruct-v0.1": "Mixtral-8x7B",
    "vicuna-7b-v1.5-16k-hf": "Vicuna-7B-v1.5-16k",
    "vicuna-13b-v1.5-16k-hf": "Vicuna-13B-v1.5-16k",
    "chatglm3-6b-32k-hf": "ChatGLM3-6B-32k",
    "baichuan2-7b-chat-hf": "Baichuan2-7B",
    "baichuan2-13b-chat-hf": "Baichuan2-13B",
    "internlm2-chat-1.8b-turbomind": "InternLM2-1.8B",
    "internlm2-chat-7b-turbomind": "InternLM2-7B",
    "internlm2-chat-20b-turbomind": "InternLM2-20B",
    "yi-6b-chat-hf": "Yi-6B",
    "yi-34b-chat-hf": "Yi-34B",
    "yi-1.5-6b-chat-hf": "Yi1.5-6B",
    "yi-1.5-34b-chat-hf": "Yi1.5-34B",
    "deepseek-7b-chat-hf": "DeepSeek-7B",
    "deepseek-67b-chat-hf": "DeepSeek-67B",
    "deepseek-v2-chat-hf": "DeepSeek-v2",
    "qwen-7b-chat-hf": "Qwen-7B",
    "qwen-14b-chat-hf": "Qwen-14B",
    "qwen-72b-chat-hf": "Qwen-72B",
    "qwen1.5-1.8b-chat-hf": "Qwen1.5-1.8B",
    "qwen1.5-7b-chat-hf": "Qwen1.5-7B",
    "qwen1.5-14b-chat-hf": "Qwen1.5-14B",
    "qwen1.5-72b-chat-hf": "Qwen1.5-72B",
}

CN_BRANDS = [
    'chatglm3',
    'baichuan2',
    'internlm2',
    'yi',
    'deepseek',
    'qwen',
]  # 国内
EN_BRANDS = [
    'gpt',
    'llama-2',
    'llama-3',
    'vicuna',
    'mistral',
    'mixtral',
]  # 国外
CN_BRANDS = [_.lower() for _ in CN_BRANDS]
EN_BRANDS = [_.lower() for _ in EN_BRANDS]


def get_model_brand(model_name):
    model_name = model_name.lower()
    for _ in CN_BRANDS:
        if _ in model_name:
            return _
    for _ in EN_BRANDS:
        if _ in model_name:
            return _

    raise ValueError(f"Unknown model name: {model_name}")


def is_CN_LLM(model_name):
    brand = get_model_brand(model_name)
    return brand in CN_BRANDS


def is_EN_LLM(model_name):
    brand = get_model_brand(model_name)
    return brand in EN_BRANDS


def get_model_size_b(model_name):
    assert isinstance(model_name, str)
    model_name = model_name.lower()
    model_name_split = model_name.split('-')
    assert sum([int(_.endswith('b')) for _ in model_name_split]) == 1
    for _ in model_name_split:
        if _.endswith('b'):
            return int(_.replace('b', ''))


# ====================================================

PROMPT_ORDER = [
    "Direct",
    "ZH-CoT",
    "EN-CoT",
    "Translate-EN",
    "XLT",
]
PROMPT_ORDER = [_.lower() for _ in PROMPT_ORDER]

# ====================================================


def compare_model_and_prompting(src_tuple1, src_tuple2):

    assert isinstance(src_tuple1, tuple)
    assert isinstance(src_tuple2, tuple)
    assert len(src_tuple1) == len(src_tuple2)
    assert len(src_tuple1) > 1
    model_name1 = src_tuple1[0]
    model_name2 = src_tuple2[0]
    prompting1 = src_tuple1[1]
    prompting2 = src_tuple2[1]
    assert isinstance(model_name1, str)
    assert isinstance(model_name2, str)
    assert isinstance(prompting1, str)
    assert isinstance(prompting2, str)

    model_name1 = model_name1.lower()
    model_name2 = model_name2.lower()
    prompting1 = prompting1.lower()
    prompting2 = prompting2.lower()

    # if same model, sort according to prompting
    if model_name1 == model_name2:
        if prompting1 == prompting2:
            return 0
        for _ in PROMPT_ORDER:
            if _ == prompting1:
                return -1
            elif _ == prompting2:
                return 1

    # CN_LLM < EN_LLM
    if is_CN_LLM(model_name1) and is_EN_LLM(model_name2):
        return 1
    if is_EN_LLM(model_name1) and is_CN_LLM(model_name2):
        return -1

    brand1 = get_model_brand(model_name1)
    brand2 = get_model_brand(model_name2)

    if is_CN_LLM(model_name1) and is_CN_LLM(model_name2):

        # sort according to brand
        if brand1 != brand2:
            for _ in CN_BRANDS:
                if _ == brand1:
                    return -1
                elif _ == brand2:
                    return 1

        # sort by model size
        try:
            model_size1 = get_model_size_b(model_name1)
            model_size2 = get_model_size_b(model_name2)
            return -1 if model_size1 < model_size2 else 1
        except:
            return -1 if model_name1 < model_name2 else 1

    if is_EN_LLM(model_name1) and is_EN_LLM(model_name2):

        # sort according to brand
        if brand1 != brand2:
            for _ in EN_BRANDS:
                if _ == brand1:
                    return -1
                elif _ == brand2:
                    return 1

        # sort by model size
        try:
            model_size1 = get_model_size_b(model_name1)
            model_size2 = get_model_size_b(model_name2)
            return -1 if model_size1 < model_size2 else 1
        except:
            return -1 if model_name1 < model_name2 else 1


def sort_by_model_and_prompting(src_index):

    assert src_index.names[0] == 'model'
    assert src_index.names[1] == 'prompting'
    return sorted(src_index, key=cmp_to_key(compare_model_and_prompting))


def compare_prompting(prompting1, prompting2):
    assert isinstance(prompting1, str)
    assert isinstance(prompting2, str)

    prompting1 = prompting1.lower()
    prompting2 = prompting2.lower()

    if prompting1 == prompting2:
        return 0

    if prompting1 not in PROMPT_ORDER:
        return 1
    if prompting2 not in PROMPT_ORDER:
        return -1

    for _ in PROMPT_ORDER:
        if _ == prompting1:
            return -1
        elif _ == prompting2:
            return 1


def sort_by_prompting(src_list):
    return sorted(src_list, key=cmp_to_key(compare_prompting))
