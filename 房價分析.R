library(dplyr)
library(stringr)
library(skimr)
library(ggplot2)
library(lubridate)
library(plotly)


# 讀取資料
all_buy_df = read.csv('data/result/house_data.csv',stringsAsFactors = F)

# 基本資料探勘
unique(all_buy_df$build_case_name)
unique(all_buy_df$city)
table(all_buy_df$is_presale)
table(all_buy_df$house_type)
skim(all_buy_df) # presale no house_main_area/house_add_area/house_balcony_area/building_date


# 哪種房屋形態要留下來
house_type_target_filter = c('公寓(5樓含以下無電梯)','住宅大樓(11層含以上有電梯)','華廈(10層含以下有電梯)','透天厝','套房(1房1廳1衛)')
# house_type_target_filter = c('公寓(5樓含以下無電梯)','住宅大樓(11層含以上有電梯)','華廈(10層含以下有電梯)')

# 要留下的縣市
city_filter = c("竹北市","寶山鄉","芎林鄉","新竹市","竹東鎮","頭份市","竹南鎮","新埔鎮")

# 幾年以內的房子
house_year_upper_bound = 15

# 整理資料
sub_df = 
  all_buy_df%>%
  filter(city %in% city_filter)%>%
  mutate_at(c('total_price','total_land_area','total_house_area','car_price'),as.numeric) %>%
  mutate(house_year = ifelse(is_presale,0,ceiling((trading_date-building_date)/10000)))%>% # 買賣時屋齡，不足一年以一年計算
  filter(300<total_price & total_price<4000) %>% # 房價塞選
  filter(trading_land == 'True' & trading_house == 'True') %>% # 有地+房才留下
  filter(total_land_area<50 & total_land_area>1) %>% # 土地面積太大太小不留下
  filter(total_house_area<100 & total_house_area>5) %>% # 房子面積太大太小不留下
  filter(house_year<house_year_upper_bound) %>%
  # filter(building_date>800000 | build_case_name!='' ) %>% #留下40年內的房子 or 預售屋
  filter(trading_date>1050000) %>%
  filter(house_type %in% house_type_target_filter) %>%
  # filter(house_main_area<100 & house_main_area>5) %>%
  mutate(car_area = ifelse(is.na(car_area),0,car_area)) %>%
  mutate(house_price_per_area = (total_price-car_price)/(total_house_area-car_area)) %>%
  filter(house_price_per_area<150) %>%
  mutate(house_year_stratidied = as.character( ceiling(house_year/5)  ))%>%
  mutate(trading_year = as.integer( trading_date/10000))%>%
  mutate(trading_month = as.integer( trading_date/100)%%100)%>%
  mutate(trading_quater = as.integer((trading_month+2)/3)) %>%
  mutate(trading_year_quater = paste0(trading_year,' Q',trading_quater)) %>%
  mutate(trading_year_quater_plot = trading_year+(trading_quater-1)/4 ) 
  
  #arrange(house_price_per_area)

# unique(sub_df$trading_year_quater_plot )

# 決定by甚麼維度Summarize data
plot_data = 
  sub_df %>%
  group_by(city,trading_year_quater) %>%
  # group_by(city,house_type,trading_year_quater_plot) %>%
  # group_by(city,is_presale,trading_year_quater_plot) %>%
  # group_by(city,is_presale,house_type,trading_year_quater_plot) %>%
  summarise(m_price = quantile(house_price_per_area,0.75),ct = n()) %>%
  print(n=1000) 


# 畫價格趨勢圖
# ggplot(plot_data, aes(x = trading_year_quater, y = m_price, color = city)) +
# geom_line()
plot_ly(plot_data, x = ~trading_year_quater, y = ~m_price, color = ~city, type = 'scatter', mode = 'lines') %>%
  layout(
    title = "Year and Quarter 每坪價格趨勢圖",
    xaxis = list(title = "Year-Quarter"),  # 设置X轴名称
    yaxis = list(title = "每坪價格(萬)")          # 设置Y轴名称
  )

# 畫成交量趨勢圖
ggplot(plot_data, aes(x = trading_year_quater_plot, y = ct, color = city)) +
  geom_line()

plot_ly(plot_data, x = ~trading_year_quater, y = ~ct, color = ~city, type = 'scatter', mode = 'lines')%>%
  layout(
    title = "Year and Quarter 交易量 趨勢圖",
    xaxis = list(title = "Year-Quarter"),  # 设置X轴名称
    yaxis = list(title = "交易量")          # 设置Y轴名称
  )

# city is_presale trading_year_quater_plot house_type house_year_stratidied


#################################以下不重要#####################

ggplot(sub_df, aes(x = city, y = house_price_per_area)) +
  geom_boxplot() +
  labs(title = "資料分布")


sub_df %>%
  group_by(city,is_presale,house_type,trading_year_quater_plot) %>%
  summarise(mean(house_price_per_area),ct = n()) %>%
  print(n=1000) 

plot_data = 
  sub_df %>%
  group_by(house_year_stratidied,trading_year_quater_plot)%>%
  summarise(m_price = mean(house_price_per_area),ct = n()) %>%
  print(n=1000)

sub_df %>%
  group_by(trading_year,trading_quater)%>%
  summarise(mean(house_price_per_area),ct = n()) %>%
  print(n=1000)


sub_df %>%
  group_by(trading_year)%>%
  summarise(mean(house_price_per_area)) %>%
  print(n=1000)


# 所得
# 塞選老屋
# 改中文
# 流英文
# 抽出路名、地區 要注意段
# 

sub_df$建築完成年月

sub_df$建案名稱
unique(sub_df$建案名稱)

skim(sub_df)
hist(sub_df$house_main_area)
hist(sub_df$house_price_per_area)
see = sub_df[which.max(sub_df$house_price_per_area),]

sort(sub_df$house_price_per_area,decreasing  = T)
###
see = all_buy_df[all_buy_df$交易年月日==1100419,]
skim(sub_df)

