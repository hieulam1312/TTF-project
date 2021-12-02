import requests #-> Để gọi API
import re #-> Để xử lý data dạng string
from datetime import datetime as dt #-> Để xử lý data dạng datetime
import gspread #-> Để update data lên Google Spreadsheet
from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
import numpy as np
import pandas as pd #-> Để update data dạng bản
import json 
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import os
import matplotlib.image as mpimg
import streamlit as st
from google.oauth2 import service_account
## Collect QR scan database from Googlesheet

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)

spreadsheet_key = '1xNupQa21l9bVVDBJf6Zw2U4J2jy9-k29zH44DGEsAhU' # input SPREADSHEET_KEY HERE
#scan_df
sh1 = gc1.open("TCHC - ĐỀ XUẤT PHOTO").worksheet('FORM')
form=sh1.get_all_records()
form=pd.DataFrame(form)
form.columns=form.columns.str.replace(' ', '_')

#SYNTAX
sh2 = gc1.open("TCHC - ĐỀ XUẤT PHOTO").worksheet('SYNTAX')
syntax=sh2.get_all_records()
syntax=pd.DataFrame(syntax)
syntax.columns=syntax.columns.str.replace(' ', '_')

#BỘ PHẬN
sh3=gc1.open("TCHC - ĐỀ XUẤT PHOTO").worksheet('BỘ PHẬN')
bp=sh3.get_all_records()
bp=pd.DataFrame(bp)
bp.columns=bp.columns.str.replace(' ', '_')

_0_df=form.loc[(form.LOẠI_TÀI_LIỆU=='Đơn hàng nội bộ - ĐHNB')]
table0=_0_df[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','HDV-1','HDV-2','HDV-3','HDV-4','HDV-5']]

_1_df=form.loc[(form.LOẠI_TÀI_LIỆU=='Hướng dẫn vải - HDV')]
table1=_1_df[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','HDV-1','HDV-2','HDV-3','HDV-4','HDV-5']]
# table1.head(20)


_2_df=form.loc[(form.LOẠI_TÀI_LIỆU=='Phiếu chuyển - PC')|(form.LOẠI_TÀI_LIỆU=='Đơn hàng nội địa - ĐHNĐ')]
table2=_2_df[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','Tên_tài_liệu-1','Tên_tài_liệu-2','Tên_tài_liệu-3','Tên_tài_liệu-4','Tên_tài_liệu-5','CHUYỂN_ĐI_ĐÂU-1','CHUYỂN_ĐI_ĐÂU-2','CHUYỂN_ĐI_ĐÂU-3','CHUYỂN_ĐI_ĐÂU-4','CHUYỂN_ĐI_ĐÂU-5']]


_3_df=form.loc[form.LOẠI_TÀI_LIỆU=='TTSP - Handpick']
table3=_3_df[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','TTSP-1','TTSP-2','TTSP-3','TTSP-4','TTSP-5','BV-1','BV-2','BV-3','BV-4','BV-5']]


_4_df=form.loc[(form.LOẠI_TÀI_LIỆU=='Lệnh sản xuất - LSX')]
table4=_4_df[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','MÃ_LSX-1','MÃ_LSX-2','MÃ_LSX-3','MÃ_LSX-4','MÃ_LSX-5','Nhà_Máy_nào-1','Nhà_Máy_nào-2','Nhà_Máy_nào-3','Nhà_Máy_nào-4','Nhà_Máy_nào-5','LSX_BV-1','LSX_BV-2','LSX_BV-3','LSX_BV-4','LSX_BV-5']]


t0_df = table0.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU'], var_name='MÃ_TÀI_LIỆU',
             value_name='Tên_tài_liệu')
table0_df=t0_df.loc[(t0_df['Tên_tài_liệu'].isnull()==False)]
table0_df['BỘ_PHẬN']='PKTH'
table0_df['Số_lượng']=1
table0_drop=table0_df.drop(['MÃ_TÀI_LIỆU'],axis=1)


table0_final=table0_drop.replace("",np.nan)

DHNB=table0_final.loc[table0_final.Tên_tài_liệu.isnull()==False]


t1_df = table1.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU'], var_name='MÃ_TÀI_LIỆU',
             value_name='Tên_tài_liệu')
table1_df=t1_df.loc[(t1_df['Tên_tài_liệu'].isnull()==False)]

table1_df=table1_df.merge(bp,how='left',on='LOẠI_TÀI_LIỆU')

table1_drop=table1_df.drop(['MÃ_TÀI_LIỆU'],axis=1)

table1_final=table1_drop.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','Tên_tài_liệu'], var_name='MÃ_TÀI_LIỆU',
             value_name='BỘ_PHẬN')
table1_final=table1_final.replace("",np.nan)

HDV=table1_final.loc[table1_final.BỘ_PHẬN.isnull()==False]

#convert all columns without separatot to MultiIndex
table2_df= table2.set_index(['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU'])
#split columns by separator
table2_df.columns =table2_df.columns.str.split('-', expand=True)
#reshape by stack
table2_df = table2_df.stack().reset_index().rename(columns={'level_2':'state'})
table2_df[['1','2','3','4','5','6','7','8','9']]=table2_df.CHUYỂN_ĐI_ĐÂU.str.split(", ",expand=True)

table2_drop=table2_df.drop(['CHUYỂN_ĐI_ĐÂU', 'level_3'], axis=1)
table2_final=table2_drop.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','Tên_tài_liệu'], var_name='MÃ_TÀI_LIỆU',
             value_name='BỘ PHẬN')
table2_final.columns=table2_final.columns.str.replace(' ','_')

PC=table2_final.loc[table2_final.BỘ_PHẬN.isnull()==False]
PC['NOTE']=""
PC_=PC.replace('',np.nan)
PC_final=PC_.loc[PC_.Tên_tài_liệu.isnull()==False]



table3_df = table3.set_index(['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU'])
#split columns by separator
table3_df.columns = table3_df.columns.str.split('-', expand=True)

# # #reshape by stack
table3_df =table3_df.stack().reset_index().rename(columns={'level_2':'state'})

table3_df=table3_df.merge(bp,how='left',on='LOẠI_TÀI_LIỆU')
table3_df=table3_df.replace('',np.nan)
table3_df=table3_df.loc[table3_df.TTSP.isnull()==False]
table3_drop=table3_df.drop(['level_3'], axis=1)
# table3_drop
table3_final=table3_drop.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','TTSP','BV'], var_name='MÃ_TÀI_LIỆU',
             value_name='BỘ_PHẬN')
