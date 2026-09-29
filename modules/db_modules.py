from sqlalchemy import create_engine, Integer, String, Date, DateTime, Float, UniqueConstraint, select, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from datetime import date, timedelta, datetime

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

def define_db (db_url):
    # create sqlite
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()

def insert_table(session, city, forecast_dates, mins_temps, maxs_temps, avrs_hums, maxs_winds, weaher_descrs):
    try: 
        # insert
        for i in range (0, 4):
            exist = session.scalars(
                select(WeatherForecast).where(
                    WeatherForecast.city == city,
                    WeatherForecast.forecast_date == forecast_dates[i]
                )
            ).first()

            if exist is None:
                insert_stmt = WeatherForecast(
                    city=city,
                    forecast_date = forecast_dates[i],
                    temp_min = mins_temps[i],
                    temp_max = maxs_temps[i],
                    humidity = avrs_hums[i],
                    wind_speed = maxs_winds[i],
                    description = weaher_descrs[i],
                    created_at = func.now()
                )
                session.add(insert_stmt)

        session.commit()
        return insert_stmt
    
    except Exception: 
        session.rollback()
        raise


def read_table(session):
    return session.scalars(select(WeatherForecast)).all()
