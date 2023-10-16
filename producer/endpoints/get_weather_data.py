from constants import CITIES_ID
from containers import Container
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from repositories import WeatherRepository
from .router import router


@router.get("/get/")
@inject
async def get_weather_data(
    id=0,
    weather_repository: WeatherRepository = Depends(
        Provide[Container.weather_repository]
    ),
):
    """
    Receives id of request and retrive current data and progress.
    """
    data = weather_repository.get_weathers(id)

    return {
        "progress": len(data) / len(CITIES_ID),
        "data": [
            {
                "city_id": d.city_id,
                "temperature": d.temperature,
                "datetime": d.created_date,
                "humidity": d.humidity,
            }
            for d in data
        ],
    }
