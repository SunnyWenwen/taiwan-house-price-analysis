import datetime

from download_house_price import download_house_price_zip_data_from_gov_web
from download_income import download_income_pdf_data_from_gov_web
from read_and_merge import read_merge_rename
from unzip_house_price import unzip_data

# parameter
zip_dir_path = "data\\zip_data\\"  # zip file location
house_price_data_path = "data\\house_price_xls\\"  # xls(unzip) file location
income_data_path = "data/income"
start_year = 106  # The year start download
city_code_filter = ['o']  # city code, mapping table can see 'doc/縣市代碼'

if __name__ == '__main__':
    download_house_price_zip_data_from_gov_web(zip_dir_path, start_year)
    unzip_data(zip_dir_path, house_price_data_path)
    read_merge_rename(house_price_data_path, start_year, city_code_filter)
    download_income_pdf_data_from_gov_web(income_data_path, start_year, city_code_filter)