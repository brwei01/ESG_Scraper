import requests
import os
import json

def download_files(url, output_dir):
    response = requests.get(url)
    data = response.json()

    total_records = data['recordCnt']

    # Modify and update the URL
    # url = url.replace('rowRange=10', f'rowRange={total_records}')
    url = url.replace('rowRange=10', 'rowRange=50')
    response = requests.get(url)
    data = response.json()

    # Parse JSON
    files_info = data['result']
    files_info = json.loads(files_info)

    # download files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_info in files_info:
        file_link = 'https://www1.hkexnews.hk' + file_info['FILE_LINK']
        title = file_info['TITLE'].replace('\n', ' ').replace('/', '_')
        title = title[:200]  # Limit filename length to 200 characters
        file_extension = file_info['FILE_LINK'].split('.')[-1]
        file_name = f"{title}.{file_extension}"
        file_path = os.path.join(output_dir, file_name)

        print(f'Downloading {file_name}...')
        file_response = requests.get(file_link)
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
        print(f'{file_name} downloaded successfully.')


url = 'https://www1.hkexnews.hk/search/titleSearchServlet.do?sortDir=0&sortByOptions=DateTime&category=0&market=SEHK&stockId=-1&documentType=-1&fromDate=20240612&toDate=20240712&title=&searchType=0&t1code=-2&t2Gcode=-2&t2code=-2&rowRange=10&lang=E'
output_dir = 'D:/Dev/downloads'
download_files(url, output_dir)
