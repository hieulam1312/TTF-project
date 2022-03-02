import datetime as dt
from ipaddress import collapse_addresses
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

    
st.title("KHO SƠN - XUẤT SƠN CHO SẢN XUẤT")
lsx_df=pull_lsx(gc)

with st.form(key='abcd'):
    c1,c2=st.columns(2)
    with c1:
        nm=st.multiselect('Xuất cho chuyền sơn:',['Treo 1','Treo 2','Pallet 1','Pallet 2','Pallet 3','Pallet 5',"Metro",'Handpick'])
    with c2:
        kh=st.selectbox("Loại đề xuất",['Kế hoạch','Phát sinh'])
        lsx_id=lsx_df['LỆNH SX'].unique().tolist()
    l1,l2=st.columns(2)
    with l1:
        lsx=st.multiselect('Tên Lệnh SX',lsx_id)
        sanpham = lsx_df[lsx_df['LỆNH SX'].isin(lsx)]
        sl_sp=st.text_input('Cho số lượng ghế:',)

    sanpham
    with l2:
        sanpham = lsx_df[lsx_df['LỆNH SX'].isin(lsx)]
        cd=st.multiselect('Loại Bước sơn',['Lót 1',"Stain 1",'Bóng','Lót 2',"Stain 2",'Sửa gỗ','Dặm màu','Glaze màu','Màu','Xăng','Lau màu','Fw màu','Tẩy gỗ',"chống mốc"])

        slson=st.text_input('Số kg cần lấy')


    st.form_submit_button('Hoàn tất')


id=lsx[0]

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
with c3:
    h=st.session_state.count+4   

    st.write('Tổng số dòng: {}'.format(h ))
with st.form(key='abc'):
    st.subheader('Bước sơn có các vật tư sau:')
    df=pd.read_excel('TTT_ver2/t.xlsx')
    vattu=df['Tên sản phẩm'].unique().tolist()
    r1,r2,=st.columns(2)
    with r1:
        b1=[]
        for nr in range(h):
            r=r1.selectbox('Tên vật tư',vattu,key=f'dfuestidn {nr}')
            b1.append(r)
    with r2:
        b2=[]
        for nr in range (h):
            b2.append(r2.number_input('Khối lượng',key=f'dfuesidn {nr}'))
    st.form_submit_button('Hoàn tất')
dic2={'Tên vật tư':b1,'Tỉ lệ':b2}
data2=pd.DataFrame.from_dict(dic2)
data2['Số lượng']=(int(slson)*data2["Tỉ lệ"].astype(float))/sum(b2) 
data2
if st.button('Hoàn tất xuất kho'):
    data=data2.copy()
    data['Tên Sản phẩm']=str(sanpham['TÊN SẢN PHẨM TTF'].tolist())
    data['Nhà máy']=nm[0]
    data['Lệnh SX']=str(lsx)
#     data['SỐ ĐH']=sdh_id[0]
    data['SL sản phẩm']=sl_sp
    data['Loại đề xuất']=kh
    data['Bước sơn']=cd[0]
    # data[]
    data['Khối lượng sơn']=slson
    data['Ngày xuất kho']=pd.to_datetime('today').date()
    data=data.astype(str)
    data
    # data1=data.drop(columns={'Ngày nhập kho','Đơn hàng'})   
    data1=data.copy()
    push(data1,gc,'Xuất kho')
    data2=data1[['Tên vật tư','Số lượng']]
    
    if len(sanpham['TÊN SẢN PHẨM TTF'].tolist()) ==0:
        tsp=""
    else:
        tsp=sanpham['TÊN SẢN PHẨM TTF'].tolist()[0]
    title_text ='TTF - Phiếu xuất kho ngày {}'.format(pd.to_datetime('today').date())
    subtitle_text = '\n \nLSX: {} - Chuyền sơn: {}'.format(id,nm[0])
    annotation_text = 'Nhà máy                                         Thủ kho sơn'
    sp='\n \nTên SP: {} \n \nSL ghế: {} \n \nBước sơn: {}\n \nKhối lượng sơn: {} kg'.format(tsp,sl_sp,cd[0],slson)
    footer_text = 'Ngày xuất {}'.format(pd.to_datetime('today').date())
    plt.figure(linewidth=1,
            
            tight_layout={'pad':1},
            # figsize=(5,4)
            )


    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Hide axes border
    plt.box(on=None)

    # Add title
    plt.suptitle(title_text,
                weight='bold',
                size=14,
                )

    # Add subtitle
    plt.figtext(0.5, 0.9,
                subtitle_text,
                horizontalalignment='center',
                size=12, style='italic',
                
            )
    plt.figtext(0.1, 0.5,
                sp,
                horizontalalignment='left',
                size=10,
                

            )

    # Add annotation
    plt.figtext(0.5, 0.3,
                annotation_text,
                horizontalalignment='center',
                size=9, weight='light',
                
            )

    plt.draw()

    fig = plt.gcf()


    # the_table.scale(2,1)
    pp = PdfPages("phieu_xuat_kho.pdf")
    pp.savefig(fig, bbox_inches = 'tight')
    pp.close()

    with open("phieu_xuat_kho.pdf", 'rb') as f:
        data = f.read()
        bin_str = base64.b64encode(data).decode()
        f.close()
    st.download_button(label='📥 Tải file xuống',
                            data=data ,
                            file_name= "phieu_xuat_kho.pdf")
