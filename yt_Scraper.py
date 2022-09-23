import re
import pandas as pd
import numpy as np
from requests_html import HTMLSession

# link FOOD
pertinenza_food = "https://www.youtube.com/results?search_query=food&sp=CAASAhAB"
visualizzazioni_food = "https://www.youtube.com/results?search_query=food&sp=CAMSAhAB"
voto_food = "https://www.youtube.com/results?search_query=food&sp=CAESAhAB"

# link TECHNOLOGY
pertinenza_technology = "https://www.youtube.com/results?search_query=technology&sp=CAASAhAB"
visualizzazioni_technology = "https://www.youtube.com/results?search_query=technology&sp=CAMSAhAB"
voto_technology = "https://www.youtube.com/results?search_query=technology&sp=CAESAhAB"

# link ART
pertinenza_art = "https://www.youtube.com/results?search_query=art&sp=CAASAhAB"
visualizzazioni_art = "https://www.youtube.com/results?search_query=art&sp=CAMSAhAB"
voto_art = "https://www.youtube.com/results?search_query=art&sp=CAESAhAB"


def stringCleaner(string):
    string = string.replace("simpleText\":", "")
    string = string.replace("\"", "")
    string = string.replace("}", "")
    string = string.replace("{", "")
    string = string.replace("text:", "")
    string = string.replace(",", "")
    string = string.replace("•", "")
    string = string.replace(":", "")
    string = string.replace(";", " ")
    string = string.rstrip()
    string = string.lstrip()
    return string


df = pd.DataFrame(columns=['Link', 'Titolo', 'Data',
                  'Visualizzazioni', 'hashtag', 'Filter', 'keyword'])
Link = 0
Filter = 'Visualizzazioni'
keyword = 'Art'

session = HTMLSession()
LinkYTSearch = visualizzazioni_art
response = session.get(LinkYTSearch)
response.html.render(sleep=1, keep_page=True, scrolldown=500)


for links in response.html.find('a#video-title'):
    Link = next(iter(links.absolute_links))
    # rimozione video short
    Link = str(Link)
    short = Link.find('short')
    if short != -1:
        continue
    new_row = {'Link': Link, 'Titolo': '', 'Data': '', 'Visualizzazioni': '',
               'hashtag': '', 'Filter': Filter, 'keyword': keyword}
    df.loc[len(df.index)] = [Link, '', '', '', '', Filter, keyword]

print('OK LINK')
session = HTMLSession()

for index, row in df.iterrows():
    LinkYT = df.at[index, 'Link']
    response = session.get(LinkYT)
    hashtags = re.findall(r"/hashtag/(.*?)\"", response.text)  # this is a list
    hashtags = list(dict.fromkeys(hashtags))  # Remove duplicate

    # filtro hashtag
    if not hashtags:
        hashtags = np.nan

    title = re.findall(r"title\":{\"(.*?)}", response.text)[0]
    visualizzazioni = re.findall(
        r",{\"text\":(.*?)visualizzazioni", response.text)[-1]
    date = re.findall(r"\"dateText\"(.*?)}", response.text)[0]
    title = stringCleaner(title)
    visualizzazioni = stringCleaner(visualizzazioni)
    date = stringCleaner(date)

    # filtro video 2020, 2021
    date = str(date)
    listDate = ["2020", "2021"]
    dateCheck = any(listDates in date for listDates in listDate)
    if dateCheck == False:
        date = np.nan

    df.at[index, 'hashtag'] = hashtags
    df.at[index, 'Titolo'] = title
    df.at[index, 'Visualizzazioni'] = visualizzazioni
    df.at[index, 'Data'] = date


df.dropna(inplace=True)
df.to_csv("Art_Visualizzazioni.csv", sep=';')
print(df)
