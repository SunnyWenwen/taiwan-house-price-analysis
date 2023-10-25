import datetime
import os

import requests

save_zip_file_path = "data\\zip_data"

if not os.path.isdir(save_zip_file_path):
    os.makedirs(save_zip_file_path, exist_ok=True)

# for test
response = requests.get(f"https://plvr.land.moi.gov.tw/DownloadSeason?season=110S4&type=zip&fileName=lvr_landcsv.zip")
# [200] is success
if response.ok:
    print('Test download is Success')
else:
    raise BaseException('Test download is failed')


# start download raw data from gov web
today_year = datetime.datetime.today().year-1911
season_list = ['S' + str(i) for i in range(1, 5)]
year_list = list(str(x) for x in range(101, today_year+1))

for year in year_list:
    for season in season_list:
        filename = f"{year}_{season}"
        print(f"Start download {filename}")
        response = requests.get(
            f"https://plvr.land.moi.gov.tw/DownloadSeason?season={year}{season}&type=zip&fileName=lvr_landcsv.zip")
        if response.ok:
            with open(f'{save_zip_file_path}\\{filename}.zip', 'wb') as file:
                file.write(response.content)
                file.close()
            print(f"Success download {filename}")
        else:
            print(f"Error in download {filename}")
