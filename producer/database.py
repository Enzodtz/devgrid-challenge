import logging
from contextlib import contextmanager

from models import Base, Weather
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, uri):
        self._engine = create_engine(uri)

        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def get_weathers(self, user_id):
        with Session(self._engine) as session:
            return session.query(Weather).filter(Weather.user_id == user_id).all()

    def create_database(self):
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
