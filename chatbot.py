from tensorflow import keras
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from colorama import Fore, Style
import colorama
import json
import shortuuid
import numpy as np
import pickle
import spacy

colorama.init()

with open("intents.json") as file:
    data = json.load(file)

with open("courses.json") as info:
    course_info = json.load(info)

with open("semester.json") as info:
    sem_info = json.load(info)

nlp = spacy.load('en_core_web_sm')

translator = Translator()

def examine_language(text):
    lang = translator.detect(text).lang

    if lang != 'en':
        return translator.translate(text, dest='en').text, lang
    return text, 'en'

def translate_response(text, lang):
    return translator.translate(text, dest=lang).text

def speakResponse(text, lang):
    tts = gTTS(text, lang=lang)
    filename = shortuuid.uuid()
    tts.save(f'responses/{filename}.mp3')
    playsound(f'responses/{filename}.mp3')

def chat():
    model = keras.models.load_model('chat_model')

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)

    max_len = 20

    current_tag = ''
    NAME = 'User'
    PROBLEM = ''
    AREA_OF_INTEREST = ''
    SELECTED_COURSE = ''

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()
        
        if inp.lower() == "quit":
            break

        if current_tag == 'greeting':
            doc = nlp(inp)
            if len(doc.ents) != 0:  
                NAME = doc.ents[0].text
            inp = 'let this trigger work'
        elif current_tag == 'view-course-offered':
            # print('waiting on your to enter something smart')
            if 'medicine' in inp.lower() or '1' in inp:
                AREA_OF_INTEREST = 'medicine'
                inp = 'interested course event'
            elif 'engineering' in inp.lower() or '2' in inp:
                AREA_OF_INTEREST = 'engineering'
                inp = 'interested course event'
            elif 'computing' in inp.lower() or '3' in inp:
                AREA_OF_INTEREST = 'computing'
                inp = 'interested course event'
            elif 'business' in inp.lower() or '4' in inp:
                AREA_OF_INTEREST = 'business'
                inp = 'interested course event'

        elif 'batchelor' in inp.lower():
            for course in course_info['degrees']:
                if course['name'].lower() in inp.lower():
                    SELECTED_COURSE = course['name']
                    inp.replace(course['name'], '$course')

        text, lang = examine_language(inp)

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]), truncating='post', maxlen=max_len))
        tag = label_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:

                # print(text)
                # print(tag)
                current_tag = tag[0]
                
                response = np.random.choice(i['responses'])

                if '$name' in response:
                    response = response.replace('$name', NAME)
                if 'identify' in current_tag:
                    if 'semester' in text:
                        PROBLEM = 'this semester'
                    elif 'course' in text:
                        PROBLEM = 'courses'
                    response = response.replace('$problem', PROBLEM)
                
                if 'payload' in response:
                    if 'view_course_payload' == response:
                        response = "Are you interested in any of the following areas. Please choose one of the following.\n1. Medicine\n2. Engineering \n3. Computing \n4. Business"
                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)
                    elif 'view_all_courses_payload' == response:
                        response = 'Well in that case, here is a list of all the courses offered by Utech.'
                        res = 'Well in that case, here is a list of all the courses offered by Utech.'
                        for course in course_info['degrees']:
                            response += '\n - ' + course['name']
                        trans_text = translate_response(response, lang)
                        trans_txt = translate_response(res, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_txt, lang)
                    elif 'view_some_courses_payload' == response:
                        response = f'Here is a list of courses in {AREA_OF_INTEREST} offered by the University of Technology:'
                        res = f'Here is a list of courses in {AREA_OF_INTEREST} offered by the University of Technology:'
                        for course in course_info['degrees']:
                            if course['type'] == AREA_OF_INTEREST:
                                response += '\n - ' + course['name']
                        trans_text = translate_response(response, lang)
                        trans_txt = translate_response(res, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_txt, lang)
                    elif 'course_cost_payload' in response:
                        for course in course_info['degrees']:
                            if course['name'] in text:
                                response = 'The expected overall tuition for ' + course['name'] + ' is ' + "${:,.2f} JMD".format(float(course['cost']))
                        
                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)
                    elif 'course_info_payload' == response:
                        response = 'I can tell you the following about the major you have selected\n1. Module Selection Guide\n2. Cost of the Course\n3. Careers related to the major'
                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)
                    elif 'module_guide_payload' == response:
                        for course in course_info['degrees']:
                            if course['name'] in text:
                                response = 'The link for the module selection guide for ' + course['name'] + ' is ' + course['module_guide_link']
                                res = 'The link for the module selection guide for ' + course['name']
                        trans_text = translate_response(response, lang)
                        trans_txt = translate_response(res, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_txt, lang)
                    elif 'semester_link_payload' == response:
                        if 'withdrawal' in text:
                            response = 'Here is the link for the withdrawal form: ' + sem_info['semesters'][1]['withdrawal_form_link']
                            res = 'Here is the link for the withdrawal form'
                        elif 'add' in text or 'drop' in text:
                            response = 'Here is the link for the add/drop page: ' + sem_info['semesters'][1]['add_drop_link']
                            res = 'Here is the link for the add/drop page'

                        trans_text = translate_response(response, lang)
                        trans_txt = translate_response(res, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_txt, lang)
                    elif 'course_career_payload' == response:
                        for course in course_info['degrees']:
                            if course['name'] in text:
                                response = 'Here are some of the jobs opportunity for this course: '
                                for index in range(len(course['associated_careers'])):
                                    if index == len(course['associated_careers']) - 1:
                                        response += course['associated_careers'][index]
                                    else:
                                        response += course['associated_careers'][index] + ', '

                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)
                    elif 'date_payload' in response:
                        if 'end' in text:
                            date_type = ['end']
                            response = 'The final date for '
                        elif 'start' in text or 'begin' in text:
                            date_type = ['start']
                            response = 'The start date for '
                        else:
                            date_type = ['start', 'end']
                            response = 'The timeframe for '

                        if 'semester' in text:
                            event_type = 'semester'
                            response += 'the semester is '
                        elif 'module' in text:
                            event_type = 'module_selection'
                            response += 'the module selection is '
                        elif 'add' in text or 'drop' in text or 'withdrawal' in text:
                            event_type = 'add_drop'
                            response += 'the add/drop or withdrawal is '
                            
                        for index in range(len(date_type)):
                            if index == 0:
                                response += sem_info['semesters'][1][event_type + '_' + date_type[index]]
                            else:
                                response += ' - ' + sem_info['semesters'][1][event_type + '_' + date_type[index]]
                        
                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)

                else:
                    if "\n" in response:
                        for res in response.split("\n"):
                            trans_text = translate_response(res, lang)
                            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                            speakResponse(trans_text, lang)
                    else:
                        trans_text = translate_response(response, lang)
                        print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , trans_text)
                        speakResponse(trans_text, lang)

if __name__ == '__main__':
    chat()