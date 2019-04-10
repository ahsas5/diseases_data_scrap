import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

base_url = 'http://www.agriculture.gov.au'
url = 'http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
ul = soup.find('a', {'href' : '/pests-diseases-weeds/plant'}).find_next('ul')
disease_links = [x['href'] for x in ul.select('.dynamic.menu-item')]
disease_details = []

for disease_link in disease_links:
    if disease_link == '/pests-diseases-weeds/plant/xylella/international-symposium-xylella-fastidiosa':
        continue

    print('Running for {}'.format(disease_link))
    full_url = base_url + disease_link
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    disease_name = soup.find(class_='pest-header-content').find('h2').get_text().strip()
    image_link = soup.find(class_='pest-header-image').find('img')['src']
    image_link_updated = base_url + image_link
    try:
        origin = soup.find(class_='pest-header-content').find_all('p')[1].find_all('strong')[1].next_sibling
    except IndexError:
        origin = soup.find(class_='pest-header-content').find_all('p')[2].find_all('strong')[1].next_sibling
    how_to_identify = soup.find_all(class_='hide')[0].get_text()
    legally_to_aus = soup.find_all(class_='hide')[1].get_text()
    secure_suspect_specimens = soup.find_all(class_='hide')[2].get_text()
    disease_details.append({
        'disease_name': disease_name,
        'image_link': image_link_updated,
        'origin': origin,
        'how_to_identify': how_to_identify,
        'legally_to_aus':legally_to_aus,
        'secure_suspect_specimens':secure_suspect_specimens
    })

df = pd.DataFrame(disease_details)
writer = ExcelWriter('disease_details_latest_2.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()


