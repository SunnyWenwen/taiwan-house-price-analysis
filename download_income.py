import datetime
import os

import requests
import PyPDF2

from para import city_code_dict


def download_income_pdf_data_from_gov_web(save_income_path, start_year=101,
                                          city='all'):  # save_income_path = 'data/income'
    today_year = datetime.datetime.today().year - 1911
    year_list = list(str(x) for x in range(start_year, today_year + 1))
    for tmp_year in year_list:  # tmp_year = 109
        print(f'Start download {tmp_year} data')
        if city != 'all':
            city_list = city
        else:
            city_list = list(city_code_dict.keys())
        for tmp_city_code in city_list:  # tmp_city_code = 'O'
            tmp_city_code = tmp_city_code.upper()
            if int(tmp_year) >= 109:
                url = f'https://www.fia.gov.tw/WEB/fia/ias/isa{tmp_year}s/isa{tmp_year}/{tmp_year}_165-{tmp_city_code}.pdf'
            else:
                url = f'https://www.fia.gov.tw/WEB/fia/ias/isa{tmp_year}/isa{tmp_year}/{tmp_year}_165-{tmp_city_code}.pdf'
            response = requests.get(url)
            if response.ok:
                tmp_data_path = save_income_path + f'/city-{tmp_city_code}'
                if not os.path.isdir(tmp_data_path):
                    os.makedirs(tmp_data_path, exist_ok=True)
                tmp_data_path += f"/{tmp_year}_{tmp_city_code}.pdf"
                with open(tmp_data_path, 'wb') as f:
                    f.write(response.content)
                print(f"Success download {city_code_dict[tmp_city_code]} {tmp_year} year's income data ")
            else:
                print(f"Fail to download {city_code_dict[tmp_city_code]} {tmp_year} year's income data ")


# reader = PyPDF2.PdfReader('sample.pdf')
# print(reader.pages[0].extract_text())


if __name__ == '__main__':
    # url1: data start from 109 year
    test_year = 109
    test_city = 'O'
    url1 = f'https://www.fia.gov.tw/WEB/fia/ias/isa{test_year}s/isa{test_year}/{test_year}_165-{test_city}.pdf'
    response = requests.get(url1)
    # [200] is success
    if response.ok:
        print('Url1 test download is Success')
    else:
        raise BaseException('Url1 test download is failed')
    # url2: data is up to 109
    url2 = f'https://www.fia.gov.tw/WEB/fia/ias/isa{test_year}/isa{test_year}/{test_year}_165-{test_city}.pdf'
    response = requests.get(url2)
    # [200] is success
    if response.ok:
        print('TUrl2 test download is Success')
    else:
        raise BaseException('Url2 test download is failed')

    # download_income_pdf_data_from_gov_web("data/income", 106, ['O'])
    download_income_pdf_data_from_gov_web("data/income", 101, 'all')
