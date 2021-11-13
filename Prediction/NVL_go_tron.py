# from typing_extensions import Concatenate
import numpy as np
from logging import error
from mimetypes import MimeTypes
import streamlit as st
import email, smtplib, ssl # to automate email
import email as mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime as dt # to work with date, time
from bs4 import BeautifulSoup # to work with web scrapping (HTML)
import pandas as pd # to work with tables (DataFrames) data
from IPython.core.display import HTML
from streamlit.elements import multiselect # to display HTML in the notebook
import PIL
# import barcode
# from barcode.writer import ImageWriter
# import cv
st.set_page_config(layout='wide')

# from cvcv import ncc_f
from ncc import abv
from list_info import qc_list
go_list=["ALDER",
"ASH VN",
"ASH",
"BẠCH ĐÀN",
"BEECH",
"CĂM XE",
"CAO SU ĐEN",
"CAO SU",
"CHERRY",
"CHÒ CHỈ",
"SYCAMORE",
"DỪA",
"DƯƠNG LIỄU",
"GÒN",
"HICKORY",
"KAPUS",
"LÒNG MỨT",
"MAPLE",
"MÍT",
"MUỒNG",
"NEP PALLET",
"OAK",
"PƠ MU",
"POPLAR",
"RED ELM",
"RED OAK",
"SỌ KHỈ",
"TẠP",
"TEAK",
"THÔNG",
"TRÀM",
"TRÅU",
"WALNUT",
"WHITE OAK",
"WHITE POPLAR",
"WILLOW",
"XOÀI"
]
in_list=["ADL","ASV","ASH","BDA","BEE","CXE","CSD","CSU","CHE","CCI","SYC","DUA","DLI","GON","HIC","KAP","LMU","MAP","MIT","MNG","NPL","OAK","PMU","PLR","REL","ROK","SOK","TAP","TEK","THO","TRM","TRU","WAL","WOK","WPR","WIL","XOA"]
# abv
list_ncc = abv[0]

list_int= abv[1]
# cv.ncc_f()
# def increment_counter(increment_value=0):
#     rowss += increment_value

# def decrement_counter(decrement_value=0):
#     rowss -= decrement_value

st.subheader('Nhập thông tin:')
a2,a3,a4,a5=st.columns((1.5,1.5,1,1))
with a2:
    ncc=st.multiselect('NCC:',list_ncc)
with a3:
    qc=st.multiselect('QC kiểm:',qc_list)
with a4:
    go=st.multiselect('Loại gỗ:',go_list)
with a5:
    da=st.text_input('Độ ẩm:',)
cls1,cls2,cls3,cls4=st.columns(4)
# with cls1:
#     tk=st.number_input('Thẻ Kiện:',step=1)
with cls2:
    ml=st.text_input('MÃ LÔ:',)
with cls3:
    clg=st.text_input('Chất lượng gỗ',)
with cls4:
    ngaykiem=st.text_input('Ngày kiểm',)
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value

c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
with c1:
    st.button('Thêm dòng', on_click=increment_counter,
        kwargs=dict(increment_value=1))
with c2:
    st.button('Giảm dòng', on_click=decrement_counter,
        kwargs=dict(decrement_value=1))
with c4:
    st.write('Tổng số dòng = ', st.session_state.count+1)
h=st.session_state.count


def form(ncc):
    with st.form(key='columns_in_form'):
        rowss=60
        if not ncc:
            st.info('Nhập đầy đủ thông tin ở phía trên')
        else:
            st.subheader('Danh sách kiểm chi tiết:')
            mol1,mol2=st.columns(2)
            with mol1:
                mol1.subheader('KIỆN 1')


            r_1,r_2,r_3,t1_,r_4=st.columns((1,1,1,1,3))
            r1,r2,r3,r4=st.columns((1,1,2,3))
              
            with r_1:
                a1=r_1.text_input('Dày',)
            with r_2:
                tk1=r_2.text_input('Thẻ kiện',)
            with r_3:
                st.form_submit_button('Kiểm tra số khối')

            with r1:
                b1=[]
                for nr in range(rowss):
                    b1.append(r1.text_input('Rộng', key=f'df1uestidn {nr}'))
            with r2:
                    c1=[]
                    for ng in range(rowss):
                        c1.append(r2.text_input(label='Dài', key=f'df1uestion {ng}'))
            with r3:
                    d1= []
                    for ngg in range(rowss):
                        d1.append(r3.text_input(label='Số thanh', key=f'Quđsesdf1gtion {ngg}'))
            
            tk1="-" if tk1 =="" else tk1
            a1="0" if a1 =="" else a1
            b1=["0" if v =="" else v for v in b1]
            c1=["0" if v =="" else v for v in c1]
            d1=["0" if v =="" else v for v in d1]
            dict1={'MÃ THẺ KIỆN':tk1,'QC Dày':a1,'QC Rộng':b1,'QC Dài':c1,'Số thanh':d1}
            df1=pd.DataFrame.from_dict(dict1)    
            df1=df1.astype({'QC Rộng':float,'QC Dài':float,'QC Dày':float,'Số thanh':int,'MÃ THẺ KIỆN':str})
            khoi=df1['QC Dày']*df1['QC Rộng']*df1['QC Dài']*df1['Số thanh']
            df1['MÃ THẺ KIỆN']="K."+in_list[go_list.index(go[0])]+"."+df1['MÃ THẺ KIỆN'].astype(str)
            df1=df1[df1['Số thanh']>0]
            df1['KHỐI LƯỢNG']=round(khoi/10**9,4)
            td=pd.to_datetime('today')
            df1['NGÀY NHẬP LIỆU']=td
            # df1['THẺ KIỆN']=tk
            df1['NCC']=ncc[0]
            df1['LOẠI GỖ']=go[0]
            df1['NGƯỜI KIỂM']=qc[0]
            df1['NGÀY NHẬP LIỆU']=df1['NGÀY NHẬP LIỆU'].dt.date 
            NCC=ncc[0]+" "+"("+clg+")"
            df1['NCC']=  NCC
            df1['MÃ LÔ']=ml
            # df['NCC']=NCC
            df1['ĐỘ ẨM']=da
            df1["NGÀY KIỂM"]=ngaykiem
            total=round(sum(df1['KHỐI LƯỢNG']),4)
            d1=df1.sort_index(ascending=False).reset_index(drop=True) 
            with r4:
                df2=df1.groupby(['MÃ THẺ KIỆN','QC Dài']).agg({'KHỐI LƯỢNG':'sum'}).reset_index()
                df2
            return df1
