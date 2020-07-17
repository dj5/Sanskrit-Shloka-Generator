from bs4 import BeautifulSoup
import requests

# Scrapping data from websites


def get_data():
    req = requests.get("https://resanskrit.com/sanskrit-shlok-popular-quotes-meaning-hindi-english/")
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    data = soup.find_all("p", {"style": "text-align: center;"})
    transliteration = list()
    hindi = list()
    english = list()
    for d in data:
        if "Transliteration" in d.text:
            transliteration.append(d.text.split(":")[1])
        if "English Translation" in d.text:
            english.append(d.text.split(":")[1])
        if "Hindi Translation" in d.text:
            hindi.append(d.text.split(":")[1])
        print(d.text)
    req2 = requests.get("https://resanskrit.com/top-chanakya-neeti/")
    content2 = req2.content
    soup2 = BeautifulSoup(content2, "html.parser")
    data2 = soup2.find_all("p", {"style": "text-align: center;"})

    for d in data2:
        if "Transliteration" in d.text:
            transliteration.append(d.text.split(":")[1])
        if "English translation" in d.text:
            english.append(d.text.split(":")[1])
        if "Hindi translation" in d.text:
            hindi.append(d.text.split(":")[1])

    req2 = requests.get("https://resanskrit.com/bhagavad-gita-most-useful-quotes-hindi-english/")
    content2 = req2.content
    soup2 = BeautifulSoup(content2, "html.parser")
    data2 = soup2.find_all("p", {"style": "text-align: center;"})
    f = True
    f2 = True
    for d in data2[2:]:
        if f:
            transliteration.append(d.text)
            f = False
            # print(d.text)
        elif f2:
            hindi.append(d.text)
            f2 = False
            # print(d.text)
        else:
            english.append(d.text)
            f = True
            f2 = True
            # print(d.text)

    #     print(d.text)


def get_data_sanskrit():
    req = requests.get("https://resanskrit.com/sanskrit-shlok-popular-quotes-meaning-hindi-english/")
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    data_san = soup.find_all("h3", {"style": "text-align: center;"})
    sanskrit = []
    for d in data_san:
        sanskrit.append(d.text)
    req2 = requests.get("https://resanskrit.com/bhagavad-gita-most-useful-quotes-hindi-english/")
    content2 = req2.content
    soup2 = BeautifulSoup(content2, "html.parser")
    data_san2 = soup2.find_all("strong")
    for i in data_san2[:26]:
        sanskrit.append((i.text))
    req2 = requests.get("https://resanskrit.com/top-chanakya-neeti/")
    content2 = req2.content
    soup2 = BeautifulSoup(content2, "html.parser")
    data_san2 = soup2.find_all("h4", {"style": "text-align: center;"})
    for i in data_san2:
        sanskrit.append(i.text)
    sanskrit = [t[:t.find("॥") + 1] for t in sanskrit]
    temp = []
    for t in sanskrit:
        if t.find("॥") != -1:
            temp.append(t[:t.find("॥") + 1])
        elif t != '':
            temp.append(t)

    sanskrit = temp
    return sanskrit
