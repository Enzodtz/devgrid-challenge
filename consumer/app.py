from kafka import KafkaConsumer
from constants import TOPIC

from handler import handler
from dependency_injector.wiring import inject, Provide
from containers import Container


@inject
def main(kafka_consumer: KafkaConsumer = Provide[Container.kafka_consumer]):
    kafka_consumer.subscribe([TOPIC])

    for message in kafka_consumer:
        handler(message)


container = Container()

db = container.db()
db.create_database()

container.wire(modules=[__name__, "handler"])

if __name__ == "__main__":
    main()
