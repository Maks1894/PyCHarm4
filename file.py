import csv
import os
import requests
class WeatherForecast:
    def __init__(self, file_path):
        self.file = file_path
        self.data = self.read_data_from_file()

    def read_data_from_file(self):
        results = {}
        if os.path.exists(self.file):
            with open(self.file, 'r', newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    results[row[0]] = row[1]
        return results

    def save_data(self):
        with open(self.file, 'w', newline="", ) as f:
            writer = csv.writer(f)
            for day, desc in self.data.items():
                writer.writerow([day, desc])

    def get_forecast(self, date):

        cached_info = self.data.get(date)
        if cached_info:
            return cached_info
        else:
            url = f'https://api.open-meteo.com/v1/forecast?latitude=51.107883&longitude=17.038538&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}'
            print("Pobieram danne z API")
            respons = requests.get(url)
            if respons.status_code == 200:
                datas = respons.json()
                rain = datas['daily']['rain_sum'][0]
                if rain > 0.0:
                    rain_wynik = "Bedzie padac"
                elif rain == 0.0:
                    rain_wynik = "Nie bedzie padac"
                else:
                    rain_wynik = 'Nie wiem'
                self.data[date] = rain_wynik
                self.save_data()
                return rain_wynik
            else:
                return None
    def __getitem__(self, item):
        if info := self.data.get(item):
            return info
        return None
    def __setitem__(self, key, value):
        self.data[key] = value
        self.save_data()
    def __iter__(self):
        return iter(self.data)

    def items(self):
        for day, desc in self.data.items():
            yield (day, desc)
