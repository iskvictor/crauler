import requests
from bs4 import BeautifulSoup

class Gismeteo_model():
    URL_GIS = 'https://www.gismeteo.ua/city/?gis{}={}&searchQueryData='
    URL_REQ = 'https://www.gismeteo.ua{}14-days/'
    HEADERS = {
        'Host': 'www.gismeteo.ua',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html; charset=UTF-8',
        'Connection': 'keep-alive'
    }


    def get_html(self, date_selection, selection_of_city):
        try:
            req = requests.get(self.URL_GIS.format(date_selection.replace('-', ''), selection_of_city), headers=self.HEADERS)
            return req.text
        except Exception as e:
            print(e)


    def get_city_gis(self,html_gis):
        soup = BeautifulSoup(html_gis, 'lxml')
        links = []
        cities = []
        try:
            all_catalog = soup.findAll('div', {'class': 'districts wrap'})[:-1]
            for section in all_catalog:
                group = section.findAll('div', {'class': 'group'})
                for part_group in group:
                    part_group.find('ul')
                    li = part_group.findAll('li')
                    for d in li:
                        l = d.find('a')
                        link = l.get('href')
                        city = d.text.replace('\n', '').replace('\t\t\t', '').replace('\xa0', '').replace('\t', '')
                        cities.append(city)
                        links.append(link)
            return cities, links
        except (IndexError, Exception):
            raise ValueError('Попробуйте еще раз')


    def list_of_cities_gis(self,cities):
        print('from GISMETEO')
        for number_of_city in enumerate(cities):
            print(number_of_city)


    def send_req(self, http_gis):
        try:
            r = requests.get(self.URL_REQ.format(http_gis), headers=self.HEADERS)
            return r.text
        except Exception as e:
            print(e)


    def parse_date_index(self,req_http,data_selection):
        try:
            soup = BeautifulSoup(req_http, 'lxml')
            content = soup.findAll('div', {'class': 'wbfull'})
            my_list = []
            for i in content:
                m = i.find_all('tbody', {'id': 'tbwdaily1'})
                for k in m:
                    sp = str(k.find('th'))
                    my_list.append(sp)
            for row in my_list:
                if data_selection in row:
                    return my_list.index(row)
        except Exception as e:
            print(e)


    def parse_14_day(self,req_http, index):
        try:
            soup = BeautifulSoup(req_http, 'lxml')
            content = soup.findAll('div', {'class': 'wbfull'})[index]
            weather = content.findAll('tr')
            list_temp =[]
            for el in weather:
                day = el.find('th').text
                params = el.findAll('td')[1:]
                temp_gis = params[1].find('span', {'class': 'value m_temp c'}).text
                dictionary = {day: temp_gis}
                list_temp.append(dictionary)
            return list_temp
        except Exception as e:
            print(e)
