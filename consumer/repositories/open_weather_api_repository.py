import requests
from requests.exceptions import HTTPError


class OpenWeatherAPIRepository:
    def __init__(self, url, key):
        self.url = url + key

    def get_weathers(self, cities_id):
        _url = self.url + f"&id={','.join(cities_id)}"
        response = requests.get(_url)

        if response.status_code != 200:
            raise HTTPError(response.status_code)

        return response.json()
