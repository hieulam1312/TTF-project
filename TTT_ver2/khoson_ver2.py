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
from io import BytesIO
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
    ncc=ncc[['LỆNH SX','SỐ ĐH','TÊN KHÁCH HÀNG','TÊN SẢN PHẨM TTF','SỐ LƯỢNG','MÀU SƠN']]
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
    sh=gc.open("Kho sơn - DS đặt hàng").worksheet('Xuất kho')
    sheet=sh.get_all_records()
    data=pd.DataFrame(sheet).astype(str)

    data=data[data['FILTER']=="C"]
    data['Tên Sản phẩm'],data['Lệnh SX']=data['Tên Sản phẩm'].str.replace("'",""),data['Lệnh SX'].str.replace("'","")
    data['Tên Sản phẩm'],data['Lệnh SX']=data['Tên Sản phẩm'].str.replace("[",""),data['Lệnh SX'].str.replace("[","")
    data['Tên Sản phẩm'],data['Lệnh SX']=data['Tên Sản phẩm'].str.replace("]",""),data['Lệnh SX'].str.replace("]","")
    data=data[['Mã phiếu đề xuất','Tên Sản phẩm','Lệnh SX','Tên vật tư','Số lượng','Ngày xuất kho','Nhà máy','NHÀ MÁY','Khách hàng']]
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1',index=False)
    workbook = writer.book
    # worksheet = writer.sheets['Sheet1','Sheet2']
    writer.save()
    processed_data = output.getvalue()
    return processed_data
Cre=service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc=gspread.authorize(Cre)

# sheet1=gc.open("Kho sơn - DS đặt hàng").worksheet('Sheet1')

# data=sheet1.get_all_records()
# df=pd.DataFrame(data)
# order_list=df['Đơn hàng'].unique().tolist()

if st.sidebar.button('Tải DS cho Kế toán'):
    data=pull(gc)
    st.sidebar.download_button(label='📥 Tải file xuống',
                            data=data,
                            file_name= "phieu_xuat_kho.xlsx")
st.title("KHO SƠN - XUẤT SƠN CHO SẢN XUẤT")
lsx_df=pull_lsx(gc)

with st.form(key='abcd'):
    c1,c2,c3=st.columns(3)
    with c1:
        nm=st.multiselect('Xuất cho chuyền sơn:',['Treo 1','Treo 2','Pallet 1','Pallet 2','Pallet 3','Pallet 5',"Metro",'Handpick'])
    with c2:
        kh=st.multiselect("Loại đề xuất",['Kế hoạch','Phát sinh'])
        lsx_id=lsx_df['LỆNH SX'].unique().tolist()
        lsx_id.append('Nội địa')

    with c3:
        time=st.multiselect('Giờ nhận sơn:',['06:50 - 07:15','09:30 - 09:45',"13:00 - 13:15",'16:00 - 16:15','19:00 - 19:15'])
    l1,l2=st.columns(2)
    with l1:
        lsx=st.multiselect('Tên Lệnh SX',lsx_id)

        sl_sp=st.text_input('Cho số lượng ghế:',)

   
    with l2:
        sanpham = lsx_df[lsx_df['LỆNH SX'].isin(lsx)]
#         cd=st.multiselect('Loại Bước sơn',['Lót 1',"Stain 1",'Bóng','Lót 2',"Stain 2",'Sửa gỗ','Dặm màu','Glaze màu','Màu','Xăng','Lau màu','Fw màu','Tẩy gỗ',"chống mốc"])
        cd=st.text_input('Loại bước sơn',)
        cd=cd.replace('(',"").replace("%","").replace(")","").upper()
        cd=''.join([i for i in cd if not i.isdigit()])
        slson=st.text_input('Số kg cần lấy')


    st.form_submit_button('Hoàn tất')
if lsx[0]!="Nội địa":
    namesp=str(sanpham['TÊN KHÁCH HÀNG'].tolist()[0])
    nam=str(sanpham['TÊN SẢN PHẨM TTF'].tolist())
    mauson=str(sanpham['MÀU SƠN'].tolist()[0])
