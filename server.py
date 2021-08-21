from flask import Flask, request, jsonify, render_template
import requests
from requests.exceptions import HTTPError


app = Flask(__name__)

def get_dates(year,month,day):
    name_params= {"country":"us","day":int(day),"month":int(month)}
    nameday_url = "https://nameday.abalin.net/namedays"
    holiday_url = f"https://date.nager.at/api/v3/PublicHolidays/{int(year)}/us"
    input_date = f"{year}-{month}-{day}"
    print(input_date)
    
    try:
        resp_name = requests.post(nameday_url, params = name_params)
        resp_name.raise_for_status()
        name_data = resp_name.json()
        name_days = name_data["data"]["namedays"]["us"]

        resp_holidays = requests.get(holiday_url)
        resp_holidays.raise_for_status()
        holiday_data = resp_holidays.json()

        holiday_result = ""
        for i in holiday_data:
            if str(i["date"]) == input_date:
                holiday_result = i["name"]
            else:
                holiday_result = "no holiday on that day"

    except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
            print(f'Other error occurred: {err}')  

    return name_days, holiday_result

@app.route('/')
def index():
    return '''<h3> This is my calendar day app</h3>
            <p> Example usage: /date/?year=1976&&month=12&&day=24</p>'''
    
all_requests = []
@app.route('/date/', methods=['GET'])
def date():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    try:
        if request.method == 'GET':
            if year and month and day:
                name_days, holiday_result = get_dates(year, month, day)
                result = jsonify("holiday", holiday_result, "name_days", name_days)
                all_requests.append(str(year)+ "." +str(month)+ "." +str(day) + " " + str(name_days) + ", "+ str(holiday_result))
                return result

            else:
                raise ValueError("invalid date")

    except Exception as err:
            print(f'Other error occurred: {err}')  

@app.route('/usage',methods=['GET'])
def usage():
    return render_template('index.html', data=all_requests)

if __name__ == '__main__':
    app.run(debug=True)
