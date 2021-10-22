# from typing_extensions import Concatenate
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
import barcode
from barcode.writer import ImageWriter
from cv import ncc_list

def qr_code(link="https://engineering.catholic.edu/eecs/index.html"):
        ean = barcode.get('code128', link, writer=ImageWriter())
        filename = ean.save('code128',{"module_width":0.2, "module_height":9, "font_size":14, "text_distance": 1, "quiet_zone": 1})
        return filename
def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value
st.subheader('Nhập thông tin:')

# st.set_page_config(layout='wide')
from list_info import qc_list,go_list

a2,a3,a4,a5=st.columns((1.5,1.5,1,1))
with a2:
    ncc=st.multiselect('NCC:',ncc_list)
with a3:
    qc=st.multiselect('QC kiểm:',qc_list)
with a4:
    go=st.multiselect('Loại gỗ:',go_list)
with a5:
    da=st.text_input('Độ ẩm:',)
if not ncc:
    st.info('Nhập đầy đủ thông tin ở phía trên')
else:
    st.subheader('Danh sách kiểm chi tiết:')
    mol1,mol2=st.columns(2)
    with mol1:
        st.subheader('KIỆN 1')
    with mol2:
        st.subheader('Kiện 2')
    list_r=[50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    r_1,r_2,r_3,r_4,r_5,r_6=st.columns((1,1,1,1,1,1))
    r1,r2,r3,r4,r5,r6=st.columns((1,1,2,1,1,2))
    if 'count' not in st.session_state:
        st.session_state.count = 0
    c1,c2,c3,c4,c5,c6=st.columns((1,1,1,1,1,1))
    with c1:
        st.button('Thêm dòng', on_click=increment_counter,
            kwargs=dict(increment_value=1))

    with c3:
        st.write('Tổng số dòng = ', st.session_state.count+1)
    h=st.session_state.count
        
    with r_1:
        a=st.text_input('Dày',)
    with r_4:
        dsfg=st.text_input('Dày2',)
    with r1:
            b=[st.selectbox('Rộng',list_r)]
            for nr in range(st.session_state.count):
                b.append(st.selectbox('',list_r[nr+1:], key=f'dfuestidn {nr}'))
    with r2:
            c=[st.text_input('Dài',)]
            for ng in range(st.session_state.count):
                c.append(st.text_input(label='', key=f'dfuestion {ng}'))
    with r3:
            d= [st.number_input('Số thanh',step=1)]
            for ngg in range(st.session_state.count):
                d.append(st.number_input(label='', key=f'Quđsesdfgtion {ngg}',step=  1))
    with r4:
            b=[st.selectbox('Rộng2',list_r)]
            for nr in range(st.session_state.count):
                b.append(st.selectbox('',list_r[nr+1:], key=f'dfuestdidn {nr}'))
    with r5:
            c=[st.text_input('Dài1',)]
            for ng in range(st.session_state.count):
                c.append(st.text_input(label='', key=f'dfuestsdion {ng}'))
    with r6:
            d= [st.number_input('Số thanh1',step=1)]
            for ngg in range(st.session_state.count):
                d.append(st.number_input(label='', key=f'Quesdfgsdtion {ngg}',step=  1))







































    # mol3,mol4=st.columns(2)
    # with mol3:
    #     st.subheader('KIỆN 3')
    # with mol4:
    #     st.subheader('Kiện 4')
    # r__1,r__2,r__3,r__4,r__5,r__6=st.columns((1,1,1,1,1,1))
    # k1,k2,k3,k4,k5,k6=st.columns((1,1,1,1,1,1))
    # if 'count' not in st.session_state:
    #     st.session_state.count = 0
    # c_1,c_2,c_3,c_4,c_5,c_6=st.columns((1,1,1,1,1,1))
    # with c_1:
    #     st.button('Thêm dòng2', on_click=increment_counter,
    #         kwargs=dict(increment_value=1))

    # with c_3:
    #     st.write('Tổng số dòng2 = ', st.session_state.count+1)
    # h=st.session_state.count
        
    # with r__1:
    #     a=st.text_input('Dày3',)
    # with r__4:
    #     a=st.text_input('Dày4',)
    # with k1:
    #         b=[st.text_input('Rộng2',)]
    #         for nr in range(st.session_state.count):
    #             b.append(st.text_input(label='', key=f'2`xv1 {nr}'))
    # with k2:
    #         c=[st.text_input('Dài2',)]
    #         for ng in range(st.session_state.count):
    #             c.append(st.text_input(label='', key=f'dfuesdftion {ng}'))
    # with k3:
    #         d= [st.number_input('Số thanh2',step=1)]
    #         for ngg in range(st.session_state.count):
    #             d.append(st.number_input(label='', key=f'Quđsesdfdfgtion {ngg}',step=  1))
    # with k4:
    #         b=[st.text_input('Rộng3',)]
    #         for nr in range(st.session_state.count):
    #             b.append(st.text_input(label='', key=f'2`sd1dsfsd {nr}'))
    # with k5:
    #         c=[st.text_input('Dài3',)]
    #         for ng in range(st.session_state.count):
    #             c.append(st.text_input(label='', key=f'dfuestsdddsfsdffion {ng}'))
    # with k6:
    #         d= [st.number_input('Số thanh3',step=1)]
    #         for ngg in range(st.session_state.count):
    #             d.append(st.number_input(label='', key=f'Quesdfgsddfsdftion {ngg}',step=  1))