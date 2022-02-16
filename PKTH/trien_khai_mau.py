# Import Library
from tkinter.tix import COLUMN
from types import new_class
import requests #-> Để gọi API
import re #-> Để xử lý data dạng string
from datetime import datetime as dt #-> Để xử lý data dạng datetime
import time
import gspread #-> Để update data lên Google Spreadsheet
import numpy as np
import pandas as pd #-> Để update data dạng bản
import json 
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import os
import streamlit as st
from google.oauth2 import service_account
## Collect QR scan database from Googlesheet


from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit as st

credentials=service_account.Credentials.from_service_account_info(
    st.secrets['gcp_service_account'],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)


#scan_df
# sh1 = gc1.open("MẪU 2022 - COLLECT DATA").worksheet('UNPIVOT')
# scan_df=sh1.get_all_records()
# scan_df=pd.DataFrame(scan_df)
# #td_df
sh2=gc1.open("MẪU 2022 - COLLECT DATA").worksheet('TD')
td_df=sh2.get_all_records()
td_df=pd.DataFrame(td_df)
#td_x4_df
sh3=gc1.open("MẪU 2022 - COLLECT DATA").worksheet('TD X4-NỆM')
td_x4_df=sh3.get_all_records()
td_x4_df=pd.DataFrame(td_x4_df)
sh6=gc1.open("MẪU 2022 - COLLECT DATA").worksheet('XL+ SL')
xl_sl=sh6.get_all_records()
xl_sl_df=pd.DataFrame(xl_sl)
#order_df
sh4=gc1.open('TTF - MẪU 2022 - TRIỂN KHAI').worksheet('D.SÁCH')
order_df=sh4.get_all_records()
order_df=pd.DataFrame(order_df)

# sh5=gc2.open('TTF - MẪU 2022 - TRIỂN KHAI').worksheet('T.DÕI')
# td_old=sh5.get_all_records()
# td_old_df=pd.DataFrame(td_old)

sh7=gc1.open('TTF - MẪU 2022 - DƯỚI 12').worksheet('D.SÁCH')
under_12ds=sh7.get_all_records()
under_12ds_df=pd.DataFrame(under_12ds)
sh8=gc1.open('TTF - MẪU 2022 - DƯỚI 12').worksheet('T.DÕI')
under_12td=sh8.get_all_records()
under_12td_df=pd.DataFrame(under_12td)

sh8=gc1.open('TTF - MẪU 2022 - TRIỂN KHAI').worksheet('Sheet53')
dataaa=sh8.get_all_records()
data=pd.DataFrame(dataaa)
nm_df=td_df.loc[(td_df['NHÀ MÁY']!='X4')&(td_df['NHÀ MÁY']!='NM NỆM')]
td_new_df=pd.concat([nm_df,td_x4_df])
td_new_df=td_new_df[['SỐ ĐƠN HÀNG','BƯỚC','IN','OT','NHÀ MÁY','NMVLM','BỘ PHẬN','NGÀY GIẢI QUYẾT','NHÓM MẪU']]
td_new_df=td_new_df.rename(columns={'IN': 'NGÀY NHẬN','OT':'NGÀY GIAO','NMVLM':'NVLM'})

# td_old_df.columns=td_old_df.columns.str.replace(" ","_")
td_all_df=pd.concat([td_new_df,under_12td_df])
td_all_df=td_all_df.replace('',np.nan)
td_2022_df=td_all_df[td_all_df['SỐ ĐƠN HÀNG'].notnull()]
# under_12ds_df=under_12ds_df.rename(columns={'NV LÀM MẪU':'NVLM'})
under_12ds_df=under_12ds_df.drop(['BƯỚC'],axis=1)
nvlm=td_all_df[['SỐ ĐƠN HÀNG','NVLM']]
nvlm_df=nvlm.drop_duplicates()
nvlm_df=nvlm_df.dropna()

# xl_sl_df.columns=xl_sl_df.columns.str.replace(' ','_')
xl=xl_sl_df.loc[xl_sl_df['THAO TÁC']==' Giao đơn hàng']
xl_df=xl[['SỐ ĐH','XẾP LOẠI','SL THỰC TẾ']]
xl_df=xl_df.rename(columns={'SỐ ĐH':'SỐ ĐƠN HÀNG'})

