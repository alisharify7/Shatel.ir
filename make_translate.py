"""
this script automatically translate all _() texts to expected language
TODO: refactor code :!!!!!
"""


import datetime
import os
import pathlib
import sys
import json
import time

from translate import Translator

# pybabel extract -F babel.fg -k _l -o message.po .
# extracting persian raw texts from codes
# pybabel init -i message.po -d ./translations -l en
# pybabel compile -d ./translations


languages = [
    "fa",
    "en",
    "ar",
    "ru",
    "tr",
    "zh",
]
max_request_error = "MYMEMORY WARNING"

global dictionary
dictionary = {}
startTime = time.time()


def log(text:str) -> None:
    """Logger function
    
    Keyword arguments:
    text --  std.out
    Return: None
    """
    
    print(f"[{datetime.datetime.utcnow()}] {text}")


def load_data():
    """
    This function load saved data from json file to a dictionary file
    """
    global dictionary
    try:
        with open("translations/data.json", "r", encoding="utf-8") as f:
            dictionary = json.load(f)
            log("Load data from backup file")
    except FileNotFoundError:
        pass


def save_date():
    """
    This function save each language translation in json file
    """
    global dictionary
    with open("translations/data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(dictionary))
        log("saving data to backup file")


load_data()

for each in languages:
    if each not in dictionary:
        dictionary[each] = {}

log("extract Keywords for files")
print(os.system("pybabel extract -F babel.cfg -k _l -o ./translations/message.po ."))

log("Create catalog for each Language")
for each in languages:
    print(os.system(f"pybabel init -i ./translations/message.po -d ./translations -l {each}"))






global counter
counter = 0


def translate(text, from_lang, to_lang):
    def check():
        global counter
        counter += 1
        if counter == 20:
            save_date()
            counter = 0
            print(f"[20] round dumping, counter is {counter}")

    check()

    if to_lang == from_lang:
        return text
    if text in dictionary[to_lang]:
        return dictionary[to_lang][text]
        for each in ['MAX', 'ERROR']:
            if each in dictionary[to_lang][text].upper():
                with open("txt.txt", "w", encoding="utf-8") as f:
                    f.write(text.strip())
                print(dictionary[to_lang][text])
                t = bool(input(f"Tr from {from_lang} to {to_lang} OK "))
                with open("txt.txt", "r", encoding="utf-8") as f:
                    t = f.readlines()
                print(t)
                exit()
                dictionary[to_lang][text] = t


        return dictionary[to_lang][text]

        if max_request_error in dictionary[to_lang][text]:
            save_date()
            print("MAX ERROR")
            sys.exit("Max")

        if dictionary[to_lang][text] == text or not dictionary[to_lang][text]:
            del dictionary[to_lang][text]
            txt = translate(text, from_lang, to_lang)
            dictionary[to_lang][text] = txt
            return txt

        dictionary[to_lang][text] = text
        return dictionary[to_lang][text]

    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translatedText = translator.translate(text=text)

    if not translatedText:
        save_date()
        return text

    if max_request_error in translatedText:
        save_date()
        print("MAX ERROR")
        sys.exit("MAX")

    translatedText = translatedText
    if to_lang == "en":
        translatedText = translatedText.capitalize()
    dictionary[to_lang][text] = translatedText
    print("OK:", translatedText)
    return translatedText


dirs = os.listdir("./translations")
for each in dirs:
    lang = each
    if lang not in languages:
        continue
    each = pathlib.Path(f"./translations/{each}")

    if not each.is_dir():
        continue

    each = each.absolute() / os.listdir(each.absolute())[0] / "messages.po"
    log(f"Opening [{lang}] File")
    p = ""
    new_file = ""
    with open(each, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:

            if "msgid" in line:
                p = line.split("msgid")[-1]
            elif "msgstr" in line:
                p = p.replace("\n", " ")
                p = p.replace(r"\n", " ")
                p = p.replace("\\n", " ")
                p = p.strip()

                t = f'msgid "{p}"'
                text = translate(text=p, from_lang="fa", to_lang=lang)


                print(f"[FROM fa]: {p}")
                print(f"[TO {lang}]: {text}")

                t += f"\nmsgstr \"{text}\"\n"
                new_file += t
                p = ""
            elif line.startswith("#"):
                new_file +="\n" +line.strip().replace("\n", "")+"\n"
            else:
                p += line
                p = p.replace('"', '')
                p = p.replace("\n", "")
                p = p.strip()

                continue

        with open(each.parent / each, "w", encoding="utf-8") as f:
            f.write(new_file)
            log(f"Dumping {lang} catalog")

        save_date()
        log(f"Dumping {lang} to file is done")

save_date()
# print(os.system("pybabel compile -d ./translations"))
log(f"Total Time: {time.time() - startTime} second")
