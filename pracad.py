
import datetime
from file import WeatherForecast

def get_pogoda_infp():
    if not (date := input('Podaj date dla ktorej sprawdzamy pogodę. Data musi byc w formacie YYYY-mm-dd lub naciśnij Enter, aby użyć jutrzejszej daty: ')):
        next_data = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"Nie podales daty, używam daty na następny dzień: {next_data}")
        return next_data
    else:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            print(f"Podano datę: {date}")
            return date
        except ValueError:
            print("Błąd: Podana data nie jest w poprawnym formacie YYYY-mm-dd.")
            return None

if __name__ == "__main__":
    print('Witam w programie meteorologicznym')
    cache = WeatherForecast(file_path ="cache.csv")
    if data := get_pogoda_infp() :
        if forecast := cache.get_forecast(data):
            print(f"Prognoza na {data}: {forecast}")
        else:
            print("Blad")
    else:
        print("Nie mogę sprawdzić pogody, ponieważ data nie została poprawnie podana.")
for date, forecast in cache.items():
        print(f"Data: {date}, Prognoza: {forecast}")