under_12ds_df=under_12ds_df.drop(['NV LÀM MẪU'],axis=1)
order_df=order_df.drop(['BAO BÌ','GHI CHÚ','HÌNH ẢNH'], axis = 1)
# order_df
new_order=order_df.merge(xl_df,how='left',on='SỐ ĐƠN HÀNG')
order_2022_df=pd.concat([new_order,under_12ds_df])
order_new=order_2022_df .merge(nvlm_df,how='left',on='SỐ ĐƠN HÀNG')
order_new=order_new.replace(np.nan,0)

# pd.to_datetime(order_new['NGÀY GIAO'],dayfirst=True,errors='coerce')
# order_new['NGÀY GIAO']=pd.to_datetime(order_new['NGÀY GIAO'],dayfirst=True,errors='coerce')
# order_new['NGÀY LẬP']=pd.to_datetime(order_new['NGÀY LẬP'],dayfirst=True,errors='coerce')
# td_2022_df['NGÀY NHẬN']=pd.to_datetime(td_2022_df['NGÀY NHẬN'],dayfirst=True,errors='coerce')
# td_2022_df['NGÀY GIAO']=pd.to_datetime(td_2022_df['NGÀY GIAO'],dayfirst=True,errors='coerce')

order_df=order_new[['SỐ ĐƠN HÀNG','TÊN KHÁCH HÀNG','TÊN SẢN PHẨM','S/L','NHÀ MÁY','TÌNH TRẠNG','NV PTM','GỖ']]
# data=pd.read_excel(r'D:\OneDrive\DATACracy\TTF project\TĐ MẪU.xlsx',sheet_name='Sheet1')
order_df=order_df.astype(str)
data['NGÀY']=data['NGÀY'].astype(str).str[:10]
list_order=order_df['SỐ ĐƠN HÀNG'].unique().tolist()
HT_df=data.loc[data['BỘ PHẬN']=='Hàng trắng']
KL_df=data.loc[data['BỘ PHẬN']=='Kim loại']
VE_df=data.loc[data['BỘ PHẬN']=='Ván ép']
order_key=list_order.copy()

_list={}
early_list={}
for i in order_key:
    _list[i]={}
    _list[i]['Hàng trắng']=HT_df.loc[HT_df['SỐ ĐƠN HÀNG']==i]['NGÀY'].to_list()
    _list[i]['Kim loại']=KL_df.loc[KL_df['SỐ ĐƠN HÀNG']==i]['NGÀY'].to_list()
    _list[i]['Ván ép']=VE_df.loc[VE_df['SỐ ĐƠN HÀNG']==i]['NGÀY'].to_list()
dataa=pd.DataFrame.from_dict(_list, orient='index').reset_index()

td_df=td_df.replace("",np.nan)
td_=td_df[td_df['SỐ ĐƠN HÀNG'].notnull()]
td_tm=td_.loc[td_['LOẠI THU MUA'].notnull()]

new_list={k:{sk:sv[-1] for sk,sv in s.items() if len(sv)>0} for k,s in _list.items() }
new_list_df=pd.DataFrame.from_dict(new_list, orient='index').reset_index()

# st.write('helo Linh')
user=st.sidebar.text_input('User name')
pw=st.sidebar.text_input('Password',type='password')
check=st.sidebar.checkbox('Login')
td_=td_2022_df.replace("",np.nan)
td_sd=td_.merge(order_df,how='left',on='SỐ ĐƠN HÀNG')

td_sd=td_sd[['SỐ ĐƠN HÀNG','BƯỚC','TÊN KHÁCH HÀNG','TÊN SẢN PHẨM','NV PTM_x','NHÀ MÁY_x','NVLM','TÌNH TRẠNG','BỘ PHẬN','NGÀY NHẬN','NGÀY GIAO','NGÀY GIẢI QUYẾT','NHÓM MẪU']]
td_sd_=td_sd.rename(columns={'TÊN KHÁCH HÀNG_x':'TÊN KHÁCH HÀNG','TÊN SẢN PHẨM_x':'TÊN SẢN PHẨM','NV PTM_x':'NV PTM','NHÀ MÁY_x':'NHÀ MÁY','NVLM_x':'NVLM','TÌNH TRẠNG_y':'TÌNH TRẠNG','NGÀY GIAO_x':'NGÀY GIAO'})
td__=td_sd_.loc[td_sd_['NHÓM MẪU'].isnull()==False]
td__['NGÀY NHẬN']=pd.to_datetime(td__['NGÀY NHẬN'])
td__['NGÀY GIAO']=pd.to_datetime(td__['NGÀY GIAO'])
td_2022_df=td__
td_2021_=td_2022_df.loc[td_2022_df['TÌNH TRẠNG']=='Đang triển khai']

