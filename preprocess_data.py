import datetime
import os
import re
import zipfile

import PyPDF2
import numpy as np
import pandas as pd

from para import city_code_dict


def preprocess_income_data(income_pdf_data_path, result_path, start_year: int = 101, city_code_filter=[]):
    """
    :param income_pdf_data_path:
    :param result_path:
    :param start_year:
    :param city_code_filter: city code, mapping table can see 'doc/縣市代碼'
    Example
        []: all city
        ['o','j']: 新竹市+新竹縣
    :return: write data to result_path
    """
    print(f"Start Preprocess Income Data")
    # settable parameter
    # house_price_data_path = "data\\house_price_xls\\"
    if not os.path.isdir(result_path):
        os.makedirs(result_path, exist_ok=True)

    year_list = list(str(x) for x in range(start_year, datetime.datetime.today().year - 1910))
    # city_code_filter = ['o']
    # city_code_filter = ['f']

    if not city_code_filter:
        city_code_filter = list(city_code_dict.keys())

    income_dict_list = []
    for tmp_year in year_list:
        print(f"    Start read {tmp_year}")
        for tmp_city_code in city_code_filter:  # tmp_city_code = 'O'
            tmp_city_code = tmp_city_code.upper()
            tmp_pdf_path = f'{income_pdf_data_path}/city-{tmp_city_code}/{tmp_year}_{tmp_city_code}.pdf'

            if not os.path.isfile(tmp_pdf_path):
                print(f"        {tmp_pdf_path}資料並不存在")
                continue
            print(f"        Start read {tmp_pdf_path}")
            all_pdf_page = PyPDF2.PdfReader(tmp_pdf_path).pages

            patterns = r'(.*)\n(.*)'

            for pdf_page in all_pdf_page:  # pdf_page = all_pdf_page[0]
                results = [x[1] for x in re.findall(patterns, pdf_page.extract_text())]
                village_indexes = [index for index in range(len(results)) if
                                   len(results[index]) > 2 and '里' == results[index][2]]
                for village_index in village_indexes:  # village_index = 2
                    tmp_result = str.split(results[village_index])
                    tmp_dict = {'city': city_code_dict[tmp_city_code],
                                'year': tmp_year,
                                'village': tmp_result[0],
                                '納稅單位': tmp_result[8],
                                '綜合所得總額': tmp_result[1],
                                '平均數': tmp_result[2],
                                '中位數': tmp_result[3],
                                '一分位': tmp_result[4],
                                '三分位': tmp_result[5],
                                '標準差': tmp_result[6],
                                '變異係數': tmp_result[7]
                                }
                    income_dict_list.append(tmp_dict)
            print(f"        Complete read {tmp_pdf_path}")
        print(f"    Complete read {tmp_year}")
    summary_df = pd.DataFrame(income_dict_list)
    summary_df.to_csv(result_path + 'income_data.csv', encoding='utf-8-sig', index=False)
    print(f"Success write data to {result_path + 'income_data.csv'}")
    print('')


