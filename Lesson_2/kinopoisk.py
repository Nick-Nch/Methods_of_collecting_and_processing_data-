from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'https://www.kinopoisk.ru'

params = {'quick_filters':'serials',
          'tab':'all'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

response = requests.get(url+'/popular/films', params=params, headers=headers)

soup = bs(response.text, 'html.parser')

serials_list = soup.find_all('div',attrs={'class':'desktop-rating-selection-film-item'})
print()

serials = []

for serial in serials_list:
    serial_data = {}
    serial_link = url + serial.find('a',attrs={'class':'selection-film-item-meta__link'}).get('href')
    serial_name = serial.find('p',attrs={'class':'selection-film-item-meta__name'}).getText()
    serial_genre = serial.find_all('span',attrs={'class':'selection-film-item-meta__meta-additional-item'})[1].getText()
    serial_rating = serial.find('span',attrs={'class':'rating__value'})
    if serial_rating:
        serial_rating = float(serial_rating.getText())

    serial_data['link'] = serial_link
    serial_data['name'] = serial_name
    serial_data['genre'] = serial_genre
    serial_data['rating'] = serial_rating

    serials.append(serial_data)

pprint(serials)
