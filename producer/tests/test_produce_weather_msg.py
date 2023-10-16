from unittest import mock

from app import app
from kafka import KafkaProducer
from constants import CITIES_ID


def test_produce_weather_msg(client):
    """
    Test that function will return correct weather.
    """
    producer_mock = mock.Mock(spec=KafkaProducer)

    with app.container.kafka_producer.override(producer_mock):
        response = client.post("/collect/", json={"id": 1})

    assert response.status_code == 200

    assert producer_mock.send.call_count == int(len(CITIES_ID) / 20 + 1)
