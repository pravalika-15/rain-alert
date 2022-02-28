import os
from twilio.rest import Client
import requests
from twilio.http.http_client import TwilioHttpClient



account_sid = 'AC91b6f472a7ece5b80803fc44f7e675c1'
auth_token = 'e32e8015b8edc367ec84367bd2e5b1af'
api_key = 'cc7baf96b75b392b31f8ae665c427b67'
lat = 21.251385
lon = 81.629639
part = 'current,minutely,daily'
my_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}'

response = requests.get(url=my_url)
response.raise_for_status()
data = response.json()['hourly'][:12]
new_data = [hour_data['weather'][0]['id'] for hour_data in data]
will_rain = False
for i in new_data:
    if i > 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's going to rain today. don't forget to get an umbrella.",
        from_='+18507903847',
        to='+91 96187 62597'
    )

    print(message.status)