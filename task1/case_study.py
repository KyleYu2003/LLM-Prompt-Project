import os
from prepare_data import *
from scorer import *
import sys
from OpenAIGPT_datagen_multithread import *

def clean_previous():
    os.remove("./data/2.exam_prepared.jsonl")
    os.remove("./data/3.exam_aftgpt.jsonl")
    os.remove("./data/4.score.json")
    os.remove("./data/4.wrong_ans.json")

if __name__ == '__main__':
    try:
        clean_previous()
    except:
        print("Do not need to clean.")
    
    result_dict = {}

    for reward in [0, 1, 10, 100, 1000, 10000]:
        score_sum = 0
        for _ in range(10):
            parser = argparse.ArgumentParser(description="Prepare data for OpenAIGPT generation")
            parser.add_argument("--input_path", type=str, default="./data/1.exam.json", help="Path to the input JSON file.")
            parser.add_argument("--output_path", type=str, default="./data/2.exam_prepared.jsonl", help="Path to the output JSONL file.")
            args = parser.parse_args()

            Prepare_data(args)

            parser = argparse.ArgumentParser(description="Process JSONL files concurrently.")
            parser.add_argument(
                "--model_name",
                type=str,
                default="gpt-3.5-turbo",
                help="Name of the OpenAIGPT model to use.",
            )
            parser.add_argument(
                "--keys_path",
                type=str,
                default="./gpt3keys.txt",
                help="API key for the OpenAIGPT service.",
            )
            parser.add_argument(
                "--input_path", type=str, default="./data/2.exam_prepared.jsonl", help="Path to the input JSONL file."
            )
            parser.add_argument(
                "--output_path", type=str, default="./data/3.exam_aftgpt.jsonl", help="Path to the output JSONL file."
            )
            parser.add_argument(
                "--max_workers",
                type=int,
                default=10,
                help="Maximum number of workers for concurrent processing.",
            )

            args = parser.parse_args()

            OpenAIGPT_datagen(args, reward)
            
            input_file="./data/3.exam_aftgpt.jsonl"
            wrong_ans_path="./data/4.wrong_ans.json"
            score_file="./data/4.score.json"
            score_result(input_file, wrong_ans_path, score_file)
            
            with open("./data/4.score.json", encoding='utf-8') as f:
                score_data = json.load(f)
            score = score_data["total_score"]

            score_sum += score

            clean_previous()

        result_dict[reward] = score_sum/10

    with open("./data/case_study_result.json", 'w', encoding='utf-8') as fscore:
        json.dump(result_dict, fscore, ensure_ascii=False, indent=4)