table3_final=table3_final.loc[table3_final.BỘ_PHẬN.isnull()==False]


HDV['NOTE']=""

HDV_=HDV.merge(syntax,how='left',left_on=["BỘ_PHẬN",'LOẠI_TÀI_LIỆU'],right_on=["Bộ_phận",'Tên_tài_liệu'])
HDV_=HDV_.drop(['MÃ_TÀI_LIỆU','Bộ_phận','Tên_tài_liệu_y','Ghi_chú'],axis=1)
HDV_=HDV_.loc[(HDV_.Số_lượng.isnull()==False)& (HDV_.Tên_tài_liệu_x.isnull()==False)]
HDV_=HDV_.rename(columns={'Tên_tài_liệu_x':'Tên_tài_liệu'})


PC_=PC_final.merge(syntax,how='left',left_on=["BỘ_PHẬN"],right_on=["Bộ_phận"])
PC_1=PC_[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','Tên_tài_liệu_y','Tên_tài_liệu_x','BỘ_PHẬN','NOTE','Số_lượng']]
PC_1=PC_1.rename(columns={'Tên_tài_liệu_y':'LOẠI_TÀI_LIỆU','Tên_tài_liệu_x':'Tên_tài_liệu'})
PC_2=PC_1.replace('',np.nan) 
PC2=PC_2.loc[(PC_2.Tên_tài_liệu.isnull()==False) & (PC_2['LOẠI_TÀI_LIỆU'].str.contains('ĐHNĐ')) + (PC_2['LOẠI_TÀI_LIỆU'].str.contains('PC'))]
# PC_=PC_.drop(['Tên_tài_liệu_y','Bộ_phận','Ghi_chú','MÃ_TÀI_LIỆU'],axis=1)


TTSP_HP=table3_final.rename(columns={'TTSP': 'Tên_tài_liệu','BV':'NOTE' })



TTSP_HP1=TTSP_HP.merge(syntax,how='left',left_on=["BỘ_PHẬN"],right_on=["Bộ_phận"])
TTSP_HP_=TTSP_HP1[['Dấu_thời_gian','MÃ_PHIẾU_ĐỀ_XUẤT','Tên_tài_liệu_x','NOTE','BỘ_PHẬN','Tên_tài_liệu_y','Số_lượng']]
# TTSP_HP_=TTSP_HP_.rename(columns={'Tên_tài_liệu_x':'Tên_tài_liệu'})
TTSP_HP_=TTSP_HP_[TTSP_HP_['Tên_tài_liệu_y'].isnull()==False]
# TTSP_HP_
TTSP_HP_1=TTSP_HP_.loc[(TTSP_HP_['Tên_tài_liệu_y'].str.contains('TTSP - Handpick'))]
TTSP_HP_final=TTSP_HP_1.rename(columns={'Tên_tài_liệu_y':'LOẠI_TÀI_LIỆU','Tên_tài_liệu_x':'Tên_tài_liệu'})




table4_df=table4.set_index(['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU'])

# #split columns by separator
table4_df.columns =table4_df.columns.str.split('-', expand=True)

# #reshape by stack
table4_df = table4_df.stack().reset_index().rename(columns={'Tên_tài_liệu':'Nhà_máy'})
table4_df=table4_df.rename(columns={'MÃ_LSX': 'Tên_tài_liệu','LSX_BV':'NOTE','Nhà_Máy_nào':'0'})
table4_df.tail(20)
table4_df=table4_df.merge(bp,how='left',on='LOẠI_TÀI_LIỆU')
# table4_df.tail(20)

table4_drop=table4_df.drop(['level_3'], axis=1)
# table4_df.tail(20)

table4_final=table4_drop.melt(id_vars=['Dấu_thời_gian', 'MÃ_PHIẾU_ĐỀ_XUẤT','LOẠI_TÀI_LIỆU','Tên_tài_liệu','NOTE'], var_name='MÃ_TÀI_LIỆU',
             value_name='BỘ_PHẬN')
# 
table4_final=table4_final.merge(syntax,how='inner',left_on=["LOẠI_TÀI_LIỆU","BỘ_PHẬN"],right_on=["Tên_tài_liệu","Bộ_phận"])
# table4_final
table4_final1=table4_final.drop(['MÃ_TÀI_LIỆU','Bộ_phận','Tên_tài_liệu_y','Ghi_chú'],axis=1)
LSX=table4_final1.rename(columns={'Tên_tài_liệu_x':'Tên_tài_liệu'})
LSX=LSX.replace('',np.nan)
LSX_final=LSX.loc[LSX.Tên_tài_liệu.isnull()==False]



final=pd.concat([HDV_,DHNB,PC2,LSX_final,TTSP_HP_final])



# ## notice:
table1_final1=pd.concat([HDV_,DHNB])
table1_final1['Dấu_thời_gian']=pd.to_datetime(table1_final1.Dấu_thời_gian)

table1_final1=table1_final1.sort_values('Dấu_thời_gian')

hdv1=table1_final1['Dấu_thời_gian']
hdv2=table1_final1['Tên_tài_liệu']
hdv=pd.DataFrame({'Time':hdv1,'Tên':hdv2})
hdv=hdv.replace('', np.nan)
hdv_final=hdv.loc[hdv.Tên.isnull()==False]
hdv_final=hdv_final.drop_duplicates()
hdv_final.sort_values(by=['Time'])
hdv_final.tail(30)
st.info('hallu Nga!')
st.info("Đợi một chút để tải file nà")

# # table2_final: PC, ĐHNĐ
table2_final1=PC_final
table2_final1['Dấu_thời_gian']=pd.to_datetime(table2_final1.Dấu_thời_gian)

table2_final1=table2_final1.sort_values('Dấu_thời_gian')

pc1=table2_final1['Dấu_thời_gian']
pc2=table2_final1['Tên_tài_liệu']
pc=pd.DataFrame({'Time':pc1,'Tên':pc2})
pc=pc.replace('', np.nan)

pc_final=pc.loc[pc.Tên.isnull()==False]
pc_final=pc_final.drop_duplicates()
pc_final.sort_values(by=['Time'])


# # # table3_final: TTSP HP
table3_final1=TTSP_HP_final
table3_final1['Dấu_thời_gian']=pd.to_datetime(table3_final1.Dấu_thời_gian)

table3_final1=table3_final1.sort_values('Dấu_thời_gian')

hp1=table3_final1['Dấu_thời_gian']
hp2=table3_final1['Tên_tài_liệu']
hp=pd.DataFrame({'Time':hp1,'Tên':hp2})
hp=hp.replace('', np.nan)
hp=hp.drop_duplicates()
hp_final=hp.loc[hp.Tên.isnull()==False]
hp_final.sort_values(by=['Time'])


# #LSX
table4_final1=LSX
table4_final1['Dấu_thời_gian']=pd.to_datetime(table4_final1.Dấu_thời_gian)

table4_final1=table4_final1.sort_values('Dấu_thời_gian')

lsx1=table4_final1['Dấu_thời_gian']

lsx2=table4_final1['Tên_tài_liệu']
lsx=pd.DataFrame({'Time':lsx1,'Tên':lsx2})
lsx=lsx.replace('', np.nan)
lsx_final=lsx.loc[lsx.Tên.isnull()==False]

lsx_final=lsx_final.drop_duplicates()
# lsx_final
lsx_final.sort_values(by='Time')





# ACCES GOOGLE SHEET
sheet_index_no1 = 0
sheet_index_no2 = 1
sheet_index_no3 = 2
sheet_index_no4 = 3
sheet_index_no5 = 4
spreadsheet_key = '13P--4fYhCsFXUZLUnr1vHUHZYQ6RohL7jcFVOJWDYz4' # input SPREADSHEET_KEY HERE
sh = gc1.open_by_key(spreadsheet_key)
worksheet1 = sh.get_worksheet(sheet_index_no1)#-> 0 - first sheet, 1 - second sheet etc. 
worksheet2 = sh.get_worksheet(sheet_index_no2)
worksheet3 = sh.get_worksheet(sheet_index_no3)
worksheet4 = sh.get_worksheet(sheet_index_no4)
worksheet5 = sh.get_worksheet(sheet_index_no5)
# APPEND DATA TO SHEET
set_with_dataframe(worksheet1, final) #-> Upload user_df vào Sheet đầu tiên trong Spreadsheet
st.balloons()

set_with_dataframe(worksheet2,hdv_final) 
set_with_dataframe(worksheet3,pc_final)
set_with_dataframe(worksheet4,hp_final)
set_with_dataframe(worksheet5,lsx_final)
st.success('Xong rồi nà')
# # DONE: Bây giờ bạn có thể mở spreadsheet và kiểm tra nội dung đã update chứ
