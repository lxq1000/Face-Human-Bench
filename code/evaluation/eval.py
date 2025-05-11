
import os
import json
import base64
import requests
import sys
from PIL import Image 
import io 
import time

import random
random.seed(100)


def resize_and_encode_image(image_path, max_size=(1000, 1000)):  
    with Image.open(image_path) as img:  
        width, height = img.size  
           
        if width > max_size[0] or height > max_size[1]:  
            img.thumbnail(max_size, Image.ANTIALIAS) 
            width, height = img.size   
           
        byte_arr = io.BytesIO()  
        img.save(byte_arr, format='PNG')
        byte_arr = byte_arr.getvalue()  
           
        base64_str = base64.b64encode(byte_arr).decode('utf-8')  
          
        return base64_str  


def gpt_api(text, image_path):
    base64_image = resize_and_encode_image(image_path)

    # TODO: your API key
    api_key = "your API key"

    headers = {
        "Authorization": 'Bearer ' + api_key,
    }

    payload = {
        "model": "gpt-4o-2024-05-13",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }

    # TODO: your API site
    site = "your API site"

    response = requests.post(site, 
                            headers=headers, 
                            json=payload,
                            stream=False)
    return response


# TODO: In this test code, we use GPT-4o as an example to demonstrate how to use it. 
# If you need to test other MLLMs, please replace this function with the corresponding API of the desired MLLM.
def gpt(text, image_path, max_retries=3):

    retries = 0

    while retries < max_retries:
        try:
            chat_completion = gpt_api(text, image_path)
            response = chat_completion.json()["choices"][0]["message"]["content"]
            retries+=1
            return response
        
        except Exception as e:
            print(f"Someting wrong:{e}. Retrying in 1 minute...")
            time.sleep(60)
            retries += 1

    print("Max retries reached. Unable to get a response.")
    return "ERROR"


def test_single_sample(sample_info, eval_data_root_path, subset_info, language):

    k = len(sample_info["QA"]["options"])

    sample = dict()
    sample["task_type"] = subset_info[0]
    sample["data_version"] = subset_info[1]
    sample["sample_info"] = sample_info
    sample["eval"] = []

    round_k = random.randint(0, k-1) # shuffle

    if language == "en":

        text = "Question: " + sample_info["QA"]["question"] + "\n"
        op = ["A.", "B.", "C.", "D."]
        for i in range(k):
            text += op[i]
            text += " "
            text += str(sample_info["QA"]["options"][(i+round_k)%k])
            text += "\n"
        text += "Please select the correct answer from the options above."
    else:

        text = "问题: " + sample_info["QA"]["question"] + "\n"
        op = ["A.", "B.", "C.", "D."]
        for i in range(k):
            text += op[i]
            text += " "
            text += str(sample_info["QA"]["options"][(i+round_k)%k])
            text += "\n"
        text += "请从以上选项中选择正确的答案。"

    answer_op = ["A", "B", "C", "D"]
    answer = answer_op[(sample_info["QA"]["answer"]-round_k)%k]
    image_path = os.path.join(eval_data_root_path, sample_info["image"]["image_paths"][subset_info[1]])


    result = gpt(text, image_path)

    temp = dict()
    temp["round"] = round_k
    temp["text"] = text
    temp["answer"] = answer
    temp["output"] = result

    sample["eval"].append(temp)

    return sample


def test_single_subset(data_dict, eval_data_root_path, output_path, subset_info, file_handle, language):

    data = data_dict["data"]
    temp_results = []

    for i in range(len(data)):
        print(f"[{i+1}/{len(data)}]")
        each = data[i]
        sample_output = test_single_sample(each, eval_data_root_path, subset_info, language)
        temp_results.append(sample_output)
        file_handle.write(str(sample_output)+"\n")

    return temp_results


def test(model_name, bench_version, languages, json_files_path, eval_data_root_path, output_path, selected_subset):


    for language in languages:
        print(f"Test for {language}...")

        results = dict()
        results["results"] = list()
        results["model_name"] = model_name
        results["bench_version"] = bench_version
        results["language"] = language

        temp_output_file_name = os.path.join(output_path, f"face_human_eval_{bench_version}_{language}_{model_name}_results")

        file_handle = open(temp_output_file_name+"_log.txt", mode='a')

        for each in selected_subset:
            print(f"Test for {each[0]}, {each[1]} version...")
            temp_path = os.path.join(json_files_path, language, each[0]+'.json' if language=="en" else each[0]+'_zh.json')
            with open(temp_path, 'r') as file:
                data_dict = json.load(file)
                temp_results = test_single_subset(data_dict, eval_data_root_path, output_path, each, file_handle, language)
                results["results"].extend(temp_results)

        with open(temp_output_file_name+".json", 'w',  encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)

        file_handle.close()
    

if __name__ == "__main__":

    #TODO: The name of the MLLM to be tested.
    #In this script, we use GPT-4o as an example to demonstrate how to use it. 
    model_name = "GPT-4o"

    #TODO The folder path for JSON files.
    json_files_path = "<your path>/json"

    #TODO The folder path for images.
    eval_data_root_path = "<your path>/data"

    #TODO The folder path for output.
    output_path = "<your path>/result"


    bench_version = "v2"
    languages = ["en", 'zh']
    selected_subset = [
        ("face_age_basic_5", "original"),
        ("face_age_basic_5", "cropped"),
        ("face_age_basic_10", "original"),
        ("face_age_basic_10", "cropped"),
        ("face_age_basic_15", "original"),
        ("face_age_basic_15", "cropped"),
        ("face_attack_digital_expression_swap", "cropped"),
        ("face_attack_digital_identity_swap", "cropped"),
        ("face_attack_physical_paper", "cropped"),
        ("face_attack_physical_replay", "cropped"),
        ("face_attribute_compound", "original"),
        ("face_attribute_compound", "cropped"),
        ("face_expression_basic", "original"),
        ("face_expression_basic", "cropped"),
        ("face_expression_compound", "cropped"),
        ("face_recognition_basic", "cropped"),
        ("face_recognition_cross_age", "cropped"),
        ("face_recognition_cross_pose", "cropped"),
        ("face_recognition_mask", "cropped"),
        ("face_recognition_similar_looking", "cropped"),
        ("human_action_basic", "boxed"),
        ("human_attribute_compound", "boxed"),
        ("human_attribute_compound_cropped", "cropped"),
        ("human_reid_basic", "cropped"),
        ("human_social_relation_occupation", "boxed"),
        ("human_social_relation_relationship", "boxed"),
        ("human_spatial_relation_count_10", "original"),
        ("human_spatial_relation_count_100", "original"),
        ("human_spatial_relation_count_100plus", "original"),
        ("human_spatial_relation_location", "boxed")]


    test(model_name, bench_version, languages, json_files_path, eval_data_root_path, output_path, selected_subset)