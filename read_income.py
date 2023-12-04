import datetime
import os
import re

import PyPDF2
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
        for tmp_city_code in city_code_filter:  # tmp_city_code = 'O'
            tmp_city_code = tmp_city_code.upper()
            tmp_pdf_path = f'{income_pdf_data_path}/city-{tmp_city_code}/{tmp_year}_{tmp_city_code}.pdf'

            if not os.path.isfile(tmp_pdf_path):
                print(f"{tmp_pdf_path}資料並不存在")
                continue
            print(f"Start read {tmp_pdf_path}")
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
            print(f"Complete read {tmp_pdf_path}")
    summary_df = pd.DataFrame(income_dict_list)
    summary_df.to_csv(result_path + 'income_data.csv', encoding='utf-8-sig', index=False)
    print(f"Success write data to {result_path + 'income_data.csv'}")

# income_data_path = "data/income/city-O"
# if 0:
#     income_dict_list = []
#     for tmp_year in range(101, 111):  # tmp_year = 101
#         pdf_path = f'{income_data_path}/{tmp_year}_O.pdf'
#         all_pdf_page = PyPDF2.PdfReader(pdf_path).pages
#
#         patterns = r'(.*)\n(.*)'
#
#         for pdf_page in all_pdf_page:  # pdf_page = all_pdf_page[0]
#             results = [x[1] for x in re.findall(patterns, pdf_page.extract_text())]
#             village_indexes = [index for index in range(len(results)) if
#                                len(results[index]) > 2 and '里' == results[index][2]]
#             for village_index in village_indexes:  # village_index = 2
#                 tmp_result = str.split(results[village_index])
#                 tmp_dict = {'year': tmp_year,
#                             'village': tmp_result[0],
#                             '納稅單位': tmp_result[8],
#                             '綜合所得總額': tmp_result[1],
#                             '平均數': tmp_result[2],
#                             '中位數': tmp_result[3],
#                             '一分位': tmp_result[4],
#                             '三分位': tmp_result[5],
#                             '標準差': tmp_result[6],
#                             '變異係數': tmp_result[7]
#                             }
#                 income_dict_list.append(tmp_dict)
#
#     summary_df = pd.DataFrame(income_dict_list)
#
#     set(summary_df['village'])
#
#     target_col = ['year', 'village', '納稅單位', '平均數', '中位數', '一分位', '三分位', '標準差', '變異係數']
#
#     see1 = summary_df[summary_df['village'] == '新光里'][target_col]
#     see2 = summary_df[summary_df['village'] == '關東里'][target_col]
#
#     see1 = summary_df[summary_df['village'] == '東勢里'][target_col]
#     # # importing all the required modules
#     #
#     #
#     # # print the number of pages in pdf file
#     # print(len(reader.pages))
#     #
#     # # print the text of the first page
#     # print(reader.pages[0].extract_text())
#     #
#     #
#     #
#     # stri = reader.pages[0].extract_text()
#     # patterns = r'(.*)\n(.*)'
#     # results = [x[1] for x in re.findall(patterns, stri)]
