import datetime as dt
from os import close
from re import T
from PIL.Image import new
import pandas as pd
from pyasn1.debug import Scope
import streamlit as st
import base64,io,gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from streamlit.elements.arrow import Data #-> Để nhập Google Spreadsheet Credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
if 'count' not in st.session_state:
    st.session_state.count = 0



def form(pr,sl,order_item,production):
    with st.form(key='columns_in_form'):
        rowss=len(production['Đơn hàng'].tolist())
        if not order_item:
            st.info('Nhập đầy đủ thông tin ở phía trên')
        else:
            r1,r2,=st.columns(2)
            with r1:
                b1=[]
                for nr in range(rowss):
                    b1.append(r1.selectbox('Tên vật tư', [pr[nr]],key=f'dfuestidn {nr}'))

            with r2:
                b2=[]
                for nr in range (rowss):
                    b2.append(r2.text_input('Số lượng',sl[nr],key=f'dfuesidn {nr}'))
        st.form_submit_button('Hoàn tất')
        dic={'Tên vật tư':b1,'Số lượng':b2}
        data=pd.DataFrame.from_dict(dic)
        data['Đơn hàng']=order_item[0]
        data['Ngày nhập kho']=pd.to_datetime('today').date()
        return data
def push(df,gc):
    import gspread_dataframe as gd
    import gspread as gs
    sheet=gc.open("Kho sơn - DS đặt hàng").worksheet('Nhập kho')
    data=gd.get_as_dataframe(sheet)
    new_df=data.append(df)
    new_df['Tên vật tư']=new_df['Tên vật tư'].dropna()
    gd.set_with_dataframe(sheet,new_df)
def pull(gc):
    import gspread_dataframe as gd
    import gspread as gs
    sheet=gc.open("Kho sơn - DS đặt hàng").worksheet('Nhập kho')
    data=gd.get_as_dataframe(sheet)
    return data
Cre=service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc=gspread.authorize(Cre)

sheet1=gc.open("Kho sơn - DS đặt hàng").worksheet('Sheet1')

data=sheet1.get_all_records()
df=pd.DataFrame(data)
order_list=df['Đơn hàng'].unique().tolist()
order_item=st.multiselect('Chọn đơn hàng',order_list)
thaotac=st.selectbox('Chọn loại thao tác',['Nhập kho','Xuất kho'])


if not thaotac:
    st.info('Chọn loại thao tác để tiếp tục')
elif thaotac=='Nhập kho': 

    production= df[df['Đơn hàng'].isin(order_item)]

    pr=production['Tên vật tư'].tolist()
    sl=production['Số lượng'].tolist()
    dvt=production['ĐVT'].tolist()


    data=form(pr,sl,order_item)
    data
    if st.button('Xuất danh sách'):
        push(data,gc)
    
elif thaotac=='Xuất kho':

    nm=st.multiselect('Xuất cho nhà máy:',['NM1','NM3','NM5','Khác'])
    lsx=st.text_input('Tên Lệnh SX',)
    data=pull(gc)
    data
    st.subheader('Xuất các vật tư sau:')
    xuatkho=data[data['Đơn hàng']==order_item[0]]
    vattuxuatkho=xuatkho['Tên vật tư'].tolist()
    xlxuat=xuatkho['Số lượng'].tolist()
    data1=form(vattuxuatkho,xlxuat,order_item,xuatkho)
    data1
    def increment_counter(increment_value=0):
        st.session_state.count += increment_value
    c1,c2,c3,c4,c5=st.columns((1,1,1,1,1))
    with c1:
        st.button('Thêm dòng', on_click=increment_counter,
            kwargs=dict(increment_value=1))
        h=st.session_state.count
    
    with st.form(key='abc'):
        st.subheader('Bổ sung thêm các vật tư sau')


        r1,r2,=st.columns(2)
        with r1:
            b1=[]
            for nr in range(h):
                b1.append(r1.text_input('Tên vật tư',key=f'dfuestidn {nr}'))

        with r2:
            b2=[]
            for nr in range (h):
                b2.append(r2.text_input('Số lượng',key=f'dfuesidn {nr}'))
        st.form_submit_button('Hoàn tất')
        dic2={'Tên vật tư':b1,'Số lượng':b2}
        data2=pd.DataFrame.from_dict(dic2)

    if st.button('Hoàn tất xuất kho'):
        data=data1.append(data2)
        data['Nhà máy']=nm[0]
        data['Lệnh SX']=lsx
        data['Ngày xuất kho']=pd.to_datetime('today').date()
        data=data.drop(columns={'Ngày nhập kho','Đơn hàng'})   
        data
        fig, ax = plt.subplots(figsize = (4,.2))
        ax.set_title('TTF - Phiếu xuất kho',loc='left')
        # ax.axis('tight')
        ax.axis('off')

        the_table = ax.table(cellText = data.values, colLabels = data.columns,loc='bottom')
        pp = PdfPages("phieu_xuat_kho.pdf")
        pp.savefig(fig, bbox_inches = 'tight')
        pp.close()

        with open("phieu_xuat_kho.pdf", 'rb') as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download=phieu_xuat_kho.pdf.pdf>Download data</a>'
            f.close()
    st.markdown(href, unsafe_allow_html=True)
