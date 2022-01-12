import datetime as dt
from os import close
from re import T
from PIL.Image import new
from numpy.core.fromnumeric import size
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
def pull_lsx(gc):
    sh=gc.open('DSX1.1 - Master Đơn hàng').worksheet('1.Master DH')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet).astype(str)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    ncc=ncc[['LỆNH SX','SỐ ĐH','TÊN KHÁCH HÀNG','TÊN SẢN PHẨM TTF','SỐ LƯỢNG',]]
    return ncc

def form(pr,sl,order_item,production):
    with st.form(key='columns_in_form'):
        rowss=len(production['Đơn hàng'].tolist())
        if not order_item:
            st.info('Nhập đầy đủ thông tin ở phía trên')
        else:
            r1,r2,r3=st.columns(3)
            with r1:
                b1=[]
                for nr in range(rowss):
                    b1.append(r1.selectbox('Tên vật tư', [pr[nr]],key=f'dfuestidn {nr}'))

            with r2:
                b2=[]
                for nr in range (rowss):
                    b2.append(r2.text_input('SL đặt hàng',sl[nr],key=f'dfuesidn {nr}'))
            with r3:
                b3=[]
                for nr in range (rowss):
                    b3.append(r3.text_input('SL nhập kho',key=f'dfuesidn {nr}'))
        st.form_submit_button('Hoàn tất')
        dic={'Tên vật tư':b1,'Số lượng':b3}
        data=pd.DataFrame.from_dict(dic)
        data['Đơn hàng']=order_item[0]
        data['Ngày nhập kho']=pd.to_datetime('today').date()
        return data
def push(df,gc,sheet):
    import gspread_dataframe as gd
    import gspread as gs
    sheet=gc.open("Kho sơn - DS đặt hàng").worksheet(sheet)
    data=gd.get_as_dataframe(sheet)
    new_df=data.append(df)
    # new_df['Tên vật tư']=new_df['Tên vật tư'].dropna()
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
        push(data,gc,'Nhập kho')
    
elif thaotac=='Xuất kho':
    c1,c2=st.columns(2)
    with c1:
            nm=st.multiselect('Xuất cho nhà máy:',['NM1','NM3','NM5','Khác'])
    with c2:
        lsx_df=pull_lsx(gc)
        lsx_id=lsx_df['LỆNH SX'].tolist()
        lsx=st.multiselect('Tên Lệnh SX',lsx_id)
    sanpham=lsx_df[lsx_df['LỆNH SX']==lsx[0]]
    c3,c4=st.columns(2)
    with c3:
        cd=st.multiselect('Xuất cho công đoạn:',['Lót 1','Lót 2','Bóng thành phẩm'])
    with c4:
        sl_sp=st.text_input('Cho số lượng ghế:',)
    data=pull(gc)
    st.subheader('Xuất các vật tư sau:')
    xuatkho=data[data['Đơn hàng']==order_item[0]]
    vattuxuatkho=xuatkho['Tên vật tư'].tolist()
    xlxuat=xuatkho['Số lượng'].tolist()
    data1=form(vattuxuatkho,xlxuat,order_item,xuatkho)

    def increment_counter(increment_value=0):
        st.session_state.count += increment_value
    def imcrement_counter(increment_value=0):
        st.session_state.count -= increment_value
    c1,c2,c3,c4,c5=st.columns((1,1,1,1,1))
    with c1:
        st.button('Thêm dòng', on_click=increment_counter,
            kwargs=dict(increment_value=1))
    with c2:
        st.button('Giảm dòng', on_click=imcrement_counter,
            kwargs=dict(increment_value=1))
    h=st.session_state.count   
    with st.form(key='abc'):
        st.subheader('Bổ sung thêm các vật tư sau')
        df=pd.read_excel('TTT_ver2/t.xlsx')
        vattu=df['Tên sản phẩm'].unique().tolist()
        r1,r2,=st.columns(2)
        with r1:
            b1=[]
            for nr in range(h):
                r=r1.multiselect('Tên vật tư',vattu,key=f'dfuestidn {nr}')
                if not r:
                    st.write('')
                else:
                 b1.append(r[0])

        with r2:
            b2=[]
            for nr in range (h):
                b2.append(r2.text_input('Số lượng',key=f'dfuesidn {nr}'))
        st.form_submit_button('Hoàn tất')
        dic2={'Tên vật tư':b1,'Số lượng':b2}
        data2=pd.DataFrame.from_dict(dic2)

    if st.button('Hoàn tất xuất kho'):
        data=data1.append(data2)
        data['Tên Sản phẩm']=sanpham['TÊN SẢN PHẨM TTF'].tolist()[0]
        data['Nhà máy']=nm[0]
        data['Lệnh SX']=lsx[0]
        data['Công đoạn']=cd[0]
        data['SL sản phẩm']=sl_sp
        data['Ngày xuất kho']=pd.to_datetime('today').date()
        data=data.drop(columns={'Ngày nhập kho','Đơn hàng'})   
        data=data.astype(str)
        data
        push(data,gc,'Xuất kho')

        fig, ax = plt.subplots(figsize = (4,.2))
        ax.set_title('TTF - Phiếu xuất kho',loc='left')
        # ax.axis('tight')
        ax.axis('off')

        the_table = ax.table(cellText = data.values, colLabels = data.columns,loc='bottom')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(9)

        pp = PdfPages("phieu_xuat_kho.pdf")
        pp.savefig(fig, bbox_inches = 'tight')
        pp.close()

        with open("phieu_xuat_kho.pdf", 'rb') as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download=phieu_xuat_kho.pdf.pdf>Download data</a>'
            f.close()
    st.markdown(href, unsafe_allow_html=True)
        
