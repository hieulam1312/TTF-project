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
def qr_code(link="https://engineering.catholic.edu/eecs/index.html"):
        ean = barcode.get('code128', link, writer=ImageWriter())
        filename = ean.save('code128',{"module_width":0.2, "module_height":9, "font_size":14, "text_distance": 1, "quiet_zone": 1})
        return filename




# st.set_page_config(layout='wide')
from list_info import ncc_list,qc_list,go_list

a2,a3,a4,a5=st.columns((1.5,1.5,1,1))
with a2:
    ncc=st.multiselect('NCC:',ncc_list)
with a3:
    qc=st.multiselect('QC kiểm:',qc_list)
with a4:
    go=st.multiselect('Loại gỗ:',go_list)


st.subheader('Danh sách kiểm chi tiết:')

r1,r2,r3,r4,r5=st.columns((1,1,1,2,2))
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
    
with r1:
        a=[st.text_input('Dày',)]
        for n in range(st.session_state.count):
            a.append(st.text_input(label='', key=f'Question {n}'))
with r2:
        b=[st.text_input('Rộng',)]
        for nr in range(st.session_state.count):
            b.append(st.text_input(label='', key=f'2`1 {nr}'))
with r3:
        c=[st.text_input('Dài',)]
        for ng in range(st.session_state.count):
            c.append(st.text_input(label='', key=f'dfuestion {ng}'))
with r4:
        d= [st.number_input('Số thanh',step=1)]
        for ngg in range(st.session_state.count):
            d.append(st.number_input(label='', key=f'Quesdfgtion {ngg}',step=  1))

a=[0 if v =="" else v for v in a]
b=[0 if v =="" else v for v in b]
c=[0 if v =="" else v for v in c]
d=[0 if v =="" else v for v in d]

a1 = []
b1=[]
c1=[]


for a_ in a:
    new_string = a_.replace(',','.')
    a1.append(new_string)

for b_ in b:
    new_string = b_.replace('.',',')
    b1.append(new_string)
for c_ in c:
    new_string = c_.replace('.',',')
    c1.append(new_string)

if a1[0]==0:
    st.info('Nhập đầy đủ thông tin vào form phía trên')
else:
    with r5: 
        g=[]
        hh=[]
        st.markdown("")
        g=[st.write("Số lượng:\n",d[0])]
        hh=[st.write('Số khối',round((float(a1[0])*float(b1[0])*float(c1[0])*float(d[0]))/10**9,4))]
        st.markdown("")


        for nr in range(1,st.session_state.count+1):
            if not a1[nr]:
                g.append(st.write("Số lượng:\n",d[nr]))
                st.write('Số khối',0)
                st.markdown("")


            elif a1[nr]:   
                g.append(st.write("Số lượng:\n",d[nr]))
                hh.append(st.write('Số khối',(round((float(a1[nr])*float(b1[nr])*float(c1[nr])*d[nr])/10**9,4))))
                st.markdown("")
    cl1,cl2=st.columns(2)
    with cl1:
        tk=st.text_input('Thẻ Kiện:',)
    dict={'Dày':a1,'Rộng':b1,'Dài':c1,'Số thanh':d}
    import pandas as pd
    df=pd.DataFrame.from_dict(dict)    
    df=df.astype(float)
    df['SỐ KHỐI']=round((df['Dày']*df['Rộng']*df['Dài']*df['Số thanh'])/10**9,4)
    df['NGÀY KIỂM']=pd.to_datetime('today')
    df['THẺ KIỆN']=tk
    df['NCC']=ncc[0]
    df['LOẠI GỖ']=go[0]
    df['QC KIỂM']=qc[0]
    st.subheader('KẾT QUẢ:')
    # st.write('Thẻ kiện: ',tk)
    # st.write('NCC:',ncc[0])
    # st.write('Gỗ:',go[0])
    # st.write('QC kiểm: ',qc[0])
    total=round(sum(df['SỐ KHỐI']),4)
    c1,c2=st.columns(2)
    with c1:
        st.write('**Thẻ kiện:** ',tk)
    # with c2:
    #    image= image=st.image(qr_code(link=tk))
    st.write('**Tổng số khối:** ',total)
    df





def send_email(subject,total,tk,filename):
    # (1) Create the email head (sender, receiver, and subject)
    sender_email = st.secrets['SENDER_EMAIL']
    password = st.secrets['PWD_EMAIL']
    receiver_email='hieulam1312@gmail.com'
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = 'abc'
    email['Subject']=subject

    # (2) Create Body part
    html2 = """
    <html>
     <br>
    Email được gửi vào lúc at <b>{}</b><br>
    </html>
    """.format(dt.datetime.now().isoformat())

    # part4 = MIMEText(html2, 'html')


    html3="""
    <html>
    <br>
    Thẻ kiện:  <b>{}</b><br>
     <br>
    Tổng số khối: <b>{}</b><br>
    <br>

    </html>
    """.format(tk,total)

    html = """ DANH SÁCH THẺ KIỆN\n
            <html>
             <br>
            <head></head>
            <body>
                {0}
                 <br>
            </body>
            </html>
            """.format(df.to_html(index=False,col_space=100,justify='center'))
    fp = open('code128.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', 'barcode')
    email.attach(msgImage)

    part1 = MIMEText(html, 'html')
    part2=MIMEText(html3,'html')
    email.attach(part2)
    email.attach(part1)

    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_email, password) #login with mail_id and password
    text = email.as_string()
    session.sendmail(sender_email, receiver_email, text)
    st.success('Đã gửi mail thành công')


if st.button('Hoàn tất'):
    send_email("Thẻ kiện - "+tk+" - "+ncc[0]+" - "+qc[0],total,tk,qr_code(link=tk))
    
