from models import Weather


class WeatherRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_weathers(self, user_id):
        with self.session_factory() as session:
            return session.query(Weather).filter(Weather.user_id == user_id).all()
