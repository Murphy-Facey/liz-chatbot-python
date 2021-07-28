# Liz Chatbot

A simple chatbot application using the Python. It was developed to handle customer service for the University of Technology, Jamaica. It is made of two sections, a conversation which is the semester problems and course problems and FAQs. 

## How to Install

First you need to have Python installed on your machine. I have Python version 3.9 but I am sure any version that is 3.6+ should work fine.

Afterwards you need to download all the required packages, using the following command in your terminal.
'''
pip install requirements.txt
python -m spacy download en_core_web_sm
'''

Alternatively, you can install all the packages manually using the following command in your terminal.
'''
pip install tensorflow, numpy, googletrans==3.1.0a0, playsound, scikit-learn, gTTS, colorama, shortuuid, spacy
python -m spacy download en_core_web_sm
'''

Then you should be ready to roll

## How to run

** :warning: Please note: You need to create a folder called `responses` inside the root directory of the project.**
The project is split into two parts:

|File name|Command to run| Usage |
|---------|--------------|-------|
|`main.py`| python main.py | This is where the models used for the chatbot is trained, and then saved|
|`chatbot.py`| python chatbot.py| This is where the model is used to power the chatbot as well as additional chatbot-related functionality|

# Things to do

There are couple things I am thinking about doing for further development:

- [ ] Create fallback intents
- [ ] Create the API for the chatbot
    - [ ] Create all GET requests
    - [ ] Create all POST requests
- [ ] Create an UI for the chatbot
- [ ] Create speech to text for the chatbot
