from abc import ABCMeta
# from typing_extensions import Concatenate
from pandas.core.reshape.concat import concat
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

def run(done,pl,todo):
    import gspread_dataframe as gd
    import gspread as gs
    sh2=gc1.open("test").worksheet('Sheet2')
    done_day1 = gd.get_as_dataframe(sh2)
    up_done=done.append(pl).reset_index(drop=True)
    # up_done
    up_done=up_done.merge(todo,how='left',on='CÔNG VIỆC')
    td=datetime.date.today()
    up_done['NGÀY']=td
    # up_done
    up_done=up_done.replace(np.nan,"Công việc khác")

    up_done=up_done[up_done['CÔNG VIỆC'].isnull()==False]
    
    updated = done_day1.append(up_done)
    # updated=updated.replace("",np.nan)
    # updated['CÔNG VIỆC']=updated['CÔNG VIỆC'].dropna()
    
    gd.set_with_dataframe(sh2, updated)
    done_dayY = gd.get_as_dataframe(sh2)

    done_dayY['NGÀY']=done_dayY['NGÀY'].astype('datetime64')
    done_dayY['NGÀY']=done_dayY['NGÀY'].dt.date
    done_day=done_dayY[done_dayY['NGÀY']==td]
    done_day=done_day[done_day['CÔNG VIỆC'].isnull()==False]
    t1,t2,t3=st.columns(3)
    with t1:
        st.subheader(':trophy:Đệ:trophy:')

        de=done_day[done_day['NV']=='ĐỆ']
        de[['LOẠI CV','CÔNG VIỆC']]
        de.style.set_properties(**{'background-color': 'pink',
                           'color': 'green'})
    with t2:
        st.subheader(':monkey_face:Long:monkey_face:')
        thuan=done_day[done_day['NV']=='LONG'].reset_index(drop=True)
        thuan[['LOẠI CV','CÔNG VIỆC']]
    with t3:
        st.subheader(':panda_face:Trọn:panda_face:')
        Tron=done_day[done_day['NV']=='TRỌN'].reset_index(drop=True)
        Tron[['LOẠI CV','CÔNG VIỆC']]
    r1,r2,r3=st.columns(3)
    with r1:
        st.subheader(':penguin:Linh:penguin:')
        Linh=done_day[done_day['NV']=='LINH'].reset_index(drop=True)
        Linh[['LOẠI CV','CÔNG VIỆC']]

    with r2:
        st.subheader(':heart:Vân:heart:')
        Van=done_day[done_day['NV']=='VÂN'].reset_index(drop=True)
        Van['CÔNG VIỆC']
    with r3:
        st.subheader(':ring:Duy:ring:')
        Duy=done_day[done_day['NV']=='DUY'].reset_index(drop=True)
        Duy[['LOẠI CV','CÔNG VIỆC']]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)
spreadsheet_key = '1XwE7OoVitWw0kIo0N2Ykxh5luZ_xHizLAECwLQJiLfE'
sh1=gc1.open("test").worksheet('Doing')

# df_done=pd.DataFrame(df_)
# if df_done.empty:
sample_name=sh1.get_all_values()
df=pd.DataFrame(sample_name)
df.columns=df.iloc[0]
df=df[1:]
st.title(':star:CÁC VIỆC ĐÃ HOÀN THÀNH HÔM NAY:star:')

with st.form(key='abc'):
    df['CÔNG VIỆC']=df['TÊN SP']+" - "+df['Loại CV']
    staff_list=['ĐỆ','LONG','TRỌN','LINH','VÂN','DUY']
    todo=df[['CÔNG VIỆC','Loại CV']]
    SXM=todo[todo['Loại CV']=='SX MỚI']
    DHM=todo[todo['Loại CV'].str.contains('MẪU')]
    # CNC=todo[todo['Loại CV'].str.contains('CNC')]
    BG=todo[todo['Loại CV'].str.contains('PHIẾU YC')]
    SXNC=todo[todo['Loại CV'].str.contains('SXNC')]
    BB=todo[todo['Loại CV'].str.contains('BAO BÌ')]
    todo_list=df['CÔNG VIỆC'].unique().tolist()

    c1,c2,c3=st.columns((1,3,2))
    with c1:
        name=st.selectbox('Tên của bạn:',staff_list)
    c2,c3,c4,c5,c6=st.columns(5)
    plan_done=[]
    with c2:
        plan_done1=st.multiselect('Sản xuất mới',SXM)
        plan_done11=st.multiselect('Sản xuất như cũ',SXNC)

    with c3:
        plan_done2=st.multiselect('ĐH mẫu',DHM)
        plan_done22=st.multiselect('Quy cách bao bì',BB)
    with c4:
        plan_done3=st.text_area('CNC',)
    with c5:
        plan_done4=st.multiselect('Báo giá',BG)
    with c6:
        out_plan=st.text_area('CÔNG VIỆC khác:',)

    plan_done=plan_done1+plan_done2+plan_done4+plan_done11+plan_done22
    pl=pd.DataFrame(plan_done,columns=['CÔNG VIỆC'])
    cnc=plan_done3.split('\n')
    cnc_done=pd.DataFrame(cnc,columns=['CÔNG VIỆC'])
    cnc_done['NV']=name
    # cnc_done
    pl['NV']=name
    t=out_plan.split('\n')
    done=pd.DataFrame(t,columns=['CÔNG VIỆC'])
    done['NV']=name

    pl=pl.astype(str)
    done_=pd.concat([done,cnc_done]).reset_index(drop=True)
    done_=done_.astype(str)

    st.form_submit_button("Xác nhận")


if st.button('Kết quả tuần này'):

    # st.title('THÀNH QUẢ CỦA HÔM NÀY NÈ!:smile:')
    run(done_,pl,todo)
