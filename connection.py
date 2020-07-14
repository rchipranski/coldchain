import network
import urequests
import requests
import json
from machine import ADC
import time

import sqlite3

conn = sqlite3.connect('local.db')

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

def do_connect():
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect('AndroidRFC', 'm1d0r1y4')
    while not sta_if.isconnected():
      pass
  print('network config', sta_if.ifconfig())
 
adc0=ADC(0)
do_connect()
URL = "https://aircprd.pythonanywhere.com/"

while True:
  send_url = 'http://freegeoip.net/json'
  r = requests.get(send_url)
  j = json.loads(r.text)
  lat = j['latitude']
  lon = j['longitude']
  localization = (lat,lon)
  
  volt = (adc0.read() / 2048.0) * 3300
  temp = volt * 0.1
  if do_connect():
    DATA = (localization, temp)
    response = urequests.post(URL, DATA)
    print(response.status_code)
  else:
    conn.execute("INSERT INTO BACKUP (LOCAL, TEMP) \ VALUES (%s, %s)" %(localization, temp))
  time.sleep(5*60)

conn.close()