def preprocess_house_price_data(house_price_data_path, result_path, start_year: int = 101, city_code_filter=[]):
    """

    :param house_price_data_path:
    :param result_path:
    :param start_year:
    :param city_code_filter: city code, mapping table can see 'doc/縣市代碼'
    Example
        []: all city
        ['o','j']: 新竹市+新竹縣
    :return: write data to result_path
    """

    # settable parameter
    # house_price_data_path = "data\\house_price_xls\\"
    if not os.path.isdir(result_path):
        os.makedirs(result_path, exist_ok=True)

    year_list = list(str(x) for x in range(start_year, datetime.datetime.today().year - 1910))
    # city_code_filter = ['o']
    # city_code_filter = ['f']

    # fix parameter
    buy_names = "lvr_land_a.xls"
    presale_names = "lvr_land_b.xls"
    transfer_para = 1.8181 ** 2
    season_list = ['S' + str(i) for i in range(1, 5)]

    existing_house_df_list = []
    presale_df_list = []
    print(f"Start Read House Price Data")
    for year in year_list:
        for season in season_list:
            year_season = f"{year}_{season}"
            # year_season = '112_S3'
            house_price_path_sub = house_price_data_path + year_season

            if os.path.isdir(house_price_path_sub):
                print(f"    載入-{house_price_path_sub} 的資料")
                all_files = os.listdir(house_price_path_sub)
                buy_files = [tmp_file for tmp_file in all_files if buy_names in tmp_file]
                presale_files = [tmp_file for tmp_file in all_files if presale_names in tmp_file]
                if city_code_filter:
                    def filter_fuc(x):
                        return x[0] in city_code_filter

                    buy_files = list(filter(filter_fuc, buy_files))
                    presale_files = list(filter(filter_fuc, presale_files))
                    print(f"    Only read city code: {'; '.join(city_code_filter)}")

                for buy_file in buy_files:
                    # tmp_df = pd.read_csv(f"{house_price_path_sub}\\{buy_file}")
                    tmp_df = pd.read_excel(f"{house_price_path_sub}\\{buy_file}")
                    tmp_df.drop(0, axis=0, inplace=True)  # row 0 is English statement, drop it
                    tmp_df['year_season'] = year_season
                    existing_house_df_list.append(tmp_df)

                for presale_file in presale_files:
                    # tmp_df = pd.read_csv(f"{house_price_path_sub}\\{presale_file}")
                    tmp_df = pd.read_excel(f"{house_price_path_sub}\\{presale_file}")
                    tmp_df.drop(0, axis=0, inplace=True)  # row 0 is English statement, drop it
                    tmp_df['year_season'] = year_season
                    if presale_file == 'b_lvr_land_b.xls' and '110_S3' in house_price_path_sub:
                        tmp_df['棟及號'] = ''  # this data have some special str that column, so skip
                    presale_df_list.append(tmp_df)
            else:
                print(f"    {house_price_path_sub}不存在")
    print(f"Success Read House Price Data")

    print(f"Start Preprocess House Price Data")
    all_existing_house_df = pd.concat(existing_house_df_list, ignore_index=True)
    all_existing_house_df['is_presale'] = False
    # ['鄉鎮市區', '交易標的', '土地位置建物門牌', '土地移轉總面積平方公尺', '都市土地使用分區', '非都市土地使用分區',
    #  '非都市土地使用編定', '交易年月日', '交易筆棟數', '移轉層次', '總樓層數', '建物型態', '主要用途', '主要建材',
    #  '建築完成年月', '建物移轉總面積平方公尺', '建物現況格局-房', '建物現況格局-廳', '建物現況格局-衛',
    #  '建物現況格局-隔間', '有無管理組織', '總價元', '單價元平方公尺', '車位類別', '車位移轉總面積(平方公尺)',
    #  '車位總價元', '備註', '編號', '主建物面積', '附屬建物面積', '陽台面積', '電梯', '移轉編號',
    #  '車位移轉總面積平方公尺']
    all_existing_house_df['車位移轉總面積平方公尺'] = all_existing_house_df.apply(
        lambda tmp_row: tmp_row['車位移轉總面積(平方公尺)'] if pd.isna(tmp_row['車位移轉總面積平方公尺']) else tmp_row[
            '車位移轉總面積平方公尺'], axis=1)

    all_presale_df = pd.concat(presale_df_list, ignore_index=True)
    all_presale_df['is_presale'] = True
    # ['鄉鎮市區', '交易標的', '土地位置建物門牌', '土地移轉總面積平方公尺', '都市土地使用分區', '非都市土地使用分區',
    #  '非都市土地使用編定', '交易年月日', '交易筆棟數', '移轉層次', '總樓層數', '建物型態', '主要用途', '主要建材',
    #  '建築完成年月', '建物移轉總面積平方公尺', '建物現況格局-房', '建物現況格局-廳', '建物現況格局-衛',
    #  '建物現況格局-隔間', '有無管理組織', '總價元', '單價元平方公尺', '車位類別', '車位移轉總面積平方公尺', '車位總價元',
    #  '備註', '編號', '建案名稱', '棟及號', '解約情形']
    # all_presale_df[all_presale_df['建案名稱'] == '恆顧/世界首席']
    # a = all_presale_df[all_presale_df['建案名稱'].apply(lambda x:'恆顧' in str(x))]

    all_buy_df = pd.concat([all_existing_house_df, all_presale_df], ignore_index=True)
    all_buy_df.to_csv(result_path + 'ori_house_data.csv', encoding='utf-8-sig')
    # all_buy_df = pd.read_csv(result_path + 'ori_house_data.csv')

    # area relate
    all_buy_df['total_land_area'] = all_buy_df['土地移轉總面積平方公尺'].apply(lambda x: float(x) / transfer_para)
    all_buy_df['total_house_area'] = all_buy_df['建物移轉總面積平方公尺'].apply(lambda x: float(x) / transfer_para)
    all_buy_df['car_area'] = all_buy_df['車位移轉總面積平方公尺'].apply(lambda x: float(x) / transfer_para)
    all_buy_df['house_main_area'] = all_buy_df['主建物面積'].apply(lambda x: float(x) / transfer_para)
    all_buy_df['house_add_area'] = all_buy_df['附屬建物面積'].apply(lambda x: float(x) / transfer_para)
    all_buy_df['house_balcony_area'] = all_buy_df['陽台面積'].apply(lambda x: float(x) / transfer_para)
    full_width_numbers = {"０": "0", "１": "1", "２": "2", "３": "3", "４": "4", "５": "5", "６": "6", "７": "7", "８": "8",
                          "９": "9", }
    all_full_width = set(full_width_numbers.keys())
    all_buy_df['city'] = all_buy_df['鄉鎮市區']
    all_buy_df['build_case_name'] = all_buy_df['建案名稱']
    all_buy_df['address'] = all_buy_df['土地位置建物門牌'].apply(
        lambda x: ''.join(full_width_numbers[i] if i in all_full_width else i for i in x))
    all_buy_df['address'] = all_buy_df['address'].apply(lambda x: x.replace('', ','))
    all_buy_df['交易標的'] = all_buy_df['交易標的'].apply(str)
    all_buy_df['trading_land'] = all_buy_df['交易標的'].apply(lambda x: '土地' in x)
    all_buy_df['trading_house'] = all_buy_df['交易標的'].apply(lambda x: '建物' in x)
    all_buy_df['trading_car'] = all_buy_df['交易標的'].apply(lambda x: '車位' in x)
    all_buy_df['house_type'] = all_buy_df['建物型態']

    def turn_float(x):
        try:
            return float(x)
        except:
            return np.NaN

    # date relate
    all_buy_df['building_date'] = all_buy_df['建築完成年月'].apply(lambda x: turn_float(x))
    all_buy_df['trading_date'] = all_buy_df['交易年月日']

    # price relate
    all_buy_df['total_price'] = all_buy_df['總價元'].apply(lambda x: float(float(x) / 10000))
    all_buy_df['car_price'] = all_buy_df['車位總價元'].apply(lambda x: float(float(x) / 10000))

    all_buy_df_new = all_buy_df[['total_land_area',
                                 'total_house_area', 'car_area', 'house_main_area', 'house_add_area',
                                 'house_balcony_area', 'city', 'build_case_name', 'address',
                                 'trading_land', 'trading_house', 'trading_car', 'building_date',
                                 'trading_date', 'year_season', 'total_price', 'car_price', 'is_presale', 'house_type']]

    all_buy_df_new.to_csv(result_path + 'house_data.csv', encoding='utf-8-sig', index=False)
    print(f"Success write data to {result_path + 'house_data.csv'}")
    print('')


def unzip_house_price_data(zip_dir_path, target_path):
    # zip_dir_path = "data\\zip_data\\"
    # target_path = "data\\house_price_xls\\"
    print('Start unzip House Price Data')
    if not os.path.isdir(target_path):
        os.makedirs(target_path, exist_ok=True)

    all_zip_files = os.listdir(zip_dir_path)

    for tmp_zip_file in all_zip_files:  # tmp_zip_file = all_zip_files[0]
        print(f'    Start unzip: {tmp_zip_file}')
        path_to_zip_file = zip_dir_path + tmp_zip_file
        directory_to_extract_to = target_path + re.match(r"^(.*)\.zip", tmp_zip_file).group(1)
        try:
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(directory_to_extract_to)
            print(f'    Success unzip : {tmp_zip_file}')
        except zipfile.BadZipFile:
            print(f"unzip '{tmp_zip_file}' fail. It should be latest season,so there is no data ")
    print('Complete unzip House Price Data')
    print('')
