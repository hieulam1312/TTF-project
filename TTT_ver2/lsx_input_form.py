# from typing_extensions import Concatenate
import numpy as np
from logging import error
from mimetypes import MimeTypes
import streamlit as st
import datetime as dt # to work with date, time
from bs4 import BeautifulSoup # to work with web scrapping (HTML)
import pandas as pd # to work with tables (DataFrames) data
from IPython.core.display import HTML
from streamlit.elements import multiselect # to display HTML in the notebook
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread #-> Để update data lên Google Spreadsheet
from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import gspread_dataframe as gd
import gspread as gs
from gspread.utils import A1_ADDR_ROW_COL_RE
st.set_page_config(layout='wide')
def pull_lsx(gc):
    spreadsheet_key='1dUUWEBwnD4kSJAwI3Oi4_fXN1Yji8cdth4Rs2RewCuw'
    sh=gc.open('DSX1.1 - Master Đơn hàng').worksheet('MASTER DH')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    ncc["SỐ ĐƠN HÀNG"]=ncc["SỐ ĐH"]

    sh2=gc.open('LSX - lưu trữ').worksheet('LSX ĐÃ IN')
    sheet2=sh2.get_all_values()
    lsx_cu=pd.DataFrame(sheet2)
    lsx_cu.columns=lsx_cu.iloc[0]
    list=lsx_cu['LỆNH SX'].unique().tolist()
    # list
    ncc=ncc[ncc["LỆNH SX"].isin(list)==False]
    # ncc
    return ncc
# ncc_list=ncc()

def push_lsx(df,gc):
    spreadsheet_key='1JCyNuairaKmF0KL6Sj-7IegwrrGJ366TUnkUqNxBRAE'
    import gspread_dataframe as gd
    import gspread as gs
    ws1 = gc.open("DSX2.1 - Lệnh sản xuất").worksheet("1. LENH SX")
    existing1 = gd.get_as_dataframe(ws1)
    existing1=existing1.dropna()
    updated1 = existing1.append(df)
    gd.set_with_dataframe(ws1,updated1)
    # sheet_index_no1 = 0
    # sh = gc.open_by_key(spreadsheet_key)
    # worksheet1 = sh.get_worksheet(sheet_index_no1)
    # set_with_dataframe(worksheet1, df)
    ws2 = gc.open("LSX - lưu trữ").worksheet("LSX ĐÃ IN")
    existing2 = gd.get_as_dataframe(ws2)
    updated2 = existing2.append(df)
    gd.set_with_dataframe(ws2, updated2)


    st.success('Done')


# def increment_counter(increment_value=0):
#     rows += increment_value

# def decrement_counter(decrement_value=0):
#     rows -= decrement_value
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'],
)
gc = gspread.authorize(credentials)

c0,c1,c2,c3,c4,c5,c6,c7= st.columns((1.8,1,.9,.9,.9,.9,.9,9))

st.cache()
if 'count' not in st.session_state:
    rows = 50

df=pull_lsx(gc)
with st.form(key='columns_in_form'):
    c0,c1,c2,c3,c4,c5,c6,c7,c8= st.columns((1.8,2,3,1,.9,.9,.9,.9,.9))

    list_r=df["LỆNH SX"].tolist()
    kh_r=df["TÊN KHÁCH HÀNG"].tolist()  
    sp=df["TÊN SẢN PHẨM TTF"].tolist()
    # cols = st.beta_columns(5)
    # for i, col in enumerate(cols):
    rows = 10



    # list_r=[50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    with c0:
        lsx=[]
        for nr in range(rows):
            lsx.append(c0.selectbox('',[list_r[nr]], key=f'dfuestidn {nr}'))
        # st.selectbox('Lệnh sản xuất',['a','b','c'])
    with c3:

        nm=[]
        for nr in range(rows):
            nm.append(c3.selectbox('Nhà máy',["",'NM1','NM3','NM5'], key=f'dfquestidn {nr}'))
        # st.selectbox('Lệnh sản xuất',['a','b','c'])
    with c4:
        ldh=[]
        for nr in range(rows):
            ldh.append(c4.selectbox('Loại đơn hàng',["",'C',"M"], key=f'dfquesatdidn {nr}'))  
    with c5:
        gc1=[]
        for nr in range(rows):
            gc1.append(c5.selectbox('Gia công ',["",'N',"Y"], key=f'dfqudesưtdidn {nr}')) 
    with c6:
        uc=[]
        for nr in range(rows):
            uc.append(c6.selectbox('V/e uốn cong ',["",'N',"Y"], key=f'dfqudesưtdidn{nr}')) 
    with c7:
        vn=[]
        for nr in range(rows):
            vn.append(c7.selectbox('Verneer ',["",'N',"Y"], key=f'dfqudestưdidn {nr}')) 
    with c8:
        kl=[]
        for nr in range(rows):
            kl.append(c8.selectbox('Kim loại ',["",'N',"Y"], key=f'dfqudestdidn1 {nr}')) 
    with  c1:
        ks=[]
        for nr in range(rows):
            ks.append(c1.selectbox('',[kh_r[nr]], key=f'dfuesstidn {nr}'))
    with c2:
        sap=[]
        for nr in range(rows):
            sap.append(c2.selectbox('',[sp[nr]], key=f'dfuestissdn {nr}'))
    st.form_submit_button('Submit')
    
    dict={"LỆNH SX":lsx,"NMSX":nm,"SẢN PHẨM (C/M)":ldh,"GIA CÔNG (Y/N)":gc1,"V/E U/CONG (Y/N)":uc,"DÁN VNR (Y/N)":vn,"K/L ĐB (Y/N)":kl}
    dff=pd.DataFrame.from_dict(dict)
    lsx_info=dff.merge(df,how='left',on="LỆNH SX")
    a=lsx_info[["LỆNH SX","TÊN KHÁCH HÀNG",	"TÊN SẢN PHẨM TTF",	 "NMSX",	"SẢN PHẨM (C/M)",	"GIA CÔNG (Y/N)",	"V/E U/CONG (Y/N)",	"DÁN VNR (Y/N)",	"K/L ĐB (Y/N)"]]
        # a

