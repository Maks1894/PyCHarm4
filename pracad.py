
import requests
import datetime
import csv
import os
cache_file = ("cache.csv")
results = {}
if os.path.exists(cache_file):
    with open(cache_file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            results[row[0]] = {'desc': row[1]}
else:
    results = {}
print('Witam w programie meteorologicznym')

def get_pogoda_infp():
    data=input('Podaj date dla ktorej sprawdzamy pogodę. Data musi byc w formacie YYYY-mm-dd lub naciśnij Enter, aby użyć jutrzejszej daty: ')
    if not data:
        next_day = datetime.date.today() + datetime.timedelta(days=1)
        next_data= next_day.strftime('%Y-%m-%d')
        print(f"Nie podales daty, używam daty na następny dzień: {next_data}")

        return next_data
    else:
        try:
            datetime.datetime.strptime(data, '%Y-%m-%d')
            print(f"Podano datę: {data}")
            return data
        except ValueError:
            print("Błąd: Podana data nie jest w poprawnym formacie YYYY-mm-dd.")
            return None

if __name__ == "__main__":
    data = get_pogoda_infp()
    if data:
        if data in results:
            print("Pobieram danne z cahce")
            print(f"Prognoza na {data}: {results[data]['desc']}")
        else:
            url = f'https://api.open-meteo.com/v1/forecast?latitude=51.107883&longitude=17.038538&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={data}&end_date={data}'
            print("Pobieram danne z API")
            respons= requests.get(url)
            if respons.status_code == 200:
                datas = respons.json()
                rain = datas['daily']['rain_sum'][0]
                if rain > 0.0:
                    rain_wynik= "Bedzie padac"
                elif rain == 0.0:
                    rain_wynik= "Nie bedzie padac"
                else:
                    rain_wynik= 'Nie wiem'

                results[data] = {'desc': rain_wynik}
                print(f"Prognoza na {data}: {results[data]['desc']}")
                with open(cache_file, 'w',  newline="") as f:
                    writer = csv.writer(f)
                    for day, info in results.items():
                        writer.writerow([day, info['desc']])
            else:
                print("Blad")
    else:
        print("Nie mogę sprawdzić pogody, ponieważ data nie została poprawnie podana.")
