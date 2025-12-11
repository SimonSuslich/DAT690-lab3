from bs4 import BeautifulSoup
import json
import sys


INPUT_FILE = 'tram/templates/tram/hallplatser.html'
OUTPUT_FILE = 'static/tramstop_url.json'
TRAM_FILE = 'static/tramnetwork.json'

TRAFFIC_URL_TEMPLATE = "https://avgangstavla.vasttrafik.se/?stopAreaGid={gid}"

def main(): 
    with open(TRAM_FILE, encoding="utf-8") as trams:
        tramdict = json.loads(trams.read())
        stopdict = tramdict['stops']
    with open(INPUT_FILE, encoding="utf-8") as html_file: 
        soup = BeautifulSoup(html_file, 'html.parser')
        div = soup.find('div', class_="tab-pane active")
        a_tags = div.find_all("a")
        urls = {a.text.split(',')[0].strip(): TRAFFIC_URL_TEMPLATE.format(gid=a['href'].split('/')[-1]) 
        for a in a_tags if a.text.split(',')[0].strip() in stopdict}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=4)

if __name__ == "__main__":
    main()
