from unittest import mock

from constants import CITIES_ID
from models import Weather
from repositories import WeatherRepository
from app import app


def test_get_list(client):
    """
    Test that function will return correct weather.
    """

    repository_mock = mock.Mock(spec=WeatherRepository)
    repository_mock.get_weathers.return_value = [
        Weather(
            user_id=1,
            city_id=1,
            temperature=1.0,
            humidity=1.0,
            created_date="2023-10-13T05:55:50",
        ),
    ]

    with app.container.weather_repository.override(repository_mock):
        response = client.get("/get/")

    assert response.status_code == 200
    data = response.json()

    assert data == {
        "progress": 1 / len(CITIES_ID),
        "data": [
            {
                "city_id": 1,
                "temperature": 1.0,
                "datetime": "2023-10-13T05:55:50",
                "humidity": 1.0,
            }
        ],
    }
