import datetime

from download_house_price import download_house_price_zip_data_from_gov_web
from download_income import download_income_pdf_data_from_gov_web
from read_and_merge import preprocess_house_price_data
from read_income import preprocess_income_data
from unzip_house_price import unzip_house_price_data

# parameter
zip_dir_path = "data/zip_data/"  # zip file location
house_price_data_path = "data/house_price_xls/"  # xls(unzip) file location
income_data_path = "data/income/"
start_year = 105  # The year start download
city_code_filter = ['o', 'j']  # city code, mapping table can see 'doc/縣市代碼'
result_path = "data/result/"  # path for save cleaned data

if __name__ == '__main__':
    # download data
    download_house_price_zip_data_from_gov_web(zip_dir_path, start_year)
    download_income_pdf_data_from_gov_web(income_data_path, start_year, city_code_filter)

    # preprocess data
    unzip_house_price_data(zip_dir_path, house_price_data_path)
    preprocess_house_price_data(house_price_data_path, result_path, start_year, city_code_filter)
    preprocess_income_data(income_data_path, result_path, start_year, city_code_filter)
