library(dplyr)
library(ggplot2)
library(plotly)

# 讀取資料
all_income_df = read.csv('data/result/income_data.csv',stringsAsFactors = F)%>%
  mutate(year = as.character(year))



# 塞選縣市
sub_income_df = 
  all_income_df %>%
  filter(city  %in% c('新竹市'))

# 留下
# 前1/5收入的裡
n_li = as.integer(length(unique(sub_income_df$village))/5)
# 全部的里
# n_li = as.integer(length(unique(sub_income_df$village)))


# 用最新一年的收入的三分位來比較
max_year = max(sub_income_df$year)
keep_li = sub_income_df %>%
  filter(year == max_year) %>%
  slice_max(三分位,n=n_li) %>%
  distinct(village)
keep_li = keep_li$village
sub_income_df = 
  sub_income_df %>%
  filter(village %in% keep_li ) 


# 畫圖
#ggplot(sub_income_df, aes(x = year , y = 三分位 , color = village,group = village )) +
  #geom_line()
plot_ly(sub_income_df, x = ~year, y = ~三分位, color = ~village, type = 'scatter', mode = 'lines') %>%
  layout(
    title = "Year and 收入第三分位數 趨勢圖",
    xaxis = list(title = "Year"),  # 设置X轴名称
    yaxis = list(title = "收入第三分位數(千)")          # 设置Y轴名称
  )

# 
total_income_df = 
  sub_income_df%>%
  group_by(year )%>%
  summarise(三分位 = mean(三分位)) %>%
  ungroup()

plot_ly(total_income_df, x = ~year, y = ~三分位, type = 'scatter', mode = 'lines') %>%
  layout(
    title = "Year and 收入第三分位數(全里平均) 趨勢圖",
    xaxis = list(title = "Year"),  # 设置X轴名称
    yaxis = list(title = "收入第三分位數(千)")          # 设置Y轴名称
  )


