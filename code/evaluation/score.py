import os
import json

def is_true(eval):

    if eval[0]["answer"][0] == eval[0]["final_answer"][0]:
        return True
    else:
        return False

def score(model_name, bench_version, languages, answer_path, selected_subset):

    all_result_dict = dict()

    for language in languages:

        temp_path = os.path.join(answer_path, f"face_human_eval_{bench_version}_{language}_{model_name}_answers.json")
        with open(temp_path, 'r') as file:
            data_dict = json.load(file)

        result_dict = dict()

        for each in selected_subset:
            result_dict[each[0]+"-"+each[1]] = [0, 0, 0] # Correct Count, Refusal Count, Total Count

        for each in data_dict["results"]:

            eval = each["eval"]
            result_dict[each["task_type"]+"-"+each["data_version"]][2] += 1

            if is_true(eval):
                result_dict[each["task_type"]+"-"+each["data_version"]][0] += 1

            if eval[0]["final_answer"] == "X":
                result_dict[each["task_type"]+"-"+each["data_version"]][1] += 1

        total_list = [0, 0, 0]
        for each in result_dict.keys():
            total_list[0]+=result_dict[each][0]
            total_list[1]+=result_dict[each][1]
            total_list[2]+=result_dict[each][2]

        all_result_dict[language] = result_dict

    return all_result_dict


if __name__ == "__main__":

    #TODO: The name of the MLLM to be tested.
    #In this script, we use GPT-4o as an example to demonstrate how to use it. 
    model_names = [
        "GPT-4o",
    ]

    #TODO The folder path for the final results with answers output by output_final_answer.py.
    answer_path = "<your path>/answer"

    bench_version = "v2"
    languages = ["en", 'zh']
    selected_subset = [
        ("face_attribute_compound", "original"),
        ("face_attribute_compound", "cropped"),
        ("face_age_basic_5", "original"),
        ("face_age_basic_5", "cropped"),
        ("face_age_basic_10", "original"),
        ("face_age_basic_10", "cropped"),
        ("face_age_basic_15", "original"),
        ("face_age_basic_15", "cropped"),
        ("face_expression_basic", "original"),
        ("face_expression_basic", "cropped"),
        ("face_expression_compound", "cropped"),
        ("face_attack_physical_paper", "cropped"),
        ("face_attack_physical_replay", "cropped"),
        ("face_attack_digital_identity_swap", "cropped"),
        ("face_attack_digital_expression_swap", "cropped"),
        ("face_recognition_basic", "cropped"),
        ("face_recognition_cross_age", "cropped"),
        ("face_recognition_cross_pose", "cropped"),
        ("face_recognition_mask", "cropped"),
        ("face_recognition_similar_looking", "cropped"),
        ("human_reid_basic", "cropped"),    
        ("human_attribute_compound_cropped", "cropped"),
        ("human_attribute_compound", "boxed"),
        ("human_action_basic", "boxed"),
        ("human_spatial_relation_count_10", "original"),
        ("human_spatial_relation_count_100", "original"),
        ("human_spatial_relation_count_100plus", "original"),
        ("human_spatial_relation_location", "boxed"),
        ("human_social_relation_occupation", "boxed"),
        ("human_social_relation_relationship", "boxed")]

    subset_split = {
        "face": {
            "attribute": {
                "compound": [
                    ("face_attribute_compound", "original"),
                    ("face_attribute_compound", "cropped")
                ] 
            },
            "age": {
                "15-year-interval": [
                    ("face_age_basic_15", "original"),
                    ("face_age_basic_15", "cropped")
                ],
                "10-year-interval": [
                    ("face_age_basic_10", "original"),
                    ("face_age_basic_10", "cropped")
                ],
                "5-year-interval": [
                    ("face_age_basic_5", "original"),
                    ("face_age_basic_5", "cropped")
                ]
            },
            "expression": {
                "basic": [
                    ("face_expression_basic", "original"),
                    ("face_expression_basic", "cropped")
                ],
                "compound": [
                    ("face_expression_compound", "cropped")
                ]
            },
            "attack": {
                "digital_attack": [
                    ("face_attack_digital_expression_swap", "cropped"),
                    ("face_attack_digital_identity_swap", "cropped"),
                ],
                "physical_attack": [
                    ("face_attack_physical_paper", "cropped"),
                    ("face_attack_physical_replay", "cropped")
                ]
            },
            "recognition": {
                "basic": [
                    ("face_recognition_basic", "cropped")
                ],
                "cross_age": [
                    ("face_recognition_cross_age", "cropped")
                ],
                "cross_pose": [
                    ("face_recognition_cross_pose", "cropped")
                ],
                "mask": [
                    ("face_recognition_mask", "cropped")
                ],
                "similar_looking": [
                    ("face_recognition_similar_looking", "cropped")
                ],
            }
        },
        "human": {
            "attribute": {
                "compound": [
                    ("human_attribute_compound", "boxed"),
                    ("human_attribute_compound_cropped", "cropped")
                ]
            },
            "action": {
                "basic": [
                    ("human_action_basic", "boxed")
                ]
            },
            "spatial_relation": {
                "count": [
                    ("human_spatial_relation_count_10", "original"),
                    ("human_spatial_relation_count_100", "original"),
                    ("human_spatial_relation_count_100plus", "original")
                ],
                "relative_location": [
                    ("human_spatial_relation_location", "boxed")
                ]
            },
            "social_relation": {
                "occupation": [
                    ("human_social_relation_occupation", "boxed")
                ],
                "social_relationship": [
                    ("human_social_relation_relationship", "boxed")
                ]
            },
            "reid": {
                "basic": [
                    ("human_reid_basic", "cropped")
                ]
            }
        }
    }

