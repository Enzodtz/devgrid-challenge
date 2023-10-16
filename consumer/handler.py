import time
from dependency_injector.wiring import Provide, inject
from repositories import WeatherRepository, OpenWeatherAPIRepository
from containers import Container


@inject
def _handle(
    message,
    open_weather_api_repository: OpenWeatherAPIRepository = Provide[
        Container.open_weather_api_repository
    ],
    weather_repository: WeatherRepository = Provide[Container.weather_repository],
):
    data = open_weather_api_repository.get_weathers(message.value)
    user_id = message.key.split("_")[0]
    weather_repository.save_weathers(user_id, data["list"])


def handler(message):
    """
    Given that we can only view data from 60 cities within a minute,
    it means that for every second we should see only one city. Then,
    we wait the necessary time in order to handle again
    """

    t_start = time.time()
    min_time = len(message.value)  # * 1 second

    _handle(message)

    delta = time.time() - t_start
    if delta < min_time:
        print("Processed 1 message, waiting to process next:", min_time - delta)
        time.sleep(min_time - delta)
