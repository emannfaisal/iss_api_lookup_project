import requests
import smtplib
from datetime import datetime
import time

my_lat = 31.450365
my_long = 73.134964
my_email = "efaisal375@gmail.com"
my_password = "gbkw bhnq ckbe puxy"

def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    return iss_lat,iss_long


def is_iss_overhead():
    iss_lat,iss_long = get_iss_position()
    if my_lat-5 <= iss_lat <= my_lat+5 and my_long-5 <= iss_long <= my_long+5:
        return True


def is_night():
    parameters={
        "lat":my_lat,
        "long":my_long,
        "formatted":0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[1])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[1])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False



while True:
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_email,my_password)
        connection.sendmail(from_addr=my_email,to_addrs="kitchentte796@gmail.com",msg="SUBJECT: LOOK uP!\n\n The iss is above you in the sky")
        time.sleep(60)
