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
def pull_lsx(gc):
    spreadsheet_key='1dUUWEBwnD4kSJAwI3Oi4_fXN1Yji8cdth4Rs2RewCuw'

    sh=gc.open('DSX1.1 - Master Đơn hàng').worksheet('MASTER DH')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    ncc["SỐ ĐƠN HÀNG"]=ncc["SỐ ĐH"]
    # ncc["NMSX"]=""
    # ncc["SẢN PHẨM (C/M)"]=""
    # ncc["GIA CÔNG (Y/N)"]=""
    # ncc["V/E U/CONG (Y/N)"]=""
    # ncc["DÁN VNR (Y/N)"]=""
    # ncc["K/L ĐB (Y/N)"]=""
    ncc=ncc.head(50)
    # A = ncc['TÊN NCC'].unique().tolist()
    # B= ncc['MÃ'].unique().tolist()
    return ncc
# ncc_list=ncc()

def push_lsx(df,gc):
    spreadsheet_key='1SHJmMVAo_9HgfTfzkDFIRw76-eLQPLDHZ3tOFj3ln5U'
    import gspread_dataframe as gd
    import gspread as gs
    ws1 = gc.open("DSX2.1 - Lệnh sản xuất").worksheet("1. LENH SX")
    existing1 = gd.get_as_dataframe(ws1)
    updated1 = existing1.append(df)
    gd.set_with_dataframe(ws1, df)
    # sheet_index_no1 = 0
    # sh = gc.open_by_key(spreadsheet_key)
    # worksheet1 = sh.get_worksheet(sheet_index_no1)
    # set_with_dataframe(worksheet1, df)
    ws2 = gc.open("LSX - lưu trữ").worksheet("Sheet1")
    existing2 = gd.get_as_dataframe(ws2)
    updated2 = existing2.append(df)
    gd.set_with_dataframe(ws2, updated2)


    st.success('Done')


def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'],
)
gc = gspread.authorize(credentials)


st.cache()
def form(df):
    list_r=df["LỆNH SX"].unique().tolist()
    c0,c1,c2,c3,c4,c5,c6=st.columns((1.8,1,.9,.9,.9,.9,.9))



    # list_r=[50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    with c0:
        lsx=[st.selectbox('LSX',list_r)]
        for nr in range(st.session_state.count):
            lsx.append(st.selectbox('',list_r[nr+1:], key=f'dfuestidn {nr}'))
        # st.selectbox('Lệnh sản xuất',['a','b','c'])
    with c1:

        nm=[st.selectbox('Nhà máy',['NM1','NM3','NM5'])]
        for nr in range(st.session_state.count):
            nm.append(st.selectbox('',['NM1','NM3','NM5'], key=f'dfquestidn {nr}'))
        # st.selectbox('Lệnh sản xuất',['a','b','c'])
    with c2:
        ldh=[st.radio('Loại đơn hàng',('C',"M"))]
        for nr in range(st.session_state.count):
            ldh.append(st.radio('Loại ĐH ',("C",'M'), key=f'dfquesatdidn {nr}'))  
    with c3:
        gc1=[st.radio('Gia công',("N","Y"))]
        for nr in range(st.session_state.count):
            gc1.append(st.radio('Gia công ',('N',"Y"), key=f'dfqudesưtdidn {nr}')) 
    with c4:
        uc=[st.radio('V/E uốn cong',("N","Y"))]
        for nr in range(st.session_state.count):
            uc.append(st.radio('V/e uốn cong ',('N',"Y"), key=f'dfqudesưtdidn{nr}')) 
    with c5:
        vn=[st.radio('Verneer',("N","Y"))]
        for nr in range(st.session_state.count):
            vn.append(st.radio('Verneer ',('N',"Y"), key=f'dfqudestưdidn {nr}')) 
    with c6:
        kl=[st.radio('Kim loại/HW',("N","Y"))]
        for nr in range(st.session_state.count):
            kl.append(st.radio('Kim loại ',('N',"Y"), key=f'dfqudestdidn1 {nr}')) 
    dict={"LỆNH SX":lsx,"NMSX":nm,"SẢN PHẨM (C/M)":ldh,"GIA CÔNG (Y/N)":gc1,"V/E U/CONG (Y/N)":uc,"DÁN VNR (Y/N)":vn,"K/L ĐB (Y/N)":kl}
    return dict
if 'count' not in st.session_state:
    st.session_state.count = 50
t1,t2,t3,t4,t5,t6=st.columns((1,1,1,1,1,1))
with t1:
    st.button('Thêm dòng', on_click=increment_counter,
        kwargs=dict(increment_value=5))

    with t3:
        st.write('Tổng số dòng = ', st.session_state.count+1)

df=pull_lsx(gc)
fi=st.selectbox('Chọn loại thao tác',['LSX mới','In lại LSX cũ'])
if fi=='LSX mới':

    dict=form(df)

    if st.button('Push'):
        dff=pd.DataFrame.from_dict(dict)
        # dff
        lsx_info=df.merge(dff,how='left',on="LỆNH SX")
        lsx_info
        # Pull order_info
        # lsx_info=pull_lsx(gc)
        # lsx_info=lsx_info[["LỆNH SX",	"TÊN KHÁCH HÀNG",	"TÊN SẢN PHẨM TTF",	"SỐ LƯỢNG",	"ĐVT",	"LOẠI GỖ",	"MÀU SƠN"	,"NỆM"	,"NGÀY XUẤT",	"GHI CHÚ"]]
        lsx_info=lsx_info[["LỆNH SX",	 "NMSX",	"SẢN PHẨM (C/M)",	"GIA CÔNG (Y/N)",	"V/E U/CONG (Y/N)",	"DÁN VNR (Y/N)",	"K/L ĐB (Y/N)",	"SỐ ĐƠN HÀNG",	"TÊN KHÁCH HÀNG",	"TÊN SẢN PHẨM TTF",	"LOẠI GỖ"	,"MÀU SƠN"	,"NỆM"	,"SỐ LƯỢNG",	"ĐVT",	"NGÀY XUẤT",	"GHI CHÚ"]]

        #push lsx_info
        push_lsx(lsx_info,gc)
else:
    st.info('Comming soon')



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
#         st.session_state.count = 0

#     def increment_counter(increment_value=0):
#         st.session_state.count += increment_value

#     def decrement_counter(decrement_value=0):
#         st.session_state.count -= decrement_value
    
#     c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
#     with c1:
#         st.button('Thêm dòng', on_click=increment_counter,
#             kwargs=dict(increment_value=1))
#     with c2:
#         st.button('Giảm dòng', on_click=decrement_counter,
#             kwargs=dict(decrement_value=1))
#     with c4:
#         st.write('Tổng số dòng = ', st.session_state.count+1)
#     h=st.session_state.count
#     with r1:
#         a=st.text_input('Dày',)


#     with r2:
#             b=[st.text_input('Rộng',)]
#             for nr in range(st.session_state.count):
#                 b.append(st.text_input(label='', key=f'2`1 {nr}'))
#     with r3:
#             c=[st.text_input('Dài',)]
#             for ng in range(st.session_state.count):
#                 c.append(st.text_input(label='', key=f'dfuestion {ng}'))
#     with r4:
#             d= [st.number_input('Số thanh',step=1)]
#             for ngg in range(st.session_state.count):
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
  


                
