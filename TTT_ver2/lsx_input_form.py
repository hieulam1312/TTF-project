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

credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'],
)
gc = gspread.authorize(credentials)
def pull_lsx(gc):
    spreadsheet_key='1KBTVmlT5S2_x9VGseHdk_QDvZIfNBOLJy78lM0p3ORQ'

    sh=gc.open('Kho NVL - NCC').worksheet('Sheet1')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    # ncc
    # A = ncc['TÊN NCC'].unique().tolist()
    # B= ncc['MÃ'].unique().tolist()
    return ncc
# ncc_list=ncc()

def push_lsx(df,gc):
    spreadsheet_key='1C-KgsuTnMBb1vrAH6l6dRfYwPQLKAopL7swDD6ButIo'
    import gspread_dataframe as gd
    import gspread as gs
    ws = gc.open("LSX - send mail").worksheet("1. LENH SX")
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(df)
    gd.set_with_dataframe(ws, updated)
    st.success('Done')

# Pull order_info
lsx_info=pull_lsx(gc)
lsx_info
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
  


                
