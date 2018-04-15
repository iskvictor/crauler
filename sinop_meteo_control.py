from crauler import sinop_mod
from crauler import meteo_mod
from crauler import gismeteo_mod
from crauler import forecast_view
import datetime

class Sinoptik_contr():
    sin_intr = sinop_mod.Sinoptic_model()
    meteo_intr = meteo_mod.Meteo_model()
    gis_intr = gismeteo_mod.Gismeteo_model()
    view_intr = forecast_view.View()

    def __init__(self):
        self.main()


    def city_search(self):
        try:
            first_letters_city = input("Enter the first letters of your settlement:")
            return first_letters_city
        except ValueError:
            print('Invalid number')
            exit()


    def choice_region(self):
        try:
            selection_of_city = int(input("Enter the ordinal number of your settlement:"))
            return selection_of_city
        except ValueError:
            print('Invalid number')
            exit()


    def date(self):
        try:
            start = datetime.datetime.today().date()
            end = start + datetime.timedelta(days=10)
            dates = []
            while start < end:
                dates.append(start.strftime('%Y-%m-%d'))
                start = start + datetime.timedelta(days=1)
            for d in enumerate(dates):
                print(d)
            enter_date = int(input("Enter the ordinal number of date:"))
            date_selection = dates[enter_date]
            return date_selection
        except ValueError:
            print('Invalid number')
            exit()


    def main(self):
        #sinoptic
        selection_of_city = self.city_search()
        city_names = self.sin_intr.get_city_names(selection_of_city)
        cities = self.sin_intr.split_city_names(city_names)
        self.sin_intr.print_cities(cities)
        selection_of_city = self.choice_region()
        meteo_city, sin_city,region_sinop = self.sin_intr.selection_city(selection_of_city, cities)
        date_selection = self.date()
        temp_city = self.sin_intr.get_forecast_for_2_days(sin_city, date_selection)
        temperature =self.sin_intr.parsing_forecast_for_2_days(temp_city)
        #meteo
        content_json = self.meteo_intr.meteo_get_city_names(meteo_city)
        region_list = self.meteo_intr.meteo_parse_region(content_json)
        choice_city_meteo = self.choice_region()
        city_id, region_meteo = self.meteo_intr.meteo_parse_city(content_json, choice_city_meteo, region_list)
        html_content = self.meteo_intr.get_html_city_meteo(meteo_city, city_id)
        day = self.meteo_intr.what_day(date_selection)
        temp_meteo = self.meteo_intr.parse(html_content, day)
        #gismeteo
        html_gis= self.gis_intr.get_html(date_selection, meteo_city)
        cities, links = self.gis_intr.get_city_gis(html_gis)
        self.gis_intr.list_of_cities_gis(cities)
        choice_region_gis = self.choice_region()
        http_gis = links[choice_region_gis]
        region_gismeteo = (cities[choice_region_gis])
        req_http = self.gis_intr.send_req(http_gis)
        index = self.gis_intr.parse_date_index(req_http, date_selection)
        temp_gismeteo = self.gis_intr.parse_14_day(req_http, index)

        print('------------------------------------')
        self.view_intr.show_sinoptic(temperature, region_sinop, date_selection)
        print('------------------------------------')
        self.view_intr.show_meteo(temp_meteo, region_meteo,date_selection)
        print('------------------------------------')
        self.view_intr.show_gismeteo(temp_gismeteo, region_gismeteo, date_selection)

temp = Sinoptik_contr()





















