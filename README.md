# Cookmeai - SpartaHacker 8 MSU (Best use of AI)


![cookmeai](https://user-images.githubusercontent.com/93436870/215383512-4ff3afa9-9ceb-4856-b660-793d10fca0b3.png)


## Contributors

- Anh Dao (Johnx) - https://github.com/Johnx69
- Bach Nguyen - https://github.com/bach6104
- Tri Khuc - https://github.com/Ahahaei
- Nguyen Minh - https://github.com/minhngvh

## Video Demo

https://www.youtube.com/watch?v=ybEa5zyINSw

## Features

- `Img2Ing`: allow users to upload an image of a food and the AI model will return the ingredients and recipes to cook that food.
- `Eat2Gether`: allow user to input some locations and our website will return the closest eating place ( Now just support people in campus Michigan State University).
- `Reviews`: allow user to write reviews about food in dining hall.

## Technologies Used

<a href="https://en.wikipedia.org/wiki/HTML" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg" alt="HTML" width="100" height="100"/> </a>
<a href="https://en.wikipedia.org/wiki/CSS" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/w3_css/w3_css-icon.svg" alt="CSS" width="100" height="100"/> </a>
<a href="https://getbootstrap.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg" alt="Bootstrap" width="100" height="100"/> </a>
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="100" height="100"/> </a>
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="100" height="100"/> </a>
<a href="https://pytorch.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="100" height="100"/> </a>
<a href="https://opencv.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg" alt="opencv" width="100" height="100"/> </a>
<a href="https://sqlite.org/index.html" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-ar21.svg" alt="opencv" width="100" height="100"/> </a>

## How to run

> Open Terminal and do the following instructions

#### 1. Clone this github repo

```bash
  git clone https://github.com/Johnx69/SpartanHacker8-Cookmeai.git
```

#### 2. Download the model and dataset files in the following link `https://drive.google.com/drive/folders/1O3qxX_gRzUPL6wZJLcgGILyRWguHmcXu` and save to folder `data` as the following structure

```bash
root
├── data
    ├── ingr_vocab.pkl
    └── instr_vocab.pkl
    └── modelbest.ckpt
```

#### 3. Change directory

```bash
  cd SpartanHacker8-Cookmeai/ 
```

#### 4. Install requirement dependencies

```bash
  pip install -r requirements.txt
```

#### 5. Run application

```bash
  python app.py
```
