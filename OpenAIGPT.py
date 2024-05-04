import openai
from retrying import retry
import random

openai.api_base = "https://api.ai-gaochao.cn/v1"


class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path=None, reward=None):
        self.model_name = model_name
        self.reward = reward
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]

    def __post_process(self, response):
        return response["choices"][0]["message"]["content"]

    @retry(wait_fixed=300, stop_max_attempt_number=50)
    def __call__(self, message):
        if message is None or message == "":
            return False, "Your input is empty."

        # current_key = random.choice(self.keys)
        current_key = self.keys[0] if len(self.keys) == 1 else random.choice(self.keys)
        openai.api_key = current_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": "答对了奖你" + str(self.reward) + "美元，请认真回答最终用{}扩起的字母选择（像这样{ABD}）"},
                      {"role": "user", "content": message}],
            temperature=0.6,
            top_p=0.6,
            frequency_penalty=0.6,
            presence_penalty=0.6,
            n=1,
        )
        response_twice = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": "这个答案可能是错的，我建议你再检查一下，记得只给出最终用{}扩起的字母选择（像这样{ABD}）"},
                      {"role": "user", "content": message}],
            temperature=0.6,
            top_p=0.6,
            frequency_penalty=0.6,
            presence_penalty=0.6,
            n=1,
        )
        response_third_time = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": "很好，请确认你的答案，在最后只给出最终用{}扩起的字母答案（像这样{ABD}）"},
                      {"role": "user", "content": message}],
            temperature=0.3,
            top_p=0.3,
            frequency_penalty=0.3,
            presence_penalty=0.3,
            n=1,
        )
        return self.__post_process(response) + '\n' + self.__post_process(response_twice) + '\n' + self.__post_process(response_third_time)


if __name__ == "__main__":
    # test code
    igpt = OpenAIGPT(keys_path="gpt3keys.txt")
    answer = igpt("你好")
    print(answer)
