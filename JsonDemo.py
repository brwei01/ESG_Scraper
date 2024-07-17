import requests
import os
import json
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DateSearch():
    today_date = datetime.today()

    def getSearchWindow(self, months_ago):
        '''
        gets date search window from the given months ago
        :return: str, str
        '''
        # Update the to_date variable with today's date
        to_date_obj = self.today_date - relativedelta(months=months_ago-1)
        to_date = to_date_obj.strftime('%Y%m%d')
        # Calculate the from_date as one month before the to_date
        from_date_obj= self.to_date_obj - relativedelta(months=months_ago)
        from_date = from_date_obj.strftime('%Y%m%d')

        return from_date, to_date


class JsonRequestor():

    def download_files(self, url, output_dir, esg_pattern):
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




