from pandas.tseries.offsets import Week
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
from datetime import datetime, timedelta,date
from datetime import datetime as dt
from typing import Text
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
# import waterfall_chart
from numpy.core.numeric import NaN
import streamlit as st
import json
import requests
import altair as alt
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

gc1 = gspread.authorize(credentials)
spreadsheet_key = '1pMA3ZDjkL8gtIzQMyEkHwL_8-wDrXiO45OgtsPrkFec'
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
# order_df.columns = order_df.columns.str.replace(' ', '_')

#scan_df
sh1 = gc1.open("MẪU 2021 - COLLECT DATA").worksheet('UNPIVOT')
scan_df=sh1.get_all_records()
scan_df=pd.DataFrame(scan_df)
#td_df
sh2=gc1.open("MẪU 2021 - COLLECT DATA").worksheet('TD')
td_df=sh2.get_all_records()
td_df=pd.DataFrame(td_df)
#td_x4_df
sh3=gc1.open("MẪU 2021 - COLLECT DATA").worksheet('TD X4-NỆM')
td_x4_df=sh3.get_all_records()
td_x4_df=pd.DataFrame(td_x4_df)
sh6=gc1.open("MẪU 2021 - COLLECT DATA").worksheet('XL+ SL')
xl_sl=sh6.get_all_records()
xl_sl_df=pd.DataFrame(xl_sl)
#order_df

sh5=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('T.DÕI')
td_old=sh5.get_all_records()
td_old_df=pd.DataFrame(td_old)

sh7=gc3.open('TTF - MẪU 2021 - DƯỚI 12').worksheet('D.SÁCH')
under_12ds=sh7.get_all_records()
under_12ds_df=pd.DataFrame(under_12ds)
sh8=gc3.open('TTF - MẪU 2021 - DƯỚI 12').worksheet('T.DÕI')
under_12td=sh8.get_all_records()
under_12td_df=pd.DataFrame(under_12td)

sh8=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('Sheet53')
dataaa=sh8.get_all_records()
data=pd.DataFrame(dataaa)

nm_df=td_df.loc[(td_df['NHÀ MÁY']!='X4')|(td_df['NHÀ MÁY']!='NM NỆM')]
td_new_df=pd.concat([nm_df,td_x4_df])
td_new_df=td_new_df[['SỐ ĐƠN HÀNG','BƯỚC','IN','OT','NHÀ MÁY','NMVLM','BỘ PHẬN','NGÀY GIẢI QUYẾT','NHÓM MẪU']]
td_new_df=td_new_df.rename(columns={'IN': 'NGÀY NHẬN','OT':'NGÀY GIAO','NMVLM':'NVLM'})

# td_old_df.columns=td_old_df.columns.str.replace(" ","_")
td_all_df=pd.concat([td_old_df,td_new_df,under_12td_df])
td_all_df=td_all_df.replace('',np.nan)
td_2021_df=td_all_df[td_all_df['SỐ ĐƠN HÀNG'].notnull()]
td_2021_df.head()
td_2021_df.columns=td_2021_df.columns.str.replace(' ','_')

# under_12ds_df=under_12ds_df.rename(columns={'NV LÀM MẪU':'NVLM'})
under_12ds_df=under_12ds_df.drop(['BƯỚC'],axis=1)
nvlm=td_all_df
nvlm=nvlm[['SỐ ĐƠN HÀNG','NVLM']]
nvlm_df=nvlm.drop_duplicates()
nvlm_df=nvlm_df.dropna()

# xl_sl_df.columns=xl_sl_df.columns.str.replace(' ','_')
xl=xl_sl_df.loc[xl_sl_df['THAO TÁC']==' Giao đơn hàng']
xl_df=xl[['SỐ ĐH','XẾP LOẠI','SL THỰC TẾ']]
xl_df=xl_df.rename(columns={'SỐ ĐH':'SỐ ĐƠN HÀNG'})


under_12ds_df=under_12ds_df.drop(['NV LÀM MẪU'],axis=1)
order_df=order_df.drop(['GỖ','SƠN','NỆM','BAO BÌ','GHI CHÚ','HÌNH ẢNH'], axis = 1)
new_order=order_df.merge(xl_df,how='left',on='SỐ ĐƠN HÀNG')

