from unittest import mock

from app import main, container, db
from repositories import WeatherRepository, OpenWeatherAPIRepository
from models import Weather
import time


class MockMsg:
    """
    Generates a mock message from the kafka consumer.
    Notice that since it has methods to parse received message
    (decode, json.loads), we don't pass it as byte str.
    """

    key = "1_1"
    value = ["123"]


def mock_api_response():
    return {
        "list": [
            {
                "id": 123,
                "main": {
                    "temp": 1.0,
                    "humidity": 1.0,
                },
            }
        ]
    }


def test_subscription():
    """
    Tests if it subscribed to topic.
    """

    consumer_mock = mock.MagicMock()
    consumer_mock.__iter__.return_value = []

    with container.kafka_consumer.override(consumer_mock):
        main()

    assert consumer_mock.subscribe.called


def test_get_save_data():
    """
    Tests if it gets and saves data
    """

    consumer_mock = mock.MagicMock()
    consumer_mock.__iter__.return_value = [MockMsg()]

    open_weather_api_repository_mock = mock.Mock(spec=OpenWeatherAPIRepository)
    open_weather_api_repository_mock.get_weathers.return_value = mock_api_response()

    with (
        container.kafka_consumer.override(consumer_mock),
        container.open_weather_api_repository.override(
            open_weather_api_repository_mock
        ),
    ):
        main()

    with db.session() as session:
        data = session.query(Weather).all()

        assert len(data) == 1

        weather = data[0]

        assert weather.city_id == 123
        assert weather.temperature == 1.0
        assert weather.humidity == 1.0
        assert weather.user_id == 1


def test_waiting():
    """
    Tests if it waits after get the message
    """

    consumer_mock = mock.MagicMock()
    consumer_mock.__iter__.return_value = [MockMsg()]

    open_weather_api_repository_mock = mock.Mock(spec=OpenWeatherAPIRepository)
    open_weather_api_repository_mock.get_weathers.return_value = mock_api_response()

    weather_repository_mock = mock.Mock(spec=WeatherRepository)

    with (
        container.kafka_consumer.override(consumer_mock),
        container.weather_repository.override(weather_repository_mock),
        container.open_weather_api_repository.override(
            open_weather_api_repository_mock
        ),
    ):
        t_start = time.time()
        main()
        delta = time.time() - t_start

    assert delta > 1
