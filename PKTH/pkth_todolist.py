from pyasn1_modules.rfc2459 import Name
import streamlit as st
import gspread_dataframe
import numpy as np
from numpy import histogram
from numpy.lib.function_base import append
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import gspread
from google.oauth2 import service_account
import datetime
from gspread_dataframe import set_with_dataframe

st.set_page_config(layout='wide')



credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)
spreadsheet_key = '1XwE7OoVitWw0kIo0N2Ykxh5luZ_xHizLAECwLQJiLfE'
sh1=gc1.open("test").worksheet('Sheet1')

# df_done=pd.DataFrame(df_)
# if df_done.empty:
sample_name=sh1.get_all_values()
df=pd.DataFrame(sample_name)
df.columns=df.iloc[0]
df=df[1:]
df['CÔNG VIỆC']=df['TÊN SẢN PHẨM']+" - "+df['LOẠI CÔNG VIỆC']
staff_list=['Đệ','Thuận','Trọn','Linh','Vân','Duy']
todo_list=df['CÔNG VIỆC'].unique().tolist()
c1,c2,c3=st.columns((1,3,2))
with c1:
    name=st.selectbox('Tên của bạn:',staff_list)
with c2:
    plan_done=st.multiselect(' Chọn công việc đã hoàn thành',todo_list)
    
pl=pd.DataFrame(plan_done,columns=['Công việc'])
pl['NV']=name
t1,t2=st.columns((4,2))
with t1:
    out_plan=st.text_area('Công việc phát sinh:',)
t=out_plan.split('\n')
done=pd.DataFrame(t,columns=['Công việc'])
done['NV']=name
# @st.cache()
def run():
    import gspread_dataframe as gd
    import gspread as gs
    sh2=gc1.open("test").worksheet('Sheet2')
    done_day = gd.get_as_dataframe(sh2)
    up_done=done.append(pl).reset_index(drop=True)
    up_done=up_done.replace("",np.nan)
    up_done=up_done[up_done['Công việc'].isnull()==False]
    updated = done_day.append(up_done)
    gd.set_with_dataframe(sh2, updated)
    done_day = gd.get_as_dataframe(sh2)


    t1,t2,t3=st.columns(3)
    with t1:
        st.subheader('Đệ')

        de=done_day[done_day['NV']=='Đệ']
        de['Công việc']

    with t2:
        st.subheader('Thuận')
        thuan=done_day[done_day['NV']=='Thuận'].reset_index(drop=True)
        thuan['Công việc']
    with t3:
        st.subheader('Trọn')
        Tron=done_day[done_day['NV']=='Trọn'].reset_index(drop=True)
        Tron['Công việc']
    r1,r2,r3=st.columns(3)
    with r1:
        st.subheader('Linh')
        Linh=done_day[done_day['NV']=='Linh'].reset_index(drop=True)
        Linh['Công việc']

    with r2:
        st.subheader('Vân')
        Van=done_day[done_day['NV']=='Vân'].reset_index(drop=True)
        Van['Công việc']
    with r3:
        st.subheader('Duy')
        Duy=done_day[done_day['NV']=='Duy'].reset_index(drop=True)
        Duy['Công việc']


if st.button('Xác nhận'):
    run()