order_2021_df=pd.concat([new_order,under_12ds_df])
order_new=order_2021_df.merge(nvlm_df,how='left',on='SỐ ĐƠN HÀNG')
order_new=order_new.replace(np.nan,0)
order_new['NGÀY GIAO']
pd.to_datetime(order_new['NGÀY GIAO'],dayfirst=True,errors='coerce')
# order_2021_df['NGÀY GIAO'].astype('datetime64')
# df['date'].astype('datetime64')
order_new['NGÀY GIAO']=pd.to_datetime(order_new['NGÀY GIAO'],dayfirst=True,errors='coerce')
order_new['NGÀY LẬP']=pd.to_datetime(order_new['NGÀY LẬP'],dayfirst=True,errors='coerce')
td_2021_df['NGÀY NHẬN']=pd.to_datetime(td_2021_df['NGÀY NHẬN'],dayfirst=True,errors='coerce')
td_2021_df['NGÀY GIAO']=pd.to_datetime(td_2021_df['NGÀY GIAO'],dayfirst=True,errors='coerce')
sheet11=gc3.open("MẪU - dataset for Python").worksheet('CALC')
calc_=sheet11.get_all_records()
calc_df=pd.DataFrame(calc_)
calc_df=calc_df[['SỐ ĐƠN HÀNG','TÊN SẢN PHẨM','NHÀ MÁY','NVLM','NGÀY NVLM GIAO','THÁNG GIAO','TUẦN GIAO','T/G TTF']]
calc_df['NGÀY NVLM GIAO']=pd.to_datetime(calc_df['NGÀY NVLM GIAO'])

calc_df.columns=calc_df.columns.str.replace(' ',"_")
calc_df=calc_df.replace("",np.nan)

process_df=td_2021_df
process_df.columns=process_df.columns.str.replace(' ',"_")
order_2021_df.columns=order_2021_df.columns.str.replace(' ',"_")
calc_df

