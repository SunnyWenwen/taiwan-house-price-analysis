import datetime

from download_data import download_house_price_data, download_income_data
from preprocess_data import preprocess_income_data, preprocess_house_price_data, unzip_house_price_data

# setting
result_path = "data/result/"  # path for save processed data

zip_dir_path = "data/zip_data/"  # zip file location
house_price_data_path = "data/house_price_xls/"  # xls(unzip) file location
income_data_path = "data/income/"
start_year = 105  # The year start download
city_code_filter = ['o', 'j', 'k']  # city code, mapping table can see 'doc/縣市代碼'

if __name__ == '__main__':
    # download data
    download_house_price_data(zip_dir_path, start_year)
    download_income_data(income_data_path, start_year, city_code_filter)

    # preprocess data
    unzip_house_price_data(zip_dir_path, house_price_data_path)
    preprocess_house_price_data(house_price_data_path, result_path, start_year, city_code_filter)
    preprocess_income_data(income_data_path, result_path, start_year, city_code_filter)