# Prints scores.
    for model_name in model_names:

        print("*"*100)
        print(model_name)

        all_result_dict = score(model_name, bench_version, languages, answer_path, selected_subset)


        for language in languages:
            print(language)
            final_score = [0, 0]
            final_count = 0

            for first_level in subset_split.keys():
                print("\t|"+first_level)
                first_level_score = [0, 0]
                first_level_count = 0
                for second_level in subset_split[first_level].keys():
                    print("\t|\t|"+second_level)
                    second_level_score = [0, 0]
                    second_level_count = 0
                    for third_level in subset_split[first_level][second_level].keys():
                        print("\t|\t|\t|"+third_level)
                        third_level_score = [0, 0]
                        third_level_count = 0
                        for fourth_level in subset_split[first_level][second_level][third_level]:
                            temp = fourth_level[0]+"-"+fourth_level[1]
                            print("\t|\t|\t|\t|"+temp)
                            temp_score = all_result_dict[language][temp]

                            acc = temp_score[0]/temp_score[2]
                            clean_acc = temp_score[0]/(temp_score[2]-temp_score[1])
                            print("\t|\t|\t|\t|", acc, clean_acc) # Outputs overall accuracy and accuracy excluding refusal samples.

                            third_level_count+=1
                            third_level_score[0]+=acc
                            third_level_score[1]+=clean_acc
                        
                        third_level_score[0]/=third_level_count
                        third_level_score[1]/=third_level_count
                        print("\t|\t|\t|", third_level_score[0], third_level_score[1]) # Outputs overall accuracy and accuracy excluding refusal samples.

                        second_level_count+=1
                        second_level_score[0] += third_level_score[0]
                        second_level_score[1] += third_level_score[1]
                        
                    second_level_score[0]/=second_level_count
                    second_level_score[1]/=second_level_count
                    print("\t|\t|", second_level_score[0], second_level_score[1]) # Outputs overall accuracy and accuracy excluding refusal samples.

                    first_level_count+=1
                    first_level_score[0] += second_level_score[0]
                    first_level_score[1] += second_level_score[1]


                first_level_score[0]/=first_level_count
                first_level_score[1]/=first_level_count
                print("\t|", first_level_score[0], first_level_score[1]) # Outputs overall accuracy and accuracy excluding refusal samples.

                final_count+=1
                final_score[0] += first_level_score[0]
                final_score[1] += first_level_score[1]

            final_score[0]/=final_count
            final_score[1]/=final_count
            print("", final_score[0], final_score[1]) # Outputs overall accuracy and accuracy excluding refusal samples.
