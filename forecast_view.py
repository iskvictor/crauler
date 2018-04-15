class View:
    def show_sinoptic(self, temperature, region_meteo, date_selection):
        print('Welcome on sinoptic.ua')
        print('forecast in ', region_meteo)
        print('On date ', date_selection)
        print(temperature)


    def show_meteo(self, temp_meteo, region_sinop, date_selection):
        print('Welcome on meteo.ua')
        print('forecast in ', region_sinop)
        print('On date ', date_selection)
        print(temp_meteo)


    def show_gismeteo(self, temp_gismeteo, region_gis, date_selection):
        print('Welcome on gismeteo.ua')
        print('forecast in ', region_gis)
        print('On date ', date_selection)
        print(temp_gismeteo)
