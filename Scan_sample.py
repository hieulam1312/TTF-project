from numpy import histogram
from numpy.lib.function_base import append
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import gspread
from google.oauth2 import service_account
import datetime
from gspread_dataframe import set_with_dataframe
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)


today = datetime.date.today()
# today
sh1=gc1.open("PKTH - Theo dõi kho lưu mẫu").worksheet('DS TỔNG')
sample_name=sh1.get_all_records()
sample_name_pd=pd.DataFrame(sample_name)
c1,c2=st.columns((1,1))
with c1:

    step=st.selectbox('Chọn thao tác',['Trả mẫu','Mượn mẫu'])
with c2:
    factory=st.selectbox('Chọn bộ phận',['NM1','NM3','X4','TD','NM NỆM','QLCL','THU MUA','P.TM'])
filter=st.multiselect('Chọn Khách hàng',sample_name_pd['TÊN KHÁCH HÀNG'].unique().tolist())
sample=sample_name_pd[sample_name_pd['TÊN KHÁCH HÀNG'].isin(filter)]

sp=st.multiselect('Chọn sản phẩm',sample['TÊN SẢN PHẨM'].unique())
table=sample[sample['TÊN SẢN PHẨM'].isin(sp)]
table_df=table[['TÊN KHÁCH HÀNG','Tên Mẫu']].reset_index(drop=True)
table_df['NGÀY'],table_df['THAO TÁC'],table_df['BỘ PHẬN']=today,step,factory
table_=table_df[['TÊN KHÁCH HÀNG','Tên Mẫu']]
table_
# sub_folders=order_df[['TÊN KHÁCH HÀNG','TÊN SẢN PHẨM']]
# sub_folders.set_index('TÊN KHÁCH HÀNG').T.to_dict('list')

if st.button('Xuất danh sách'):
# pdf=table_df.to_pd
    dict_id={}
    sheet_index_no1= 8

    spreadsheet_key = '1eWQcw2FFziobQY8rODoYCjfzV3b-_dksTjSDm0Okdpg' # input SPREADSHEET_KEY HERE
    sh = gc1.open_by_key(spreadsheet_key)
    worksheet1 = sh.get_worksheet(sheet_index_no1)#-> 0 - first sheet, 1 - second sheet etc. 

    import gspread_dataframe as gd
    import gspread as gs

    ws = gc1.open("PKTH - Theo dõi kho lưu mẫu").worksheet('Sheet1')
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(table_df)
    gd.set_with_dataframe(ws, updated)
    st.success('Done')


    
# if st.button('Gửi báo cáo'):

#     report()

