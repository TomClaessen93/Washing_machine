from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker
import math
from datetime import datetime


class MainApp(MDApp):
    from datetime import datetime
    time = datetime.strptime("8:00:00", '%H:%M:%S').time()
    duration =datetime.strptime("8:00:00", '%H:%M:%S').time()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('time.kv')

    def print_some_info(self):
        pass

    def get_time(self, instance, time):
        self.time = str(time)[0:5]
        self.root.ids.time_label.text = f'time = {self.time}'

    def get_duration(self,instance,time):
        self.duration = str(time)[0:5]
        self.root.ids.time_label.text = f' duration = {self.duration}'

    # Cancel
    def on_cancel(self, instance, time):
        self.root.ids.time_label.text = "You Clicked Cancel!"

    def show_duration_picker(self):
        from datetime import datetime

        # Define default time
        default_time = datetime.strptime("2:40:00", '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        # Set default Time
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, time=self.get_duration)
        time_dialog.open()

    def show_time_picker(self):
        from datetime import datetime

        # Define default time
        default_time = datetime.strptime("8:00:00", '%H:%M:%S').time()

        time_dialog = MDTimePicker()
        # Set default Time
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, time=self.get_time)
        time_dialog.open()

    def assertTime(self,time: str):
        assert len(time) == 5, 'Please use the format 00:00 for the time'
        assert time[0:2].isdigit() and time[3:5].isdigit(), 'Please use the format 00:00 for the time'
        assert time[2] == ':', 'Please use the format 00:00 for the time'

    def timeToSeconds(self,time: str):

        self.assertTime(time)

        ftr = [3600, 60]
        return sum([a * b for a, b in zip(ftr, map(int, time.split(':')))])

    def seconds2String(self,sec: int):
        hours, remainder = divmod(sec, 3600)
        minutes, seconds = divmod(remainder, 60)

        return '{:02}:{:02}'.format(int(hours), int(minutes))

    def getStartTime(self,endTime, duration):

        import datetime
        endTimeSeconds = self.timeToSeconds(endTime)
        durationSeconds = self.timeToSeconds(duration)
        startTimeSeconds = endTimeSeconds - durationSeconds

        if startTimeSeconds < 0:
            startTimeSeconds = 24 * 3600 + startTimeSeconds

        return self.seconds2String(startTimeSeconds)

    def getOffset(self):

        endTime = str(self.time)[0:5]
        duration = str(self.duration)[0:5]
        now =  now=datetime.now().strftime("%H:%M")

        startTimeSeconds = self.timeToSeconds(self.getStartTime(endTime, duration))
        nowSeconds = self.timeToSeconds(now)

        if nowSeconds > startTimeSeconds:
            offSet = (24 * 3600 - nowSeconds) + startTimeSeconds
        else:
            offSet = nowSeconds - startTimeSeconds

        self.root.ids.time_label.text = self.seconds2String(offSet)

        return self.seconds2String(offSet)

    def getMinutes(self,minutes: str):
        return int(minutes.split(':')[1])

    def getHours(self,hours: str):
        return int(hours.split(':')[0])

    def getOptimalOffset(self):

        endTime = str(self.time)[0:5]
        duration = str(self.duration)[0:5]
        increment = 15
        now=datetime.now().strftime("%H:%M")

        offSet = self.getOffset(endTime, duration, now)
        minutes = self.getMinutes(now)
        hours = self.getHours(offSet)

        if math.fabs(minutes - (minutes // increment * increment)) < math.fabs(
                minutes - (minutes // increment * increment + increment)):
            optimalMinutes = (minutes // increment) * increment
        else:
            optimalMinutes = minutes // increment * increment + increment

        self.root.ids.time_label.text = str(hours) + str(':') + str(optimalMinutes)


MainApp().run()