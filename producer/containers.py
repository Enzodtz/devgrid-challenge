from dependency_injector import containers, providers
from kafka import KafkaProducer
from database import Database
from repositories import WeatherRepository
from os import getenv


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["endpoints"])

    config = providers.Configuration(
        yaml_files=[f"config.{getenv('ENVIRONMENT', 'default')}.yml"]
    )

    db = providers.Singleton(Database, uri=config.db.uri)
    kafka_producer = providers.Singleton(
        KafkaProducer, bootstrap_servers=config.kafka.uri
    )

    weather_repository = providers.Singleton(
        WeatherRepository, session_factory=db.provided.session
    )
