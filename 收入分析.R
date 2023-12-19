library(dplyr)
library(ggplot2)

# 讀取資料
all_income_df = read.csv('data/result/income_data.csv',stringsAsFactors = F)

# 塞選縣市
sub_income_df = 
  all_income_df %>%
  filter(city  %in% c('新竹市'))

# 畫圖
ggplot(sub_income_df, aes(x = year , y = 三分位 , color = village )) +
  geom_line()

# city is_presale trading_year_quater_plot house_type house_year_stratidied


