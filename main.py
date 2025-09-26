import os
import phonenumbers
from phonenumbers import carrier, geocoder, parse

os.system('cls')
phnumber = input('Phone Number: ')
nr = parse(phnumber)

c = carrier.name_for_number(nr, 'en')
r = geocoder.description_for_number(nr, 'en')

print(c + ' ' + r)