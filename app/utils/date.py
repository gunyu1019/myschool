import datetime
from app.models.nugu import Parameter


class DateConvert:
    def __init__(self, dt: datetime.datetime, name: str):
        self.format = name
        self.datetime = dt

    @property
    def date(self) -> datetime.date:
        return self.datetime.date()

    @staticmethod
    def add_days(source, count):
        target = source + datetime.timedelta(days=count)
        return target

    @staticmethod
    def get_first_date(source):
        temporary = datetime.datetime(source.year, source.month, source.day)
        day_count = temporary.weekday()
        target = DateConvert.add_days(temporary, -day_count)
        return target

    @staticmethod
    def get_last_date(source):
        temporary = DateConvert.get_first_date(source)
        target = DateConvert.add_days(temporary, 5)
        return target

    @staticmethod
    def change_weekday(weekday):
        weekday_data = {
            0: "월요일",
            1: "화요일",
            2: "수요일",
            3: "목요일",
            4: "금요일",
            5: "토요일",
            6: "일요일"
        }
        return weekday_data[weekday]

    @classmethod
    def from_parameter(cls, param1: Parameter, param2: Parameter = Parameter.empty()):
        now = datetime.datetime.now()
        if param1.type is None and param1.value == "TODAY":
            if param2.type == "BID_DT_WEEK":
                week = param2.value
                if week == "W.0":
                    return cls(now, "이번주")
                elif week == "W.1":
                    return cls(cls.add_days(now, 7), "다음주")
                elif week == "W.2":
                    return cls(cls.add_days(now, 14), "다다음주")
                elif week == "W.3":
                    return cls(cls.add_days(now, 21), "다다다음주")
                elif week == "W.-1":
                    return cls(cls.add_days(now, -7), "지난주")
                elif week == "W.-2":
                    return cls(cls.add_days(now, -14), "지지난주")
                elif week == "W.-3":
                    return cls(cls.add_days(now, -21), "지지지난주")
            return cls(now, "오늘")

        if param1.type == "BID_DT_DAY":
            if "TODAY" == param1.value:
                return cls(now, "오늘")
            elif "TOMORROW" == param1.value:
                return cls(cls.add_days(now, 1), "내일")
            elif "A_TOMORROW" == param1.value:
                return cls(cls.add_days(now, 2), "내일모레")
            elif "AA_TOMORROW" == param1.value:
                return cls(cls.add_days(now, 3), "글피")
            elif "AAA_TOMORROW" == param1.value:
                return cls(cls.add_days(now, 4), "그글피")
            elif "YESTERDAY" == param1.value:
                return cls(cls.add_days(now, -1), "어제")
            elif "B_YESTERDAY" == param1.value:
                return cls(cls.add_days(now, -2), "그저께")
            elif "BB_YESTERDAY" == param1.value:
                return cls(cls.add_days(now, -3), "그그저께")
            else:
                return None
        elif param1.type == "BID_DT_MDAY":
            month = now.month
            if param2.type == "BID_DT_YMONTH":
                month = param2.value
            days = param1.value
            try:
                dt = datetime.datetime(now.year, int(month), int(days))
            except ValueError:
                return
            return cls(dt, "{0}월 {1}일".format(month, days))
        elif param1.type == "BID_DT_WDAY":
            first_day = cls.get_first_date(now)

            if param1.value.startswith("SUN"):
                if param1.value == "SUN.W.-1":
                    week_day = cls.add_days(first_day, -1)
                    week_name = "지난주 일요일"
                elif param1.value == "SUN.W.-2":
                    week_day = cls.add_days(first_day, -8)
                    week_name = "지지난주 일요일"
                elif param1.value == "SUN.W.1":
                    week_day = cls.add_days(first_day, 13)
                    week_name = "다음주 일요일"
                elif param1.value == "SUN.W.2":
                    week_day = cls.add_days(first_day, 20)
                    week_name = "다다음주 일요일"
                else:
                    week_day = cls.add_days(first_day, 6)
                    week_name = "일요일"
                return cls(week_day, week_name)
            elif param1.value.startswith("WEEKBEGIN"):
                if param1.value == "WEEKBEGIN.W.-1":
                    week_day = cls.add_days(first_day, -7)
                    week_name = "지난주 월요일"
                elif param1.value == "WEEKBEGIN.W.-2":
                    week_day = cls.add_days(first_day, -14)
                    week_name = "지지난주 월요일"
                elif param1.value == "WEEKBEGIN.W.1":
                    week_day = cls.add_days(first_day, 7)
                    week_name = "다음주 월요일"
                elif param1.value == "WEEKBEGIN.W.2":
                    week_day = cls.add_days(first_day, 14)
                    week_name = "다다음주 월요일"
                else:
                    week_day = first_day
                    week_name = "월요일"
                return cls(week_day, week_name)
            elif param1.value == "MON":
                week_day = first_day
                week_name = "월요일"
            elif param1.value == "TUE":
                week_day = cls.add_days(first_day, 1)
                week_name = "화요일"
            elif param1.value == "WED":
                week_day = cls.add_days(first_day, 2)
                week_name = "수요일"
            elif param1.value == "THU":
                week_day = cls.add_days(first_day, 3)
                week_name = "목요일"
            elif param1.value == "FRI":
                week_day = cls.add_days(first_day, 4)
                week_name = "금요일"
            elif param1.value == "SAT":
                week_day = cls.add_days(first_day, 5)
                week_name = "토요일"
            else:
                return

            if param2.type == "BID_DT_WEEK":
                week = param2.value
                if week == "W.0":
                    week_name = "이번주 " + week_name
                elif week == "W.1":
                    week_name = "다음주 " + week_name
                    week_day = cls.add_days(week_day, 7)
                elif week == "W.2":
                    week_name = "다다음주 " + week_name
                    week_day = cls.add_days(week_day, 14)
                elif week == "W.3":
                    week_name = "다다다음주 " + week_name
                    week_day = cls.add_days(week_day, 21)
                elif week == "W.-1":
                    week_name = "지난주 " + week_name
                    week_day = cls.add_days(week_day, -7)
                elif week == "W.-2":
                    week_name = "지지난주 " + week_name
                    week_day = cls.add_days(week_day, -14)
                elif week == "W.-3":
                    week_name = "지지난주 " + week_name
                    week_day = cls.add_days(week_day, -21)
                return cls(week_day, week_name)