# t1,t2,t3,t4,t5,t6=st.columns((1,1,1,1,1,1))


# dff

if st.button('Push'):

    # Pull order_info
    # lsx_info=pull_lsx(gc)
    # lsx_info=lsx_info[["LỆNH SX",	"TÊN KHÁCH HÀNG",	"TÊN SẢN PHẨM TTF",	"SỐ LƯỢNG",	"ĐVT",	"LOẠI GỖ",	"MÀU SƠN"	,"NỆM"	,"NGÀY XUẤT",	"GHI CHÚ"]]
    lsx_info=lsx_info[["LỆNH SX",	 "NMSX",	"SẢN PHẨM (C/M)",	"GIA CÔNG (Y/N)",	"V/E U/CONG (Y/N)",	"DÁN VNR (Y/N)",	"K/L ĐB (Y/N)",	"SỐ ĐƠN HÀNG",	"TÊN KHÁCH HÀNG",	"TÊN SẢN PHẨM TTF",	"LOẠI GỖ"	,"MÀU SƠN"	,"NỆM"	,"SỐ LƯỢNG",	"ĐVT",	"NGÀY XUẤT",	"GHI CHÚ"]]

    #push lsx_info
    push_lsx(lsx_info,gc)




# # Create form input

# st.subheader('Nhập thông tin:')
# # 
# # st.set_page_config(layout='wide')
# a2,a3,a4,a5=st.columns((1.5,1.5,1,1))
# with a2:
#     ncc=st.multiselect('NCC:',list_ncc)
# with a3:
#     qc=st.multiselect('QC kiểm:',qc_list)
# with a4:
#     go=st.multiselect('Loại gỗ:',go_list)
# with a5:
#     da=st.text_input('Độ ẩm:',)
# if not ncc:
#     st.info('Nhập đầy đủ thông tin ở phía trên')
# else:
#     st.subheader('Danh sách kiểm chi tiết:')
#     # dv=st.selectbox('Đơn vị đo:',['mm','Inch','feet'])

#     r1,r2,r3,r4,r5=st.columns((1,1,1,2,2))
#     if 'count' not in st.session_state:
#         rows = 0

#     def increment_counter(increment_value=0):
#         rows += increment_value

#     def decrement_counter(decrement_value=0):
#         rows -= decrement_value
    
#     c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
#     with c1:
#         st.button('Thêm dòng', on_click=increment_counter,
#             kwargs=dict(increment_value=1))
#     with c2:
#         st.button('Giảm dòng', on_click=decrement_counter,
#             kwargs=dict(decrement_value=1))
#     with c4:
#         st.write('Tổng số dòng = ', rows+1)
#     h=rows
#     with r1:
#         a=st.text_input('Dày',)


#     with r2:
#             b=[st.text_input('Rộng',)]
#             for nr in range(rows):
#                 b.append(st.text_input(label='', key=f'2`1 {nr}'))
#     with r3:
#             c=[st.text_input('Dài',)]
#             for ng in range(rows):
#                 c.append(st.text_input(label='', key=f'dfuestion {ng}'))
#     with r4:
#             d= [st.number_input('Số thanh',step=1)]
#             for ngg in range(rows):
#                 d.append(st.number_input(label='', key=f'Quesdfgtion {ngg}',step=  1))

    
#     b=["0" if v =="" else v for v in b]
#     c=["0" if v =="" else v for v in c]
#     d=["0 "if v =="" else v for v in d]


#     b1=[]
#     c1=[]
#     a1=a.replace(',','.')

#     for b_ in b:
#         new_string = b_.replace(',','.')
#         b1.append(new_string)
#     for c_ in c:
#         new_string = c_.replace(',','.')
#         c1.append(new_string)

#     if a=="0":
#         st.info('Nhập đầy đủ thông tin vào form phía trên')
#     else:  
#         ncc_index=list_ncc.index(ncc[0])
#         ini=list_int[ncc_index]

#         dict={'Rộng':b1,'Dài':c1,'Số thanh':d}
    
#         import pandas as pd
#         df=pd.DataFrame.from_dict(dict)    
 

#         cls1,cls2,cls3=st.columns(3)
#         with cls1:
#             tk=st.number_input('Thẻ Kiện:',step=1)
#         with cls2:
#             ml=st.text_input('Mã lô:',)
#         with cls3:
#             clg=st.text_input('Chất lượng gỗ',)
  


                