doing_=td_2022_df.copy()
doing_df=doing_.loc[(doing_['NGÀY NHẬN'].isnull()==False) &
         (doing_['NGÀY GIAO'].isnull()==True)&(doing_['NGÀY NHẬN'].shift(-1).isnull()==True)]
doing_df['TÌNH_TRẠNG']='Đang xử lí'
doing_df.columns=doing_df.columns.str.replace(" ","_")

# Lọc danh sách nhóm mẫu để phân loại theo định nghĩa sau:
# A: Mẫu làm mới, không có thu mua [1,2,3,7,8,9,10,11]
# B: Mẫu làm mới, có thu mua [1,2,3,5,6,7,8,9,10,11]
# C: Mẫu cũ, nhưng làm thêm [1,2,3,7,8,9,10,11]
# D: Mẫu cũ, lấy khung tồn [1,2,3,10,11]

A_td=td_2021_.loc[(td_2021_['NHÓM MẪU']=='A')]

A_=A_td.loc[(A_td['BƯỚC']!=4.0) & (A_td['BƯỚC']!=5.0) &(A_td['BƯỚC']!=6.0)]
A_=A_.replace('NaT',np.nan)
A_.columns=A_.columns.str.replace(" ","_")

A_chưa_nhận=A_.loc[(A_['NGÀY_NHẬN'].isnull()==True) &
         (A_['NGÀY_GIAO'].shift(1).isnull()==False)]
A_chưa_nhận['TÌNH_TRẠNG']='Chưa nhận'
A_chưa_giao= A_.loc[(A_['NGÀY_GIAO'].isnull()==True) &
         (A_['NGÀY_NHẬN'].shift(-1).isnull()==False)]
A_chưa_giao['TÌNH_TRẠNG']='Chưa giao'
B1_td=td_2021_.loc[(td_2021_['NHÓM MẪU']=='B1')]

B1_=B1_td.loc[(B1_td['BƯỚC']!=4.0)&(B1_td['BƯỚC']!=5.0)]
B1_=B1_.replace('NaT',np.nan)
B1_.columns=B1_.columns.str.replace(" ","_")

B1_chưa_nhận=B1_.loc[(B1_['NGÀY_NHẬN'].isnull()==True) &
         (B1_['NGÀY_GIAO'].shift(1).isnull()==False)]
B1_chưa_nhận['TÌNH_TRẠNG']='Chưa nhận'

B1_chưa_giao= B1_.loc[(B1_['NGÀY_GIAO'].isnull()==True) &
         (B1_['NGÀY_NHẬN'].shift(-1).isnull()==False)]
B1_chưa_giao['TÌNH_TRẠNG']='Chưa giao'
B2_td=td_2021_.loc[(td_2021_['NHÓM MẪU']=='B2')]

B2_=B2_td.loc[(B2_td['BƯỚC']!=4.0)&(B2_td['BƯỚC']!=6.0)]
B2_=B2_.replace('NaT',np.nan)
B2_.columns=B2_.columns.str.replace(" ","_")

B2_chưa_nhận=B2_.loc[(B2_['NGÀY_NHẬN'].isnull()==True) &
         (B2_['NGÀY_GIAO'].shift(1).isnull()==False)]
B2_chưa_nhận['TÌNH_TRẠNG']='Chưa nhận'

B2_chưa_giao= B2_.loc[(B2_['NGÀY_GIAO'].isnull()==True) &
         (B2_['NGÀY_NHẬN'].shift(-1).isnull()==False)]
B2_chưa_giao['TÌNH_TRẠNG']='Chưa giao'
C_td=td_2021_.loc[(td_2021_['NHÓM MẪU']=='C')]

C_=C_td.loc[(C_td['BƯỚC']!=4.0) & (C_td['BƯỚC']!=5.0) &(C_td['BƯỚC']!=6.0)]
C_=C_.replace('NaT',np.nan)
C_.columns=C_.columns.str.replace(" ","_")

C_chưa_nhận=C_.loc[(C_['NGÀY_NHẬN'].isnull()==True) &
         (C_['NGÀY_GIAO'].shift(1).isnull()==False)]
