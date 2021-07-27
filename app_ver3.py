from matplotlib import legend
import streamlit as st
from datetime import datetime as dt #-> Để xử lý data dạng datetime
import gspread #-> Để update data lên Google Spreadsheet
import numpy as np
import pandas as pd #-> Để update data dạng bản 
from google.oauth2 import service_account
from datetime import datetime, timedelta,date
from datetime import datetime as dt
from typing import Text
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
from numpy.core.numeric import NaN
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
pd.plotting.register_matplotlib_converters()


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
error_df=error_df[['SỐ_ĐƠN_HÀNG','BƯỚC','NHÀ_MÁY','TÌNH_TRẠNG','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]
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
process_df=process_df.replace("",np.nan)

sheet11=gc3.open("MẪU - dataset for Python").worksheet('CALC')
calc_=sheet11.get_all_records()
calc_df=pd.DataFrame(calc_)
calc_df=calc_df[['SỐ ĐƠN HÀNG','NV PTM','TÊN SẢN PHẨM','NHÀ MÁY','NVLM','NGÀY NVLM GIAO','THÁNG GIAO','TUẦN GIAO','T/G TTF']]
calc_df['NGÀY NVLM GIAO']=pd.to_datetime(calc_df['NGÀY NVLM GIAO'])

calc_df.columns=calc_df.columns.str.replace(' ',"_")
calc_df=calc_df.replace("",np.nan)
###
plan_df.columns=plan_df.columns.str.replace(' ',"_")
attend_=error_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
error_all=error_df.merge(order_df,how='left',on='SỐ_ĐƠN_HÀNG')
attend_df=attend_[['SỐ_ĐƠN_HÀNG','BƯỚC','MÃ_KHÁCH_HÀNG','NV_PTM','TÊN_SẢN_PHẨM','NHÀ_MÁY_x','TÌNH_TRẠNG_x','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO_x','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]
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
    # plan_=plan.loc[plan.WEEK==_week+1]
    plan_toweek=plan[['NV_PTM','NHÀ_MÁY','SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','REMARKS']]
    plan_done=plan.loc[plan.REMARKS=='Done']
    plan_done=plan_done[['NV_PTM','NHÀ_MÁY','SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','REMARKS']]
    plan_done=plan_done.reset_index(drop=True)
    st.markdown("""
    ### A. DANH SÁCH KẾ HOẠCH MẪU
    """)
    c,col1,e,col2,d=st.beta_columns((.5,2,.2,2,.5))
    with col1:
        plan_today=plan_toweek.loc[plan_toweek.REMARKS=="HÔM NAY"]
        plan_today=plan_today.reset_index(drop=True)
        st.markdown("<h4 style='text-align: left'>HÔM NAY</h4>", unsafe_allow_html=True)
        st.markdown('')    
        st.write(plan_today)
        st.markdown('')
        plan_late=plan_toweek.loc[plan_toweek.REMARKS=="TRỄ"]
        plan_late=plan_late.reset_index(drop=True)
        st.markdown("<h4 style='text-align: left; color:red'>ĐANG TRỄ </h4>", unsafe_allow_html=True)
        st.markdown('')  
        st.write(plan_late)
        st.markdown('')
        st.markdown("<h4 style='text-align: left'>TRONG TUẦN</h4>", unsafe_allow_html=True)
        st.markdown('')    
        plan_doing=plan_toweek.loc[(plan_toweek.REMARKS=='ĐANG LÀM')]
        st.write(plan_doing)
        st.markdown("")
        st.markdown("")
    #Plan ngày mai
    with col2:
        plan_tomorrow=plan_toweek.loc[plan_toweek.REMARKS=="NGÀY MAI"]
        plan_tomorrow=plan_tomorrow.reset_index(drop=True)
        st.markdown("<h4 style='text-align: left'>NGÀY MAI</h4>", unsafe_allow_html=True)
        st.markdown('')
        st.write(plan_tomorrow)
        st.markdown('')
    #plan đang bị trễ

        st.markdown("<h4 style='text-align: left; color:blue'>ĐÃ GIAO HÀNG TRẮNG</h4>", unsafe_allow_html=True)
        st.markdown('')  
        st.write(plan_done)
def check_order(id,order_df):
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
    c,col1,e,col2,d=st.beta_columns((.5,2,.2,2,.5))
    with col1:
        st.markdown('Chưa scan giao')
        out=error.loc[error['TÌNH_TRẠNG_x']=='Chưa giao']
        out_df=out[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY_x']]
        out_df
        st.markdown('Chưa scan nhận')
        in_=error.loc[error['TÌNH_TRẠNG_x']=='Chưa nhận']
        in_df=in_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY_x']]
        in_df
    with col2:
        st.markdown('Đang xử lí')
        doing=error.loc[error['TÌNH_TRẠNG_x']=='Đang xử lí']
        doing_df=doing[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY_x']] 
        doing_df
def operation(calc,plan):
    month=date.today().month
    week_=date.today().isocalendar()[1]
    c,col1,d,col2,e=st.beta_columns((.5,10,.2,8,.5))
    
    done_=calc.loc[calc['THÁNG_GIAO']==month]

    done_month=done_.groupby(['NHÀ_MÁY','NVLM']).SỐ_ĐƠN_HÀNG.count().reset_index()
    total_month=done_month['SỐ_ĐƠN_HÀNG'].sum()
    done_['T/G_TTF']=done_['T/G_TTF'].astype(float)
    time_month=done_.loc[done_['T/G_TTF'].isnull()==False]
    avg_month=time_month['T/G_TTF'].mean()
    done=calc.groupby(['TUẦN_GIAO','NVLM']).SỐ_ĐƠN_HÀNG.count().reset_index()

    done_w=calc.loc[calc['TUẦN_GIAO']==week_]
    done_week=done_w.groupby(['NHÀ_MÁY','NVLM']).SỐ_ĐƠN_HÀNG.count().reset_index()
    total_week=done_week['SỐ_ĐƠN_HÀNG'].sum()

    time_week=done_w.loc[done_['T/G_TTF'].isnull()==False]
    avg_week=time_week['T/G_TTF'].mean()

    _1,_2,_3,_4,_5=st.beta_columns((.5,10,.2,10,.5))
    fig3, ax = plt.subplots()   
    sns.set_palette("pastel")
    st.set_option('deprecation.showPyplotGlobalUse',False)
    sns.barplot(data=done_month,x=done_month['NVLM'],y=done_month['SỐ_ĐƠN_HÀNG'],color='Green')
    plt.xticks(rotation=90)
    plt.show()
    fig4, ax = plt.subplots()   
    st.set_option('deprecation.showPyplotGlobalUse',False)
    sns.set_palette("pastel")
    sns.barplot(data=done_week,x=done_week['NVLM'],y=done_week['SỐ_ĐƠN_HÀNG'],color='Blue')
    plt.xticks(rotation=90)
    plt.show()
    with _2:
        st.markdown('Kết quả tháng: **{}**'.format(month))
        st.markdown('Hàng trắng: **{}**'.format(total_month))
        st.markdown('Thời gian: **{}** ngày'.format(avg_month))
        st.pyplot(fig3)
    with _4:
        st.markdown('Kết quả tuần: **{}**'.format(week_))
        st.markdown('Hàng trắng: **{}**'.format(total_week))
        st.markdown('Thời gian xử lí: **{}** ngày'.format(avg_week))
        st.pyplot(fig4) 


    plan_=plan.merge(calc,how='left',on='SỐ_ĐƠN_HÀNG')
    plan_=plan_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NGÀY_KẾ_HOẠCH','REMARKS','NHÀ_MÁY','NV_PTM','WEEK']]
    plan__=plan_.loc[plan_.WEEK==week_+1]
    # plan_
    check_plan(plan__)



col1 = st.sidebar
t1,t2,t3,t4,t5=st.beta_columns((5,.5,.1,1,.5))
with t1:
    st.title('OPERATION DASHBOARD')
r1,r2,r3,r4,r5=st.beta_columns((.5,.5,.1,1,.5))
with r1:
    ch=st.sidebar.selectbox('',['OVERVIEW','BỘ_PHẬN','SỐ_ĐƠN_HÀNG'])
if ch=='OVERVIEW':
    st.markdown('### OVERVIEW')
    st.markdown('Danh sách mẫu tại mỗi bộ phận')
    operation(calc_df,plan_df)

elif ch=='SỐ_ĐƠN_HÀNG':
    choose_type=st.sidebar.text_input('Nhập tên đơn hàng','M.00.00.00')
    if not choose_type:
        st.error('Hãy nhập mã đơn hàng!')
    else:
        check_order(choose_type,order_df)
else:
    _1=process_df['BỘ_PHẬN'].unique().tolist()
    choose_type=col1.selectbox('Chọn đối tượng 2',_1)
    _error=error_all.loc[error_df['BỘ_PHẬN']==choose_type]
    check_error(_error)

