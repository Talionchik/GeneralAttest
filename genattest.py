# Проект для парсинга определенных сайтов. Поиск можно вести по выбранным категориям. 
# Подходит для выполнения заказов по парсингу на фриланс-биржах.
# Результаты сбора информации сохраняются в csv-файле. 
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Начало работы
s = requests.session()

# Список фильмов, данные по которым необходимо удалить из анализа.
films = []

# Список данных, найденных в интернете.
names = []
ratings = []
genres = []

# Путь где будут представлены ваши фильмы.
path = input("Enter the path where your films are: ")

filmswe = os.listdir(path)

for film in filmswe:
    # Добавление в список моих фильмов
    films.append(os.path.splitext(film)[0])
   

for line in films:
    # x = line.split(", ")
    title = line.lower()
    # release = x[1]
    query = "+".join(title.split())
    URL = "https://www.imdb.com/search/title/?title=" + query
    print(URL)
    # print(release)
    try:
        response = s.get(URL)

        # Получение данных контента с выбранного сайта
        content = response.content

        # print(response.status_code)

        soup = BeautifulSoup(response.content, features="html.parser")
        # Поиск всех необходимых фильмов
        containers = soup.find_all("div", class_="lister-item-content")
        for result in containers:
            name1 = result.h3.a.text
            name = result.h3.a.text.lower()

            # Uncomment below lines if you want year specific as well, define year variable before this
            # year = result.h3.find(
            # "span", class_="lister-item-year text-muted unbold"
            # ).text.lower()

            #if film found (searching using name)
            if title in name:
                #scraping rating
                rating = result.find("div",class_="inline-block ratings-imdb-rating")["data-value"]
                #scraping genre
                genre = result.p.find("span", class_="genre")
                genre = genre.contents[0]

                #appending name, rating and genre to individual lists
                names.append(name1)
                ratings.append(rating)
                genres.append(genre)



    except Exception:
        print("Попробуйте изменить категорию или год")

# Хранение данных в датафрейме pandas 
df = pd.DataFrame({'Film Name':names,'Rating':ratings,'Genre':genres})

# Создание csv в pandas
df.to_csv('film_ratings.csv', index=False, encoding='utf-8')
