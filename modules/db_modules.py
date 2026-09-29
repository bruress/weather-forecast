from sqlalchemy import create_engine, Integer, String, Date, DateTime, Float, UniqueConstraint, select, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from datetime import date, timedelta, datetime

def define_db (db_url):
    # create sqlite
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # create db
    Base = declarative_base()

    class WeatherForecast (Base):
        __tablename__ = "weather_forecast"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        city: Mapped[str] = mapped_column(String, nullable=False)
        forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
        temp_min: Mapped[float] = mapped_column(Float, nullable=False)
        temp_max: Mapped[float] = mapped_column(Float, nullable=False)
        humidity: Mapped[int] = mapped_column(Integer, nullable=False)
        wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
        description: Mapped[str] = mapped_column(String, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

        __table_args__ = (
            UniqueConstraint(
                "city",
                "forecast_date"
            ),
        )

    Base.metadata.create_all(engine)