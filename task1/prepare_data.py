# -*- coding: utf-8 -*-

import json
import argparse

mock_path = "./data/1.mock_exam.json"

with open(mock_path, encoding='utf-8') as f:
    mock_data = json.load(f)
    print(f"len:{len(mock_data)}")

prompt = '''
你是一个药剂师考试能手，每次都考100分，这道题对你来说不在话下，深呼吸，并一步一步思考，并给出正确的答案。
这里有些例子，相信可以帮助你快速适应考试：
{examples}
好啦，让我们进入考试吧！！！
下面是一道{question_type}，请先详细分析问题，最后给出选项。
{question}
{option}
'''

formatted_data = ""

for item in mock_data:
    formatted_data += f"下面是一道{item['question_type']}，请先详细分析问题，最后给出选项"
    formatted_data += f"{item['question']}\n"
    for key, value in item['option'].items():
        formatted_data += f"{key}: {value}\n"
    formatted_data += f"正确答案是: {item['analysis']}\n"

def generate_query(data):
    chatgpt_query = prompt
    question = data['question']
    option = '\n'.join([k+'. '+v for k,v in data['option'].items() if v != ''])
    chatgpt_query = chatgpt_query.format_map({'examples':formatted_data,'question':question,'option':option,'question_type':data['question_type']})
    return chatgpt_query


def Prepare_data(args):
    data = []
    # 读取上传的JSON文件
    with open(args.input_path, encoding='utf-8') as f:
        data = json.load(f)

    print(f"len:{len(data)}")

    # 根据要求转换
    jsonl_data = []

    for id, item in enumerate(data):
        jsonl_data.append(
            {
                "id":id,
                "query": generate_query(item),
                "model_answer": "",
                "question_type": item['question_type'],
                "groundtruth": item['answer']
            }
        )

    # 将转换后的数据保存为JSONL文件
    with open(args.output_path, "w", encoding="utf-8") as file:
        for entry in jsonl_data:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"Prepare finished, output to '{args.output_path}'")
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare data for OpenAIGPT generation")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output JSONL file.")
    args = parser.parse_args()
    Prepare_data(args)
