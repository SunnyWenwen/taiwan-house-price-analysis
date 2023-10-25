import re
import zipfile
import os

zip_dir_path = "data\\zip_data\\"
target_path = "data\\house_price_csv\\"

if not os.path.isdir(target_path):
    os.makedirs(target_path, exist_ok=True)


all_zip_files = os.listdir(zip_dir_path)

for tmp_zip_file in all_zip_files:  # tmp_zip_file = all_zip_files[0]
    print(f'Start unzip: {tmp_zip_file}')
    path_to_zip_file = zip_dir_path + tmp_zip_file
    directory_to_extract_to = target_path + re.match(r"^(.*)\.zip", tmp_zip_file).group(1)

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
