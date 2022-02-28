from datetime import datetime, timedelta, date, time

import pytz

from constants import DAYS_THAT_RELEASE_AT_6PM, SIX_PM_HOUR, NYT_TIMEZONE, TEN_PM_HOUR


class TimeHandler:

    @staticmethod
    def process_date_from_str(raw_date_str: str) -> date:
        converted_datetime = datetime.fromtimestamp(float(raw_date_str), tz=pytz.timezone(NYT_TIMEZONE))
        return TimeHandler.process_date(converted_datetime)

    @staticmethod
    def process_date(raw_date: datetime):
        next_day_date = raw_date.date() + timedelta(days=1)
        if next_day_date.weekday() in DAYS_THAT_RELEASE_AT_6PM and raw_date.hour >= SIX_PM_HOUR:
            return raw_date.date() + timedelta(days=1)
        if raw_date.hour >= TEN_PM_HOUR:
            return raw_date.date() + timedelta(days=1)
        return raw_date.date()

    @staticmethod
    def get_today() -> date:
        today_raw_date = datetime.now(pytz.timezone(NYT_TIMEZONE))
        return TimeHandler.process_date(today_raw_date)

    @staticmethod
    def get_begin_datetime_for_date(this_date: date) -> datetime:
        one_day_earlier = this_date - timedelta(days=1)
        if this_date.weekday() in DAYS_THAT_RELEASE_AT_6PM:
            begin_timestamp = datetime.combine(date=one_day_earlier,
                                               time=time(hour=SIX_PM_HOUR),
                                               tzinfo=pytz.timezone(NYT_TIMEZONE))
        else:
            begin_timestamp = datetime.combine(date=one_day_earlier,
                                               time=time(hour=TEN_PM_HOUR),
                                               tzinfo=pytz.timezone(NYT_TIMEZONE))

        return begin_timestamp

    @staticmethod
    def get_end_datetime_for_date(this_date: date) -> datetime:
        next_day = this_date + timedelta(days=1)
        if next_day.weekday() in DAYS_THAT_RELEASE_AT_6PM:
            end_timestamp = datetime.combine(date=this_date,
                                             time=time(hour=SIX_PM_HOUR),
                                             tzinfo=pytz.timezone(NYT_TIMEZONE))
        else:
            end_timestamp = datetime.combine(date=this_date,
                                             time=time(hour=TEN_PM_HOUR),
                                             tzinfo=pytz.timezone(NYT_TIMEZONE))

        return end_timestamp

    @staticmethod
    def get_timestamp_from_datetime(this_datetime: datetime) -> float:
        return this_datetime.timestamp()


if __name__ == '__main__':
    print(TimeHandler.get_today())
    print(TimeHandler.get_begin_datetime_for_date(TimeHandler.get_today()))
    print(TimeHandler.get_begin_datetime_for_date(TimeHandler.get_today()))
    print(TimeHandler.get_timestamp_from_datetime(
        TimeHandler.get_begin_datetime_for_date(
            TimeHandler.get_today()
        )
    ))