plan_df.columns=plan_df.columns.str.replace(' ',"_")
attend_=error_df.merge(order_2021_df,how='left',on='SỐ_ĐƠN_HÀNG')
error_all=error_df.merge(order_2021_df,how='left',on='SỐ_ĐƠN_HÀNG')
attend_df=attend_[['SỐ_ĐƠN_HÀNG','BƯỚC','MÃ_KHÁCH_HÀNG','NV_PTM','TÊN_SẢN_PHẨM','NHÀ_MÁY_x','TÌNH_TRẠNG_x','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO_x','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]
conditions = [
    (attend_df['BƯỚC'] <= 3),(attend_df['BƯỚC'] == 5),(attend_df['BƯỚC'] == 6),(attend_df['BƯỚC'] ==7),(attend_df['BƯỚC'] ==8),(attend_df['BƯỚC'] ==9),(attend_df['BƯỚC'] ==10),
    (attend_df['BƯỚC'] ==11),(attend_df['BƯỚC'] >11)]
choices = ['TRIỂN KHAI ĐH','THU MUA','THU MUA','RA RẬP','RA RẬP','RA PHÔI','LÀM MẪU','QC MẪU','SƠN & NỆM']
attend_df['VỊ TRÍ'] = np.select(conditions, choices, default="")
hist_=process_df.merge(order_2021_df,how='left',on='SỐ_ĐƠN_HÀNG')
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
        plan_tomorrow=plan_tomorrow.reset_index(drop=False)
        st.markdown("<h4 style='text-align: left'>NGÀY MAI</h4>", unsafe_allow_html=True)
        st.markdown('')
        st.write(plan_tomorrow)
        st.markdown('')
    #plan đang bị trễ

        st.markdown("<h4 style='text-align: left; color:blue'>ĐÃ GIAO HÀNG TRẮNG</h4>", unsafe_allow_html=True)
        st.markdown('')  
        st.write(plan_done)
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
def operation(df,bp,calc,plan):
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
        st.markdown('Số lượng đã xong hàng trắng: **{}**'.format(total_month))
        st.markdown('Thời gian xử lí hàng trắng: **{}**'.format(avg_month))
        st.pyplot(fig3)
    with _4:
        st.markdown('Kết quả tuần: **{}**'.format(week_))
        st.markdown('Số lượng đã xong hàng trắng: **{}**'.format(total_week))
        st.markdown('Thời gian xử lí hàng trắng: **{}**'.format(avg_week))
        st.pyplot(fig4) 
    done_pivot=done.pivot(index='NVLM',columns='TUẦN_GIAO',values='SỐ_ĐƠN_HÀNG')
    done_pivot
    plan_=plan.merge(calc,how='left',on='SỐ_ĐƠN_HÀNG')
    plan_=plan_[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NGÀY_KẾ_HOẠCH','REMARKS','NHÀ_MÁY','WEEK']]
    plan__=plan_.loc[plan_.WEEK==week_+1]
    plan_toweek=plan__[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NHÀ_MÁY','REMARKS']]
    plan_doing=plan__.loc[plan__.REMARKS!='Done']
    plan_doing=plan_doing[['SỐ_ĐƠN_HÀNG','TÊN_SẢN_PHẨM_x','NHÀ_MÁY','REMARKS']]
    plan_doing=plan_doing.reset_index(drop=True)
    st.markdown("")
    plan_doing

    with col1:
        df_=df.loc[df['TÌNH_TRẠNG_x']!='Chưa giao']
        doing_count=df_.groupby(df_['BỘ_PHẬN']).SỐ_ĐƠN_HÀNG.count()
        doing_count=doing_count.reset_index()
        fig1, ax = plt.subplots()   
        plt.barh(doing_count['BỘ_PHẬN'], doing_count['SỐ_ĐƠN_HÀNG'], align='center')
        # plt.xlabel(doing_count['BỘ_PHẬN'])
        # plt.ylabel(doing_count['SỐ_ĐƠN_HÀNG'])
        plt.show()
    c,col1,d,col2,e=st.beta_columns((.5,10,.2,8,.5))
    with col1:
        st.pyplot(fig1)
        
    st.markdown('')
    nm=df_.drop_duplicates(subset=['SỐ_ĐƠN_HÀNG'])
    NM=nm.groupby(nm['NHÀ_MÁY_x']).SỐ_ĐƠN_HÀNG.count()
    NM_df=NM.reset_index()
    NM_df['NHÀ_MÁY_x']=NM_df['NHÀ_MÁY_x'].str.replace('#N/A','Chưa phân bổ')
    fig, ax = plt.subplots()   
    st.set_option('deprecation.showPyplotGlobalUse',False)
    sns.barplot(data=NM_df,x=NM_df['NHÀ_MÁY_x'],y=NM_df['SỐ_ĐƠN_HÀNG'])
    with col2:
        st.pyplot(fig)

    time=bp.loc[(bp['NGÀY_GIẢI_QUYẾT'].isnull==False)+(bp['NGÀY_GIẢI_QUYẾT']<1000)]
    time_df=time[['SỐ_ĐƠN_HÀNG','BỘ_PHẬN','NGÀY_NHẬN','NGÀY_GIAO','NGÀY_GIẢI_QUYẾT','NHÓM_MẪU']]
    time_df['NGÀY_GIAO']=pd.to_datetime(time_df['NGÀY_GIAO'])
    time_df['THÁNG_GIAO']=time_df['NGÀY_GIAO'].dt.month
    water_df=time_df.groupby(['BỘ_PHẬN','THÁNG_GIAO']).mean()
    water_df=water_df.reset_index()


    r1,r2,r3,r4,r5=st.beta_columns((.5,.5,.1,1,.5))
    with r2:
        month=st.number_input('Nhập tháng để xem:',step=1)
    h,c1,d=st.beta_columns((.5,2,.5))
    with c1:
        if not month:
            avg=water_df.groupby('BỘ_PHẬN').mean()
            avg=avg.reset_index()
        else:
            m_water=water_df.loc[water_df['THÁNG_GIAO']==month]
            avg=m_water.groupby('BỘ_PHẬN').mean()
            avg=avg.reset_index()  
        st.markdown('## THỜI GIAN XỬ LÍ TRUNG BÌNH CỦA CÁC BỘ PHẬN')
        waterfall_chart.plot(avg['BỘ_PHẬN'], avg["NGÀY_GIẢI_QUYẾT"],rotation_value=70)
        st.pyplot()
#######################################

# st.set_option('deprecation.showPyplotGlobalUse', False)
col1 = st.sidebar
t1,t2,t3,t4,t5=st.beta_columns((5,.5,.1,1,.5))
with t1:
    st.title('OPERATION DASHBOARD')
r1,r2,r3,r4,r5=st.beta_columns((.5,.5,.1,1,.5))
with r1:
    ch=st.sidebar.selectbox('',['OVERVIEW','KIỂM TRA TIẾN ĐỘ'])
if ch=='OVERVIEW':
    st.markdown('### OVERVIEW')
    st.markdown('Danh sách mẫu tại mỗi bộ phận')
    operation(error_all,process_df,calc_df,plan_df)
else:
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
        check_by_per=check_by_per[['SỐ_ĐƠN_HÀNG','MÃ_KHÁCH_HÀNG','TÊN_SẢN_PHẨM','NHÀ_MÁY_x','TÌNH_TRẠNG_x','VỊ TRÍ']]
        
        c=st.sidebar.selectbox('',['KẾ HOẠCH MẪU TUẦN NÀY','VỊ TRÍ CỦA MẪU'])
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
        _error=error_all.loc[error_df['BỘ_PHẬN']==choose_type]
        check_error(_error)

