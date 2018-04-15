import requests
import json
from bs4 import BeautifulSoup
import datetime

class Meteo_model():
    METEO_URL_SEARCH = 'http://meteo.ua/autocomplete-ajax?name_startsWith={}'
    METEO_URL = 'http://meteo.ua/{}/{}/14-days'
    HEADERS = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, lzma, sdch",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
        "Cookie": "PHPSESSID=vvk5heht348322k8ltkebqtjn7; lang=ru; "
                  "lastCities=YToxOntpOjM0O2E6Mzp7czo3OiJjaXR5X2lkIjtpOjM0O3M6NzoibmFtZV91YSI7czo4OiLQmtC40ZfQsiI7czo3O"
                  "iJuYW1lX3J1IjtzOjg6ItCa0LjQtdCyIjt9fQ%3D%3D; b=b; __utmt=1; __utma=1.1368481891."
                  "1508610653.1508610653.1508610653.1; __utmb=1.1.10.1508610653; __utmc=1; __utmz=1.1508610653.1.1."
                  "utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "Host": "meteo.ua",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://meteo.ua/",
        "SE-Proxy-Authorization": "[146 bytes were stripped]",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/46.0.2490.76 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }


    def meteo_get_city_names(self, meteo_city, headers=HEADERS):
        try:
            content_json = requests.get(self.METEO_URL_SEARCH.format(meteo_city), headers=headers)
            return content_json
        except Exception as e:
            print(e)
            exit()


    def meteo_parse_region(self, content_json):
        try:
            js = json.loads(content_json.text)
            region_list = []
            for i in js['cities']:
                reg = i['country_ru'], i['region_ru'], i['district_name_ru'],i['city_ru']
                region_list.append(reg)
            print('from METEO.UA')
            for r in enumerate(region_list):
                print(r)
            return region_list
        except Exception as e:
            print(e)


    def meteo_parse_city(self,content_json, choice_city_meteo,region_list):
        try:
            js = json.loads(content_json.text)
            pars_json = (js['cities'][choice_city_meteo])
            city_id = pars_json['city_id']
            meteo_region = region_list[choice_city_meteo]
            return city_id, meteo_region
        except Exception as e:
            print(e)


    def get_html_city_meteo(self, name_city, cit_id):
        try:
            html_content = requests.get(self.METEO_URL.format(cit_id, name_city))
            return html_content
        except Exception as e:
            print(e)
            exit()


    def parse(self,html_content, date):
        try:
            soup = BeautifulSoup(html_content.text, 'lxml')
            start_parse = soup.find('dl', {'class': 'ww_block no_js'}).find('dt', id='dt_{}'.format(date))
            list_temp = []
            for d in ['min', 'max']:
                temp = start_parse.find('span', {'class': 'wwt_tmp wwt_{}'.format(d)}).text
                parse_temp = str(temp).split('\n')[1:3]
                city_temp = (''.join(parse_temp))
                list_temp.append(city_temp)
            return list_temp
        except Exception as e:
            print(e)


    def what_day(self, date_selection):
        day = datetime.datetime.today()
        today = day.strftime("%Y-%m-%d")
        t_w = day + datetime.timedelta(days=1)
        tomorrow = t_w.strftime("%Y-%m-%d")
        if date_selection == today:
            return 'today'
        elif date_selection == tomorrow:
            return 'tomorrow'
        else:
            return date_selection




