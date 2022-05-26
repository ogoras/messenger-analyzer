from categorizing.message_categorizer import MessageCategorizer
from abc import abstractmethod
from datetime import datetime

class TimeCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        return self.categorize_time(message["timestamp_ms"])

    @abstractmethod
    def categorize_time(self, time):
        pass

class YearCategorizer(TimeCategorizer):
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).year

class MonthCategorizer(TimeCategorizer):
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).month

class DayCategorizer(TimeCategorizer): #day of month
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).day

class HourCategorizer(TimeCategorizer):
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).hour
    
class MinuteCategorizer(TimeCategorizer): #probably useless
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).minute

class SecondCategorizer(TimeCategorizer): #probably useless
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).second

class WeekdayCategorizer(TimeCategorizer):
    def categorize_time(self, time):
        return datetime.fromtimestamp(time/1000).weekday()