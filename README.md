# Face-Human-Bench: A Comprehensive Face and Human Understanding Benchmark for Large Visual Language Models

<p align="center">
    <img src="https://github.com/lxq1000/Face-Human-Bench/blob/main/pictures/logo.png" width="30%"> <br>
</p>


## Introduction

Faces and humans are crucial elements in social interaction and are widely included in everyday photos and videos. Therefore, a deep understanding of faces and humans will enable multi-modal assistants to achieve improved response quality and broadened application scope. Currently, the multi-modal assistant community lacks a comprehensive and scientific evaluation of face and human understanding abilities. In this paper, we first propose a hierarchical ability taxonomy that includes three levels of abilities. Then, based on this taxonomy, we collect images and annotations from publicly available datasets in the face and human community and build a semi-automatic data pipeline to produce problems for the new benchmark. Finally, the obtained Face-Human-Bench includes a development set and a test set, each with 1800 problems, supporting both English and Chinese. We conduct evaluations over 25 mainstream multi-modal large language models (MLLMs) with our Face-Human-Bench, focusing on the correlation between abilities, the impact of the relative position of targets on performance, and the impact of Chain of Thought (CoT) prompting on performance. We also explore which abilities of MLLMs need to be supplemented by specialist models. The data and evaluation code of the Face-Human-Bench will be made publicly available.

 <img src="https://github.com/lxq1000/Face-Human-Bench/blob/main/pictures/face_human_bench.png" alt="Image" width="800">



## Data Acquisition
We comply with all agreements of the original public datasets used and do not involve further copying, publishing, or distributing any portion of the images from these datasets. We will only open-source the [JSON files](https://github.com/lxq1000/Face-Human-Bench/blob/main/data) containing our test and development sets.

To help you reproduce the Face-Human-Bench Benchmark, we provide the following guidelines:

1. Download all original images from the relevant public datasets and organize them according to the file tree below.

```
<your_path>/raw_data
├── face
│   ├── CALFW
│   │   ├── calfw
│   │   └── calfw.zip
│   ├── CelebA
│   │   ├── img_align_celeba
│   │   ├── img_celeba
│   │   └── list_attr_celeba.txt
│   ├── CPLFW
│   │   ├── cplfw
│   │   └── cplfw.zip
│   ├── FF+
│   │   └── cropped
│   ├── LFW
│   │   ├── data
│   │   └── pairs.txt
│   ├── MLFW
│   │   ├── aligned
│   │   ├── mask_list.txt
│   │   ├── MLFW.zip
│   │   ├── origin
│   │   └── pairs.txt
│   ├── RAF-DB
│   │   ├── basic
│   │   └── compound
│   ├── SiW-Mv2
│   │   └── cropped
│   ├── SLLFW
│   │   └── pair_SLLFW.txt
│   └── UTKFace
│       ├── cropped
│       ├── part1
│       ├── part2
│       └── part3
└── human
    ├── HICO-DET
    │   ├── anno
    │   ├── HICO-DET
    │   ├── HICO-DET.tar.gz
    │   ├── metafile.yaml
    │   └── README.md
    ├── Market1501
    │   ├── distractors_500k.zip
    │   ├── Market-1501-v15.09.15
    │   └── Market-1501-v15.09.15.zip
    ├── PISC
    │   ├── annotation_image_info.json
    │   ├── domain.json
    │   ├── domain_split
    │   ├── domain_split.zip
    │   ├── image
    │   ├── images-00
    │   ├── images-01
    │   ├── images-02
    │   ├── images-03
    │   ├── occupation.json
    │   ├── relationship.json
    │   ├── relationship_split
    │   ├── relationship_split.zip
    │   └── test
    ├── ShTech
    │   ├── final_partA
    │   ├── final_partA.zip
    │   ├── ShanghaiTech_Crowd_Counting_Dataset
    │   └── ShanghaiTech_Crowd_Counting_Dataset.zip
    ├── SpatialSense
    │   ├── annotations.json
    │   ├── images
    │   ├── images.tar.gz
    │   └── SHA-256.txt
    └── WIDERAttribute
        ├── Image
        ├── Readme.txt
        ├── wider_attribute_annotation.zip
        ├── wider_attribute_image.tgz
        ├── wider_attribute_test.json
        └── wider_attribute_trainval.json
```
   
2. Use the [`prepare_data.py`](https://github.com/lxq1000/Face-Human-Bench/blob/main/code/prepare_data.py) script to extract test samples from the original images based on the JSON files we provide. Note: You will need to modify the paths in the script to match your local environment. 


