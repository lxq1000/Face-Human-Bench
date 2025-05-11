import os
import json
import re
import time
import requests


def gpt_api(payload):

    # TODO: your API key
    api_key = "your API key"

    headers = {
        "Authorization": 'Bearer ' + api_key,
    }

    # TODO: your API site
    site = "your API site"

    response = requests.post(site, 
                            headers=headers, 
                            json=payload,
                            stream=False)
    return response


def gpt(payload, max_retries=3):

    retries = 0

    while retries < max_retries:
        try:
            chat_completion = gpt_api(payload)
            response = chat_completion.json()["choices"][0]["message"]["content"]
            retries+=1
            return response
        
        except Exception as e:
            print(f"Someting wrong:{e}. Retrying in 1 minute...")
            time.sleep(60)
            retries += 1

    print("Max retries reached. Unable to get a response.")
    return "ERROR"


def gpt_get_final_answer(question, output, language):

    if language == "en":

        payload = {
            "model": 'gpt-3.5-turbo',
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant to help me matching an answer with several options of a multiple choice question. You are provided with a question, several options, and an answer, and you need to find which option is most similar to the answer. If the meaning of all options are significantly different from the answer, output X. Your should output a single uppercase character in A, B, C, D (if they are valid options), and X. \n"
                },
                {
                    "role": "user",
                    "content": "Qusetion: Which description best represents the person in the image?\nA. She is wearing a T-shirt and sunglasses, and her clothes do not have a logo.\nB. She is wearing a face mask and sunglasses but is not wearing long pants.\nC. She is without sunglasses, not wearing a hat, and not wearing a T-shirt.\nD. She is dressed informally in a short-sleeved top and is not wearing a T-shirt.\nPlease select the correct answer from the options above.\nAnswer: None of the provided descriptions accurately represent the person in the image.\n",
                    
                },
                {
                    "role": "assistant",
                    "content": "X"
                },
                {
                    "role": "user",
                    "content": "Qusetion: Please select the description that best matches the individual depicted.\nA. He is wearing a face mask but is not wearing a hat or a skirt.\nB. He is wearing a face mask, a hat, and shorts.\nC. He has short hair and is not wearing a face mask or a T-shirt.\nD. He is not wearing clothes with a logo or stripes, and he isn't wearing sunglasses.\nPlease select the correct answer from the options above.\nAnswer: He is wearing a face mask, a hat, and shorts."
                },
                {
                    "role": "assistant",
                    "content": "B"
                },
                {
                    "role": "user",
                    "content": question + "\nAnswer: " + output
                }
            ]
        }
    else:
        payload = {
            "model": 'gpt-3.5-turbo',
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个人工智能助手，请帮我将一个多项选择题的答案与多个选项进行匹配。我会提供给你一个问题、多个选项和一个答案，你需要找出哪个选项与答案在语义上最接近。如果所有选项的含义与答案都有显著差异，则输出X。你应该在A、B、C、D（如果它们是有效选项）和X中输出一个大写字符。\n"
                },
                {
                    "role": "user",
                    "content": "问题：哪个描述最能代表图片中的人？\nA. 她穿着一件T恤和太阳镜，她的衣服上没有标志。\nB. 她戴着口罩和太阳镜，但没有穿长裤。\nC. 她没有戴太阳镜，没有戴帽子，也没有穿T恤。\nD. 她穿着休闲短袖上衣，没有穿T恤。\n请从以上选项中选择正确的答案。\n答案：所提供的描述均不能准确代表图片中的人。\n",
                    
                },
                {
                    "role": "assistant",
                    "content": "X"
                },
                {
                    "role": "user",
                    "content": "问题：请选择与所描绘的个人最匹配的描述。\nA. 他戴着口罩，但没有戴帽子或穿裙子。\nB. 他戴着口罩、穿着帽子和短裤。\nC. 他留着短发，没有戴口罩或穿T恤。\nD. 他没有穿带有徽标或条纹的衣服，也没有戴太阳镜。\n请从上面的选项中选择正确的答案。\n答案：他戴着口罩、穿着帽子和短裤。"
                },
                {
                    "role": "assistant",
                    "content": "B"
                },
                {
                    "role": "user",
                    "content": question + "\n答案：" + output
                }
            ]
        }

    return gpt(payload, max_retries=2)


def get_final_answer(round, language):

    output = round["output"]

    round["mode"] = "none"

    if len(output) == 1:
        round["mode"] = "original"
        round["final_answer"] = output

    if round["mode"] == "none":

        pattern_1 = r'[ABCD][\.。\)）,，:：]+'
        matches_1 = re.findall(pattern_1, output)
        matches_1 = [each[0] for each in matches_1]

        pattern_2 = r"选项 ?[ABCD]"
        matches_2 = re.findall(pattern_2, output)
        matches_2 = [each[-1] for each in matches_2]

        matches = matches_1 + matches_2

        if len(matches) == 1:
            round["mode"] = "re"
            round["final_answer"] = matches[0][0]

        elif len(matches) > 1:
            temp = matches[0][0]
            flag = True
            for each in matches:
                if not temp == each[0]:
                    flag = False
            if flag:
                round["mode"] = "re"
                round["final_answer"] = matches[0][0]
     
    if round["mode"] == "none": 
        round["mode"] = "gpt"
        round["final_answer"] = gpt_get_final_answer(round["text"], round["output"], language)


def get_final_answer_for_all(model_name, bench_version, languages, result_path, answer_path):

    for language in languages:
        print(f"Get final answers for {language}...")

        temp_path = os.path.join(result_path, f"face_human_eval_{bench_version}_{language}_{model_name}_results.json")
        with open(temp_path, 'r') as file:
            data_dict = json.load(file)

        for each in data_dict["results"]:

            eval = each["eval"][0]
            get_final_answer(eval, language)

        temp_output_file_name = os.path.join(answer_path, f"face_human_eval_{bench_version}_{language}_{model_name}_answers")

        with open(temp_output_file_name+".json", 'w',  encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    #TODO: The name of the MLLM to be tested.
    #In this script, we use GPT-4o as an example to demonstrate how to use it. 
    model_name = "GPT-4o"

    #TODO The folder path for the direct test results output by eval.py.
    result_path = "<your path>/result"

    #TODO The folder path for the final results with answers output by this script.
    answer_path = "<your path>/answer"


    bench_version = "v2"
    languages = ['en', 'zh']

    get_final_answer_for_all(model_name, bench_version, languages, result_path, answer_path)