C_chưa_nhận['TÌNH_TRẠNG']='Chưa nhận'

C_chưa_giao= C_.loc[(C_['NGÀY_GIAO'].isnull()==True) &
         (C_['NGÀY_NHẬN'].shift(-1).isnull()==False)]
C_chưa_giao['TÌNH_TRẠNG']='Chưa giao'

D_td=td_2021_.loc[(td_2021_['NHÓM MẪU']=='C')]
#1,2,3,10,11
D_=D_td.loc[(C_td['BƯỚC']!=4.0) & (D_td['BƯỚC']!=5.0) &(D_td['BƯỚC']!=6.0) &(D_td['BƯỚC']!=7.0) &(D_td['BƯỚC']!=8.0) &(D_td['BƯỚC']!=9.0)]
D_=D_.replace('NaT',np.nan)
D_.columns=D_.columns.str.replace(" ","_")

D_chưa_nhận=D_.loc[(D_['NGÀY_NHẬN'].isnull()==True) &
         (D_['NGÀY_GIAO'].shift(1).isnull()==False)]
D_chưa_nhận['TÌNH_TRẠNG']='Chưa nhận'

D_chưa_giao= D_.loc[(D_['NGÀY_GIAO'].isnull()==True) &
         (D_['NGÀY_NHẬN'].shift(-1).isnull()==False)]
D_chưa_giao['TÌNH_TRẠNG']='Chưa giao'

all_error=pd.concat([D_chưa_nhận,D_chưa_giao,C_chưa_nhận,C_chưa_giao,B1_chưa_nhận,B2_chưa_giao,B2_chưa_nhận,B1_chưa_giao,A_chưa_nhận,A_chưa_giao])
all_error=all_error[all_error['BƯỚC']<12]






calc=td_new_df[['SỐ ĐƠN HÀNG',"BƯỚC",'BỘ PHẬN','NGÀY NHẬN','NGÀY GIAO']].loc[td_new_df['BƯỚC'].isin([1,3,7,8,10,11])]
A=calc.melt(id_vars=["SỐ ĐƠN HÀNG","BƯỚC",'BỘ PHẬN'],value_vars=['NGÀY NHẬN','NGÀY GIAO'],var_name='THAO TÁC',value_name='NGÀY')
b=A[(A['THAO TÁC']=="NGÀY NHẬN")&(A['BƯỚC'].isin([1,7,8,11]))| (A['THAO TÁC']=="NGÀY GIAO")& (A['BƯỚC'].isin([3,10]))].reset_index(drop=True)
b=b[b['SỐ ĐƠN HÀNG']!=""]
c=b.pivot(index=["SỐ ĐƠN HÀNG"],columns='BỘ PHẬN',values='NGÀY').reset_index().merge(order_new,how='left',on='SỐ ĐƠN HÀNG')

# c






def to_excel(df1,df2):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    new_list_df.to_excel(writer, sheet_name='KH',index=False)
    order_df.to_excel(writer, sheet_name='DS',index=False)
    td_2022_df.to_excel(writer, sheet_name='TD',index=False)
    dataa.to_excel(writer, sheet_name='dataa',index=False)
    td_tm.to_excel(writer, sheet_name='td_tm',index=False)
    c.to_excel(writer,sheet_name='calc',index=False)
    workbook = writer.book
    # worksheet = writer.sheets['Sheet1','Sheet2']
    writer.save()
    processed_data = output.getvalue()
    return processed_data
if not check:
    st.info('Nhập tên đăng nhập và mật khẩu')

elif user==st.secrets['user'] and pw==st.secrets['password']:
    st.header('Cập nhật tiến độ mẫu năm 2022')
    order_df
    df_xlsx = to_excel(new_list_df,dataa)
    st.download_button(label='📥 Tải DS họp mẫu',
                                data=df_xlsx ,
                                file_name= 'Mau2022.xlsx')

    st.header('Danh sách ĐHM scan thiếu/sai')
    all_error
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    all_error.to_excel(writer, sheet_name='error',index=False)
    workbook = writer.book
    # worksheet = writer.sheets['Sheet1','Sheet2']
    writer.save()
    processed_data = output.getvalue()

    st.download_button(label='📥 Tải DS ĐHM scan thiếu sai',
                                data=processed_data,
                                file_name= 'Mau2022.xlsx')
