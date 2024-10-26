import datetime as dt

class DateTime:
    
    @staticmethod
    def getdatetime() -> str:
        date_time = dt.datetime.now()
        date_time = date_time.strftime(r'%Y-%m-%d %H:%M:%S')
        return date_time