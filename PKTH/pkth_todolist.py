from abc import ABCMeta
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
sh1=gc1.open("test").worksheet('Sheet3')

# df_done=pd.DataFrame(df_)
# if df_done.empty:
sample_name=sh1.get_all_values()
df=pd.DataFrame(sample_name)
df.columns=df.iloc[0]
df=df[1:]

def data(df):
    df['CÔNG VIỆC']=df['TÊN SẢN PHẨM']+" - "+df['LOẠI CÔNG VIỆC']
    staff_list=['Đệ','Thuận','Trọn','Linh','Vân','Duy']
    todo=df[['CÔNG VIỆC','LOẠI CÔNG VIỆC']]
    SXM=todo[todo['LOẠI CÔNG VIỆC']=='SX MỚI']
    DHM=todo[todo['LOẠI CÔNG VIỆC'].str.contains('MẪU')]
    CNC=todo[todo['LOẠI CÔNG VIỆC'].str.contains('CNC')]
    BG=todo[todo['LOẠI CÔNG VIỆC'].str.contains('PHIẾU YC')]
    todo_list=df['CÔNG VIỆC'].unique().tolist()

    c1,c2,c3=st.columns((1,3,2))
    with c1:
        name=st.selectbox('Tên của bạn:',staff_list)
    c2,c3,c4,c5,c6=st.columns(5)
    plan_done=[]
    with c2:
        plan_done1=st.multiselect('Sản xuất mới',SXM)

    with c3:
        plan_done2=st.multiselect('ĐH mẫu',DHM)
    with c4:
        plan_done3=st.multiselect('CNC',CNC)
    with c5:
        plan_done4=st.multiselect('Báo giá',BG)
    with c6:
        out_plan=st.text_area('CÔNG VIỆC khác:',)
    plan_done=plan_done1+plan_done2+plan_done3+plan_done4
    pl=pd.DataFrame(plan_done,columns=['CÔNG VIỆC'])
    pl['NV']=name
    t=out_plan.split('\n')
    done=pd.DataFrame(t,columns=['CÔNG VIỆC'])
    done['NV']=name
    return done,pl,todo
# @st.cache()
def run(done,pl,todo):
    import gspread_dataframe as gd
    import gspread as gs
    sh2=gc1.open("test").worksheet('Sheet2')
    done_day1 = gd.get_as_dataframe(sh2)
    up_done=done.append(pl).reset_index(drop=True)
    up_done=up_done.merge(todo,how='left',on='CÔNG VIỆC')
    td=datetime.date.today()
    up_done['NGÀY']=td
    up_done=up_done.replace(np.nan,"Công việc khác")
    up_done=up_done[up_done['CÔNG VIỆC'].isnull()==False]
    updated = done_day1.append(up_done)
    gd.set_with_dataframe(sh2, updated)
    done_dayY = gd.get_as_dataframe(sh2)
    done_dayY['NGÀY']=done_dayY['NGÀY'].astype('datetime64')
    done_dayY['NGÀY']=done_dayY['NGÀY'].dt.date
    done_day=done_dayY[done_dayY['NGÀY']==td]
    
    t1,t2,t3=st.columns(3)
    with t1:
        st.subheader(':trophy:Đệ:trophy:')

        de=done_day[done_day['NV']=='Đệ']
        de[['LOẠI CÔNG VIỆC','CÔNG VIỆC']]
        de.style.set_properties(**{'background-color': 'pink',
                           'color': 'green'})
    with t2:
        st.subheader(':monkey_face:Thuận:monkey_face:')
        thuan=done_day[done_day['NV']=='Thuận'].reset_index(drop=True)
        thuan[['LOẠI CÔNG VIỆC','CÔNG VIỆC']]
    with t3:
        st.subheader(':panda_face:Trọn:panda_face:')
        Tron=done_day[done_day['NV']=='Trọn'].reset_index(drop=True)
        Tron[['LOẠI CÔNG VIỆC','CÔNG VIỆC']]
    r1,r2,r3=st.columns(3)
    with r1:
        st.subheader(':penguin:Linh:penguin:')
        Linh=done_day[done_day['NV']=='Linh'].reset_index(drop=True)
        Linh[['LOẠI CÔNG VIỆC','CÔNG VIỆC']]

    with r2:
        st.subheader(':heart:Vân:heart:')
        Van=done_day[done_day['NV']=='Vân'].reset_index(drop=True)
        Van['CÔNG VIỆC']
    with r3:
        st.subheader(':ring:Duy:ring:')
        Duy=done_day[done_day['NV']=='Duy'].reset_index(drop=True)
        Duy[['LOẠI CÔNG VIỆC','CÔNG VIỆC']]

st.title(':star:CÁC VIỆC ĐÃ HOÀN THÀNH HÔM NAY:star:')
d=data(df)
done=d[0]
pl=d[1]
todo=d[2]
if st.button('Xác nhận'):

    # st.title('THÀNH QUẢ CỦA HÔM NÀY NÈ!:smile:')
    run(done,pl,todo)

# if st.button('Thành quả tuần này!'):
#     st.success()
