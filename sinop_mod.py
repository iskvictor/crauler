import requests
from bs4 import BeautifulSoup




class Sinoptic_model():

    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, lzma, sdch, br",
        "accept-language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
        "cookie": "cities=100524901; _ym_uid=1506980810791328011; _ym_isad=2; __utmt=1; os=LINUX; location=165.100504341; "
                  "_ym_visorc_118959=w; kP834iE76=30e567d4a259e98471ad4c6f7cf81b9b6869f7fa5b7c; co=1; _"
                  "_utma=176018208.205523433.1506980811.1506980811.1506980811.1; __utmb=176018208.2.10.1506980811; "
                  "__utmc=176018208; __"
                  "utmz=176018208.1506980811.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
        "referer": "https://sinoptik.com.ru/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/53.0.2785.101 Safari/537.36 OPR/40.0.2308.62",
        "x-requested-with": "XMLHttpRequest"
    }

    URL_SEARCH = 'https://sinoptik.ua/search.php?q={}'
    URL_CITY = 'https://sinoptik.ua/{}/{}?ajax=GetForecast'

    def get_city_names(self, first_letters_city, headers=HEADERS):
        try:
            content = requests.get(self.URL_SEARCH.format(first_letters_city), headers=headers)
            content.encoding = 'utf-8'
            city_names = content.text
            return city_names
        except Exception as e:
            print(e)
            exit()


    def split_city_names(self, city_names):
        cities = [p.split('|') for p in city_names.split('\n')]
        return cities


    def print_cities(self,cities):
        print('from SINOPTIK.UA')
        for list_of_city in enumerate(cities):
            print(list_of_city)


    def get_forecast_for_2_days(self, my_city, date_selection, headers=HEADERS):
        try:
            content = requests.get(self.URL_CITY.format(my_city, date_selection), headers=headers)
            content.encoding = 'utf-8'
            temp_city = content.text
            return temp_city
        except Exception as e:
            print(e)
            exit()


    def selection_city(self,selection_of_city, cities):
        try:
            sin_city = str(cities[selection_of_city][-1])
            region_sinop = (cities[selection_of_city][0:-1])
            meteo_city = region_sinop[0]
            return meteo_city, sin_city, region_sinop
        except Exception as e:
            print(e)


    def parsing_forecast_for_2_days(self, temp_city):
        try:
            soup = BeautifulSoup(temp_city, 'lxml')
            pages_start = soup.find('div', {'class': 'wMain clearfix'}).find('div', {'class': 'rSide'})
            pages = (pages_start.find('tr', {'class': 'temperature'}))
            size = (str(pages)).find('class')
            time_detaile = ['0_00', '3_00', '6_00', '9_00', '12_00', '15_00', '18_00', '21_00']
            time_short = ['2_00', '8_00', '14_00', '20_00']
            time = None
            if size == 4:
                time = time_short
            elif size == 8:
                time = time_detaile
            temperature = []
            for loop_index in range(1, len(time) + 1):
                temp_ra = str(pages.find('td', {'class': 'p{0}'.format(loop_index)})).split('>')[1].split('<')[0]
                all_temp = ('temperature at_{}:{}'.format((time[loop_index - 1]), (temp_ra)))
                temperature.append(all_temp)
            return temperature
        except Exception as e:
            print(e)


