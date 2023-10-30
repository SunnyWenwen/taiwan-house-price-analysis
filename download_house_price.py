import datetime
import os

import requests


def download_house_price_zip_data_from_gov_web(save_zip_file_path, start_year=101):
    # save_zip_file_path= "data\\zip_data"

    if not os.path.isdir(save_zip_file_path):
        os.makedirs(save_zip_file_path, exist_ok=True)

    # start download raw data from gov web
    today_year = datetime.datetime.today().year - 1911
    season_list = ['S' + str(i) for i in range(1, 5)]
    year_list = list(str(x) for x in range(start_year, today_year + 1))

    for year in year_list:
        for season in season_list:
            filename = f"{year}_{season}"
            print(f"Start download {filename}")
            response = requests.get(
                f"https://plvr.land.moi.gov.tw/DownloadSeason?season={year}{season}&type=zip&fileName=lvr_landxls.zip")
            if response.ok:
                with open(f'{save_zip_file_path}\\{filename}.zip', 'wb') as file:
                    file.write(response.content)
                    file.close()
                print(f"Success download {filename}")
            else:
                print(f"Error in download {filename}")


if __name__ == '__main__':
    # for test
    response = requests.get(
        f"https://plvr.land.moi.gov.tw/DownloadSeason?season=110S4&type=zip&fileName=lvr_landxls.zip")
    # [200] is success
    if response.ok:
        print('Test download is Success')
    else:
        raise BaseException('Test download is failed')

    download_house_price_zip_data_from_gov_web("data\\zip_data")
