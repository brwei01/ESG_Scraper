import requests
import os
import json
import re
from datetime import datetime

def download_files(url, output_dir, esg_pattern):
    response = requests.get(url)
    data = response.json()

    total_records = data['recordCnt']
    # log total records
    print(total_records)

    # Modify and update the URL
    # url = url.replace('rowRange=10', f'rowRange={total_records}')
    # replace the line below with above
    url = url.replace('rowRange=10', 'rowRange=1000')
    response = requests.get(url)
    data = response.json()

    # Parse JSON
    files_info = data['result']
    files_info = json.loads(files_info)

    # download files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_info in files_info:
        title = file_info['TITLE']

        if esg_pattern.search(title):
            file_link = 'https://www1.hkexnews.hk' + file_info['FILE_LINK']
            title = title[:200]  # Limit filename length to 200 characters
            file_extension = file_info['FILE_LINK'].split('.')[-1]
            file_name = f"{title}.{file_extension}"
            file_path = os.path.join(output_dir, file_name)

            print(f'Downloading {file_name}...')
            file_response = requests.get(file_link)
            with open(file_path, 'wb') as file:
                file.write(file_response.content)
            print(f'{file_name} downloaded successfully.')


url1 = 'https://www1.hkexnews.hk/search/titleSearchServlet.do?sortDir=0&sortByOptions=DateTime&category=0&market=SEHK&stockId=-1&documentType=-1&fromDate='
from_date = '20240612'
to_date = '20240712'
# to_date = datetime.today().strftime('%Y%m%d')

url2 = '&title=&searchType=0&t1code=-2&t2Gcode=-2&t2code=-2&rowRange=10&lang=E'
url = url1 + from_date + to_date + '&toDate=' + url2
output_dir = 'D:/Dev/downloads'
esg_pattern = re.compile(r'\b(ESG|environment|environmental)\b', re.IGNORECASE)
download_files(url, output_dir, esg_pattern)