data=form(ncc)
# data
ncc_index=list_ncc.index(ncc[0])
ini=list_int[ncc_index]
def eccount(df,ini):
    df4=df.copy()
#     df4
    uni_tk=df4["MÃ THẺ KIỆN"].unique().tolist()
    uni_dai=df4['QC Dài'].unique().tolist()
#     uni_dai

    # uni_dai=uni_dai.sort()
#     uni_dai
    if len(uni_dai)==2:
        string_dai=str(int(uni_dai[0]))+"/"+str(int(uni_dai[-1]))
    elif len(uni_dai)==1:
        string_dai=str(int(uni_dai[0]))
    else:
        string_dai=str(int(uni_dai[0]))+"-"+str(int(uni_dai[-1]))
#     string_dai
    df4['QC Dài 2']=string_dai
    df4["MÃ THẺ KIỆN2"]=df4["MÃ THẺ KIỆN"]
    df4["MÃ THẺ KIỆN3"]=df4["MÃ THẺ KIỆN"]
    df4['QC Dày2']=df['QC Dày']
    df4["ncc"]=ini
    df4['Loại Gỗ']=in_list[go_list.index(go[0])]

    eccount=df4[["MÃ THẺ KIỆN","MÃ THẺ KIỆN2","MÃ THẺ KIỆN3",'QC Dày','QC Dài 2','MÃ LÔ','Loại Gỗ','QC Dày2','ncc','KHỐI LƯỢNG']]

    eccount_gr=eccount.groupby(["MÃ THẺ KIỆN","MÃ THẺ KIỆN2","MÃ THẺ KIỆN3",'QC Dày','QC Dài 2','MÃ LÔ','Loại Gỗ','QC Dày2','ncc'])['KHỐI LƯỢNG'].sum().reset_index()
    eccount_gr['Tỉ lệ']=1
    eccount_gr['Đơn vị']="m3"
    eccount_gr['Giá mua']=round(eccount_gr['Tỉ lệ']/eccount_gr["KHỐI LƯỢNG"],6)
    eccount_gr['Giá mua2']=0
    eccount_gr['Giá bán']=eccount_gr['Giá mua']
    eccount_gr['Giá bán2']=0
    eccount_gr['Ecount']="Ecount"
#     eccount_gr
    return eccount_gr

def push(df,str):
    import streamlit as st
    import pandas as pd
    from google.oauth2 import service_account
    import gspread #-> Để update data lên Google Spreadsheet
    from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
    from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
    )
    gc = gspread.authorize(credentials)
    spreadsheet_key='1_ZhSbjL2EfbyTLyWCpTrHJi6kCku1j0eVwQ_g1R2QTM'

    import gspread_dataframe as gd
    import gspread as gs

    ws = gc.open("TTF - Nhập liệu gỗ tròn").worksheet(str)
    existing = gd.get_as_dataframe(ws)
    # existing
    updated = existing.append(df)
    gd.set_with_dataframe(ws, updated)
    st.success('Tải lại trang để tiếp tục nhập liệu')



list_email=['qlcl@tanthanhgroup.com','ttf.qcgo@gmail.com']
with c5:
    if st.button('Xuất danh sách'):
        # send_email("Thẻ kiện: "+tk+" - "+NCC+" - "+qc[0],total,tk,qr_code(link=tk),NCC,qc[0],ml,td,html,list_email)
        sheet='3. DS NHẬP ECOUNT'
        # from cv import push
        ECC=eccount(data,ini)
        push(ECC,sheet)
        data['MÃ THẺ KIỆN_2']=data['MÃ THẺ KIỆN'].str.replace('K','T')
        # data
        data=data[['MÃ THẺ KIỆN_2',"MÃ THẺ KIỆN","NGÀY NHẬP LIỆU","NGÀY KIỂM",	"NGƯỜI KIỂM",	"NCC",	"LOẠI GỖ",	"QC Dày",	"QC Rộng","QC Dài",	"Số thanh",	 "KHỐI LƯỢNG", 	"MÃ LÔ",'ĐỘ ẨM']]
        data=data[data["QC Dài"]>0]
        data
        push(data,'1. NHẬP LIỆU')

