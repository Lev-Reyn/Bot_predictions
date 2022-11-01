from datetime import timedelta, datetime


class MyTime:
    def __init__(self, time_predications: str):
        """принимает время, в которое отправляется предсказание в таком виде '11:14'"""
        self.hour_predication = int(time_predications.split(':')[0])
        self.minutes_predication = int(time_predications.split(':')[1])

    def next_prediction_func(self):
        now = datetime.now()
        if (now.hour > self.hour_predication) or (
                now.hour == self.hour_predication and now.minute > self.minutes_predication):
            self.prediction = timedelta(days=1, hours=self.hour_predication, minutes=self.minutes_predication)
            prediction_next = str(self.prediction - timedelta(hours=now.hour, minutes=now.minute))[:-3]
        else:
            self.prediction = timedelta(hours=self.hour_predication, minutes=self.minutes_predication)
            prediction_next = str(self.prediction - timedelta(hours=now.hour, minutes=now.minute))[:-3]
        return prediction_next
