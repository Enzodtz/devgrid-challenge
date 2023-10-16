import json

from constants import CITIES_ID, TOPIC
from containers import Container
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from kafka import KafkaProducer
from pydantic import BaseModel

from .router import router


class RequestBody(BaseModel):
    id: str


@router.post("/collect/")
@inject
async def produce_weather_msg(
    body: RequestBody,
    kafka_producer: KafkaProducer = Depends(Provide[Container.kafka_producer]),
):
    """
    Receive user defined ID. Split cities into batches of 20
    and send the batches as messages with the corresponding ID.
    """

    for i in range(int(len(CITIES_ID) / 20 + 1)):
        batch = CITIES_ID[i * 20 : (i + 1) * 20]
        key = f"{body.id}_{i}"

        kafka_producer.send(
            topic=TOPIC,
            key=key.encode(),
            value=json.dumps(batch).encode(),
        )

    return {"id": body.id}
