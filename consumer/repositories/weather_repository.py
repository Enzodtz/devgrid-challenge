from models import Weather


class WeatherRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save_weathers(self, user_id, weathers):
        with self.session_factory() as session:
            weathers = [
                Weather(
                    user_id=user_id,
                    city_id=w["id"],
                    temperature=w["main"]["temp"],
                    humidity=w["main"]["humidity"],
                )
                for w in weathers
            ]
            session.bulk_save_objects(weathers)
            session.commit()
