from dependency_injector import containers, providers
from kafka import KafkaConsumer
from os import getenv
from repositories import OpenWeatherAPIRepository, WeatherRepository
from database import Database
import json


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=[f"config.{getenv('ENVIRONMENT', 'default')}.yml"]
    )

    db = providers.Singleton(Database, uri=config.db.uri)

    kafka_consumer = providers.Singleton(
        KafkaConsumer,
        bootstrap_servers=["kafka:9092"],
        auto_offset_reset="earliest",
        group_id="1",
        value_deserializer=lambda x: json.loads(x.decode("ascii")),
        key_deserializer=lambda x: x.decode("ascii"),
    )

    open_weather_api_repository = providers.Singleton(
        OpenWeatherAPIRepository,
        url=config.open_weather_api.url,
        key=config.open_weather_api.key,
    )

    weather_repository = providers.Singleton(
        WeatherRepository, session_factory=db.provided.session
    )
