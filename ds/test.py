from io import BytesIO
import requests


file_jpg = requests.get('https://api.thecatapi.com/v1/images/search?limit=1').json()
print(file_jpg)