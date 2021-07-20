import streamlit as st
import requests #-> Để gọi API
import re #-> Để xử lý data dạng string
from datetime import datetime as dt #-> Để xử lý data dạng datetime
import gspread #-> Để update data lên Google Spreadsheet
import numpy as np
import pandas as pd #-> Để update data dạng bản
import json 
import matplotlib.image as mpimg
from google.oauth2 import service_account
from datetime import datetime, timedelta
from datetime import datetime as dt
from typing import Text
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials

from numpy.core.numeric import NaN
import streamlit as st
import json
import requests
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc2 = gspread.authorize(credentials)
spreadsheet_key='1Kf79UeBTa0q2NAh4PaW2Y1nqE__S0wiSQSOkk2dkQm0'

gc3 = gspread.authorize(credentials)
spreadsheet_key = '1ECQkxew8ixIxb43FVyd3d8LmtRo5VHr1fvt3A7a88L8'

sh9 = gc3.open("MẪU - dataset for Python").worksheet('Error')
error_=sh9.get_all_records()
error_df=pd.DataFrame(error_)

sh4=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('D.SÁCH')
order_df=sh4.get_all_records()
order_df=pd.DataFrame(order_df)
#week_plan
sh5=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('T.ĐỘ SX')
plan_df=sh5.get_all_records()
plan_df=pd.DataFrame(plan_df)
order_df.columns = order_df.columns.str.replace(' ', '_')
sheet10=gc3.open("MẪU - dataset for Python").worksheet('TD')
process_=sheet10.get_all_records()
process_df=pd.DataFrame(process_)
process_df.columns=process_df.columns.str.replace(' ',"_")
plan_df.columns=plan_df.columns.str.replace(' ',"_")
attend_=error_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
attend_df=attend_[['SỐ_ĐƠN_HÀNG','BƯỚC','MÃ_KHÁCH_HÀNG','NV_PTM_y','TÊN_SẢN_PHẨM_y','NHÀ_MÁY_x','NVLM','TÌNH_TRẠNG_x','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO_x','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]
conditions = [
    (attend_df['BƯỚC'] <= 3),(attend_df['BƯỚC'] == 5),(attend_df['BƯỚC'] == 6),(attend_df['BƯỚC'] ==7),(attend_df['BƯỚC'] ==8),(attend_df['BƯỚC'] ==9),(attend_df['BƯỚC'] ==10),
    (attend_df['BƯỚC'] ==11),(attend_df['BƯỚC'] >11)]
choices = ['TRIỂN KHAI ĐH','THU MUA','THU MUA','RA RẬP','RA RẬP','RA PHÔI','LÀM MẪU','QC MẪU','SƠN & NỆM']
attend_df['VỊ TRÍ'] = np.select(conditions, choices, default="")
hist_=process_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
hist_df=hist_[['SỐ_ĐƠN_HÀNG','BƯỚC','MÃ_KHÁCH_HÀNG','NV_PTM_y','TÊN_SẢN_PHẨM_y','NHÀ_MÁY_x','NVLM','TÌNH_TRẠNG_x','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO_x','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]


st.cache()
def check_attend(attend):

    st.markdown("")
    c,col1,e,col2,d=st.beta_columns((.5,2,.2,2,.5))
    with col1:
        st.markdown('Bản vẽ')
        drawing=attend.loc[attend['VỊ TRÍ']=='TRIỂN KHAI ĐH']
        drawing=drawing.reset_index()
        drawing=drawing.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        drawing
        st.markdown('RẬP')
        _8_df=attend.loc[attend['VỊ TRÍ']=='RA RẬP']
        _8_df=_8_df.reset_index()
        _8_df=_8_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)       
        _8_df
        st.markdown('MẪU')
        MAU_df=attend.loc[attend['VỊ TRÍ']=='LÀM MẪU']
        MAU_df=MAU_df.reset_index()
        MAU_df=MAU_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        MAU_df
        st.markdown('SƠN-NỆM')
        SN_df=attend.loc[attend['VỊ TRÍ']=='SƠN-NỆM']
        SN_df=SN_df.reset_index()
        SN_df=SN_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        SN_df
    with col2:
        st.markdown('THU MUA')
        out_df=attend.loc[attend['VỊ TRÍ']=='THU MUA']
        out_df=out_df.reset_index()
        out_df=out_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        out_df
        st.markdown('PHÔI')
        TD_df=attend.loc[attend['VỊ TRÍ']=='RA PHÔI']
        TD_df=TD_df.reset_index()
        TD_df=TD_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        TD_df
        st.markdown('QC')
        QC_df=attend.loc[attend['VỊ TRÍ']=='QC MẪU']
        QC_df=QC_df.reset_index()
        QC_df=QC_df.drop(['VỊ TRÍ','index','TÌNH_TRẠNG_x'],axis=1)
        QC_df
st.cache()
def check_plan(plan):
    from datetime import date

    _week=date.today().isocalendar()[1]
    plan_=plan.loc[plan.WEEK==_week+1]
    plan_toweek=plan_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NHÀ_MÁY','REMARKS']]
    plan_done=plan_.loc[plan_.REMARKS=='Done']
    plan_done=plan_done[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NHÀ_MÁY','REMARKS']]
    plan_done=plan_done.reset_index(drop=True)
    st.markdown("""
    ### A. DANH SÁCH KẾ HOẠCH MẪU
    """)
    col1,col2=st.beta_columns((1,1))
    with col1:
        plan_today=plan_toweek.loc[plan_toweek.REMARKS=="HÔM NAY"]
        plan_today=plan_today.reset_index(drop=True)
        st.markdown("<h4 style='text-align: left'>HÔM NAY</h4>", unsafe_allow_html=True)
        st.markdown('')    
        st.write(plan_today)
        st.markdown('')

    #Plan ngày mai
    with col2:
        plan_tomorrow=plan_toweek.loc[plan_toweek.REMARKS=="NGÀY MAI"]
        plan_tomorrow=plan_tomorrow.reset_index(drop=False)
        st.markdown("<h4 style='text-align: left'>NGÀY MAI</h4>", unsafe_allow_html=True)
        st.markdown('')
        st.write(plan_tomorrow)
        st.markdown('')
    #plan đang bị trễ
        plan_late=plan_toweek.loc[plan_toweek.REMARKS=="TRỄ"]
        plan_late=plan_late.reset_index(drop=True)
        st.markdown("<h4 style='text-align: left; color:red'>ĐANG TRỄ </h4>", unsafe_allow_html=True)
        st.markdown('')  
        st.write(plan_late)

        st.markdown("<h4 style='text-align: left; color:blue'>ĐÃ GIAO HÀNG TRẮNG</h4>", unsafe_allow_html=True)
        st.markdown('')  
        st.write(plan_done)
        st.markdown('')
    st.markdown("<h4 style='text-align: left'>TRONG TUẦN</h4>", unsafe_allow_html=True)
    st.markdown('')    
    plan_doing=plan_toweek.loc[(plan_toweek.REMARKS=='ĐANG LÀM')]
    st.write(plan_doing)
    st.markdown("")
    st.markdown("")

def check_order(id):
    hist_order=order_df.loc[order_df.SỐ_ĐƠN_HÀNG==id]
    hist_orderr=hist_df.loc[hist_df.SỐ_ĐƠN_HÀNG==id].reset_index(drop=True)
    product_name=hist_order[['TÊN_SẢN_PHẨM','NV_PTM','NHÀ_MÁY','MÃ_KHÁCH_HÀNG']].drop_duplicates().values.tolist()
    st.markdown('TÊN SẢN PHẨM: **{}**'.format(product_name[0][0]))
    st.markdown('NHÂN VIÊN PHỤ TRÁCH: **{}**'.format(product_name[0][1]))
    st.markdown('NHÀ MÁY: **{}**'.format(product_name[0][2]))
    st.markdown('MÃ_KHÁCH_HÀNG: **{}**'.format(product_name[0][3]))
    historder=hist_orderr[['BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO_x','NGÀY_GIẢI_QUYẾT']]
    st.dataframe(data=historder, width=700, height=1068)

def check_error(error):
    col1,col2=st.beta_columns((1,1))
    with col1:
        st.markdown('Chưa scan giao')
        out=error.loc[error['TÌNH_TRẠNG']=='Chưa giao']
        out_df=out[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY']]
        out_df
        st.markdown('Chưa scan nhận')
        in_=error.loc[error['TÌNH_TRẠNG']=='Chưa nhận']
        in_df=in_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY']]
        in_df
    with col2:
        st.markdown('Đang xử lí')
        doing=error.loc[error['TÌNH_TRẠNG']=='Đang xử lí']
        doing_df=doing[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY']] 
        doing_df
########################################
# st.set_option('deprecation.showPyplotGlobalUse', False)
col1 = st.sidebar
choose=col1.selectbox('Chọn đối tượng 1',['NHÀ_MÁY','NV_PTM','BỘ_PHẬN','SỐ_ĐƠN_HÀNG'])
if choose=='NV_PTM':
    _1 = ["A. Hoàng","A. Sáng",'A. Bảo','C. Hai','C. Như','C. Thy']
    choose_type=col1.selectbox('Chọn đối tượng 2',_1)
    c=st.sidebar.selectbox('Chọn',['VỊ TRÍ CỦA MẪU','KẾ HOẠCH MẪU TUẦN NÀY'])
    if c=='VỊ TRÍ CỦA MẪU':
        check_by_per=attend_df.loc[attend_df['NV_PTM_y']==choose_type]
        check_by_per=check_by_per[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_y','NHÀ_MÁY_x','TÌNH_TRẠNG_x','VỊ TRÍ']]
        check_attend(check_by_per)
    else:
        plan_=plan_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
        plan_=plan_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NGÀY_KẾ_HOẠCH','REMARKS','NHÀ_MÁY','NV_PTM','WEEK']]
        check_by_per=plan_.loc[plan_['NV_PTM']==choose_type]
        check_plan(check_by_per)

elif choose=="NHÀ_MÁY":
    _1= ['NM1','NM3','X4','NM NỆM']
    choose_type=col1.selectbox('Chọn đối tượng 2',_1)
    check_by_per=attend_df.loc[attend_df['NHÀ_MÁY_x']==choose_type]
    check_by_per=check_by_per[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_y','NHÀ_MÁY_x','TÌNH_TRẠNG_x','VỊ TRÍ']]
    
    c=st.sidebar.selectbox('Chọn',['VỊ TRÍ CỦA MẪU','KẾ HOẠCH MẪU TUẦN NÀY'])
    if c=='VỊ TRÍ CỦA MẪU':
        check_attend(check_by_per)
    else:
        plan_=plan_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
        plan_=plan_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NGÀY_KẾ_HOẠCH','REMARKS','NHÀ_MÁY','NV_PTM','WEEK']]
        check_by_per=plan_.loc[plan_['NHÀ_MÁY']==choose_type]
        check_plan(check_by_per)
elif  choose=='SỐ_ĐƠN_HÀNG':
    choose_type=st.sidebar.text_input('Nhập tên đơn hàng','M.00.00.00')
    if not choose_type:
        st.error('Hãy nhập mã đơn hàng!')
    else:
        check_order(choose_type)
else:
    _1=process_df['BỘ_PHẬN'].unique().tolist()
    choose_type=col1.selectbox('Chọn đối tượng 2',_1)
    _error=error_df.loc[error_df['BỘ_PHẬN']==choose_type]
    check_error(_error)