else:
    sanpham=""
    namesp=""
    nam=""
    mauson=""
sanpham
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
data2['Số lượng']=(float(slson)*data2["Tỉ lệ"].astype(float))/sum(b2) 
data2
if st.button('Hoàn tất xuất kho'):
    data=data2.copy()
    data['Tên Sản phẩm']=nam
    
    data['Nhà máy']=nm[0]
    data['Lệnh SX']=str(lsx)
    data['Giờ lấy sơn']=time[0]
    data['SL sản phẩm']=sl_sp
    data['Loại đề xuất']=kh[0]
    data['Bước sơn']=cd
    data['Khách hàng']=namesp
    data['MÀU SƠN']=mauson
    data['Khối lượng sơn']=slson
    from datetime import datetime
    import pytz
    tz = pytz.timezone('asia/ho_chi_minh')
    data['Ngày xuất kho']=datetime.now(tz).date().strftime("%m/%d/%Y")
    data["Giờ xuất kho"]=datetime.now(tz).strftime("%H:%M")
    data=data.astype(str)
    data
    barcode=nm[0][0]+datetime.now(tz).strftime('%d%m%H%M')

    data['Mã phiếu đề xuất']=barcode
    data1=data.copy()
    push(data1,gc,'Xuất kho')
    data2=data1[['Tên vật tư','Số lượng']]
    
    if len(nam) ==0:
        tsp=""
    else:
        tsp=sanpham['TÊN SẢN PHẨM TTF'].tolist()[0]

    title_text ='TTF - Phiếu xuất kho ngày {} lúc {}'.format(datetime.now(tz).date().strftime("%d/%m/%Y"),datetime.now(tz).strftime("%H:%M"))
    subtitle_text = '\n \nLSX: {} - Chuyền sơn: {}'.format(id,nm[0])
    annotation_text = 'Nhà máy                                         Thủ kho sơn'
    sp='\n \nGiờ lấy sơn: {} \n \nLoại đề xuất: {} \n \nTên SP: {} \n \nSL ghế: {} \n \nBước sơn: {}\n \nKhối lượng sơn: {} kg'.format(time[0],kh[0],tsp,sl_sp,cd,slson)
    footer_text = 'Ngày xuất {}'.format(pd.to_datetime('today').date())
    with PdfPages('multipage_pdf.pdf') as pp:
        plt.figure(linewidth=1,
                    
                    tight_layout={'pad':1},
                    # figsize=(5,4)
                    )
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
        plt.figtext(0.8, 0.8,
                barcode,
                horizontalalignment='right',
                size=12,style='italic')
        plt.figtext(0.1, 0.4,
                    sp,
                    horizontalalignment='left',
                    size=10,
                )

        # Add annotation
        plt.figtext(0.5, 0.3,
                    annotation_text,
                    horizontalalignment='center',
                    size=9, weight='light'        
                )
        footer_text = 'trang 1/2 - kho sơn'
        ...
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        plt.draw()

        fig1 = plt.gcf()
        pp.savefig()  # saves the current figure into a pdf page
        plt.close()
        plt.rc('text', usetex=False)


        plt.figure(linewidth=1,
                    
                    tight_layout={'pad':1},
                    # figsize=(5,4)
                    )
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
        plt.figtext(0.8, 0.8,
                barcode,
                horizontalalignment='right',
                size=12,style='italic')
        plt.figtext(0.1, 0.4,
                    sp,
                    horizontalalignment='left',
                    size=10,
                )

        # Add annotation
        plt.figtext(0.5, 0.3,
                    annotation_text,
                    horizontalalignment='center',
                    size=9, weight='light'        
                )
        footer_text = 'trang 2/2 - nhà máy'
        ...
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        plt.draw()

        fig1 = plt.gcf()

        pp.savefig()  # saves the current figure into a pdf page
        plt.close()

    with open("multipage_pdf.pdf", 'rb') as f:
        data = f.read()
        bin_str = base64.b64encode(data).decode()
        f.close()
    st.download_button(label='📥 Tải file xuống',
                            data=data ,
                            file_name= "phieu_xuat_kho.pdf")
