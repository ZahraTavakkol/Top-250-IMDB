# Required Packages
import requests
from bs4 import BeautifulSoup
import random
import time
import re
import numpy as np
import os
import pandas as pd
import sys

# Define required functions

def make_movie_table(content, movie_id):

    movie = {}

    movie['id'] = movie_id
    movie['title'] = content.select('.hero__primary-text')[0].get_text().strip()

    info = content.select('.sc-d8941411-2')[0].find_all('li')
    info = [_.text.strip() for _ in info]

    try:
        movie['year'] = int(info[0])
    except:
        movie['year'] = np.nan
        
    try:
        runtime = info[-1].split()
        if len(runtime) == 2:
            movie['runtime'] = int(runtime[0][:-1])*60+int(runtime[1][:-1])
        elif len(runtime) == 1:
            if runtime[0][-1] == 'm':
                movie['runtime'] = int(runtime[0][:-1])
            elif runtime[0][-1] == 'h':
                movie['runtime'] = int(runtime[0][:-1])*60
        else:
            movie['runtime'] = np.nan
    except:
        movie['runtime'] = np.nan
    
    movie['parental_guide'] = 'Unrated'
    if len(info) >= 3:
        if info[1].strip() not in ['Not Rated', 'null', 'blank', None, np.nan, np.NAN]:
            movie['parental_guide'] = info[1].strip()
    
    try:
        boxes = content.select('.ipc-metadata-list__item.sc-48038814-2.MkXSe')
        for i in range(len(boxes)):
            box = boxes[i].select('span.ipc-metadata-list-item__label')[0].text.strip()
            if box == 'Gross US & Canada':
                gross = boxes[i].select('span.ipc-metadata-list-item__list-content-item')[0].text.strip()
                movie['gross_us_canada'] = int(re.sub(r'[\$,]', '', gross))
                break
            else:
                movie['gross_us_canada'] = np.nan
    except:
        print('problem in gross')
        movie['gross_us_canada'] = np.nan

    return [movie]

def make_language_table(content, movie_id):

    language_list = []

    detail = content.select('li.ipc-metadata-list__item')
    for d in detail:
        try:
            if d.find(class_='ipc-metadata-list-item__label').text.strip() in ['Languages', 'Language']:
                languages = [l.text.strip() for l in d.find_all(class_='ipc-metadata-list-item__list-content-item--link')]
        except:
            continue

    for l in languages:
        language = {}
        language['movie_id'] = movie_id
        language['language'] = l

        language_list.append(language)

    return language_list

def make_country_table(content, movie_id):

    country_list = []

    detail = content.select('li.ipc-metadata-list__item')
    for d in detail:
        try:
            if d.find(class_='ipc-metadata-list-item__label').text.strip() in ['Countries of origin','Country of origin']:
                countries = [c.text.strip() for c in d.find_all(class_='ipc-metadata-list-item__list-content-item--link')]
        except:
            continue

    # try:  
    for c in countries:
        country = {}
        country['movie_id'] = movie_id
        country['country'] = c

        country_list.append(country)

    return country_list

def make_genre_table(content, movie_id):

    genres_list = []

    genres = content.select('.ipc-chip-list__scroller')[0].find_all('span')
    for g in genres:
        genre = {}
        genre['movie_id'] = movie_id
        genre['genre'] = g.text.strip()

        genres_list.append(genre)

    return genres_list

def make_crew_table(person_id, movie_id, role):

    crew = {}

    crew['movie_id'] = movie_id
    crew['person_id'] = person_id
    crew['role'] = role

    return crew

def make_cast_table(person_id, movie_id):

    cast = {}

    cast['movie_id'] = movie_id
    cast['person_id'] = person_id
    
    return cast

def make_person_table(content, movie_id):
    
    person_list = []
    crew_list = []
    cast_list = []

    person_section = content.select('.ipc-metadata-list.ipc-metadata-list--dividers-all.title-pc-list.ipc-metadata-list--baseAlt')[0].select('.ipc-metadata-list__item')
    for p in person_section:
        
        try:
            role = p.find('span').text.strip()
        except:
            role = p.find('a').text.strip()

        person_info = p.find_all(class_='ipc-metadata-list-item__list-content-item')

        for i in range(len(person_info)):
            person = {}
            
            person['id'] = person_info[i].get('href').strip().split('/')[2][2:]
            person['name'] = person_info[i].text.strip()

            if role in ['Director', 'Writers', 'Directors', 'Writer']:
                crew = make_crew_table(person['id'], movie_id, role)
                crew_list.append(crew)
            elif role in ['Stars', 'Star']:
                cast = make_cast_table(person['id'], movie_id)
                cast_list.append(cast)
        
            person_list.append(person)

    return person_list, crew_list, cast_list

# save logs to a text file
def save_logs(log, log_file):
    with open(log_file, 'a') as file:
        file.write(log + '\n')

# save data to CSV
def save_to_csv(data, file_path):
    pd.DataFrame(data).to_csv(file_path, mode='a', header=False, index=False)

# scrape data
def scrape_movie_data(html_files, headers, movie_links, counter, log_file, directory):
    try:
        url = movie_links[counter - 1]
        time.sleep(random.randint(5, 10))
        movie_response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(movie_response.content, 'html.parser')
        movie_id = url.split('/')[4][2:]

        movie_temp = make_movie_table(soup, movie_id)
        genre_temp = make_genre_table(soup, movie_id)
        language_temp = make_language_table(soup, movie_id)
        country_temp = make_country_table(soup, movie_id)
        person_temp, crew_temp, cast_temp = make_person_table(soup, movie_id)

        # Saving data to CSV
        save_to_csv(genre_temp, os.path.join(directory, 'genre_table.csv'))
        save_to_csv(language_temp, os.path.join(directory, 'language_table.csv'))
        save_to_csv(country_temp, os.path.join(directory, 'country_table.csv'))
        save_to_csv(person_temp, os.path.join(directory, 'person_table.csv'))
        save_to_csv(crew_temp, os.path.join(directory, 'crew_table.csv'))
        save_to_csv(cast_temp, os.path.join(directory, 'cast_table.csv'))
        save_to_csv(movie_temp, os.path.join(directory, 'movie_table.csv'))

        message = f"Movie_{counter} data recorded."
        print(message)
        save_logs(message, log_file)

        counter = counter + 1
    
    except Exception as e:
        error_message = f"Error extracting data for Movie_{counter}: {e}"
        save_logs(error_message, log_file)
        print(error_message)
    

    return counter

def get_movie_links(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        movies = soup.select('.ipc-metadata-list-summary-item__c')
        movie_links = ['https://www.imdb.com' + movie.find('a').get('href') for movie in movies]
        return movie_links
    
    except Exception as e:
        print(f"Error getting movie links: {e}")
        return []