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
import barcode
from barcode.writer import ImageWriter
from cv import ncc_list
from list_info import qc_list,go_list,in_list

def qr_code(link="https://engineering.catholic.edu/eecs/index.html"):
        ean = barcode.get('code128', link, writer=ImageWriter())
        filename = ean.save('code128',{"module_width":0.2, "module_height":6, "font_size":11, "text_distance": 1, "quiet_zone": 1})
        return filename

st.subheader('Nhập thông tin:')

# st.set_page_config(layout='wide')

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
        a=st.text_input('Dày',)


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

    
    b=["0" if v =="" else v for v in b]
    c=["0" if v =="" else v for v in c]
    d=["0 "if v =="" else v for v in d]


    b1=[]
    c1=[]
    a1=a.replace(',','.')

    for b_ in b:
        new_string = b_.replace(',','.')
        b1.append(new_string)
    for c_ in c:
        new_string = c_.replace(',','.')
        c1.append(new_string)

    if a=="0":
        st.info('Nhập đầy đủ thông tin vào form phía trên')
    else:  
        dict={'Rộng':b1,'Dài':c1,'Số thanh':d}
    
        import pandas as pd
        df=pd.DataFrame.from_dict(dict)    
        df=df.astype(float)
        df['Dày']=float(a1)
        df['SỐ KHỐI']=round((df['Dày']*df['Rộng']*df['Dài']*df['Số thanh'])/10**9,4)
        td=pd.to_datetime('today')
        df['NGÀY KIỂM']=td
        # df['THẺ KIỆN']=tk
        df['NCC']=ncc[0]
        df['LOẠI GỖ']=go[0]
        df['QC KIỂM']=qc[0]
        df['NGÀY KIỂM']=df['NGÀY KIỂM'].dt.date 

        total=round(sum(df['SỐ KHỐI']),4)
        d1=df.sort_index(ascending=False).reset_index(drop=True)      
        #Cân đối số liệu
        # _du=0
        st.subheader('Cân đối số liệu')
        cl1,cl2=st.columns(2)
        with cl1:
            ncc_num=st.number_input('Số khối NCC:',format="%.4f")
        with cl2: 
            st.write('**Tổng số khối thực kiểm:** ',total)
            
            _du=total-ncc_num
            # _du
            if _du>0.05:

                _row0=d1['Số thanh']
                new_row=round((_row0[0]*_du)/total,0)
                test=_row0[0]-new_row
                st.write('**Điều chỉnh số thanh mã cuối cùng thành:**',test)

        cls1,cls2,cls3=st.columns(3)
        with cls1:
            tk=st.number_input('Thẻ Kiện:',step=1)
        with cls2:
            ml=st.text_input('Mã lô:',)
        with cls3:
            clg=st.text_input('Chất lượng gỗ',)

        st.subheader('KẾT QUẢ:')

        c1,c2=st.columns(2)
        with c1:
            tk="K."+in_list[go_list.index(go[0])]+"."+str(tk)
            st.write('**Thẻ kiện:** ',tk)
            st.write('**Mã lô:** ',ml)
            NCC=ncc[0]+" "+"("+clg+")"
            st.write('**NCC:** ',NCC)
        df['THẺ KIỆN']=tk
        df['Mã lô']=ml
        # df['NCC']=NCC
        df['ĐỘ ẨM']=da
        # with c2:
        #    image= image=st.image(qr_code(link=tk))

        df2=df[['Dày','Rộng','Dài','Số thanh','SỐ KHỐI']]
        df2
        st.write('**Tổng số khối:** ',total)
   
    len=len(df.index.tolist())

    if len >20:
        df_20=df2.iloc[:19]
        # df_20
        df_o=df_20.copy()
        df_o=df_o.notnull()
        df_o=df_o.replace(True,0)
        # df_o
        df_ov=df2.iloc[20:].reset_index(drop=True)
        df_o.loc[df_ov.index, :] = df_ov[:]
        df_over=df_o.copy()
        # df_over
        # df_over=df_0.loc[df1.index, :] = df1[:]
        html = """ DANH SÁCH THẺ KIỆN\n
                <body> 
                <table  margin-bottom= "2000">     
                <tr>         
                <td>             
                <table  margin-bottom= "2000">                  
                <tr>                     
                <td>{0}<td> 
                <td>{1}</td>                 
                </tr>             
                </table>         
                </td>     
                </tr> 
                </table> 
                </body>
                    """.format(df_20.to_html(index=False,col_space=50),df_over.to_html(index=False,col_space=50))
    else:
        html = """ DANH SÁCH THẺ KIỆN\n
                <html>
                <br>
                <head></head>
                <body>
                    {0}
                    <br>
                </body>
                </html>
                """.format(df2.to_html(index=False,col_space=100,justify='center'))
def send_email(subject,total,tk,QC,NCC,qc,ml,td,html,receiver_list):
    # (1) Create the email head (sender, receiver, and subject)
    sender_email = st.secrets['SENDER_EMAIL']
    password = st.secrets['PWD_EMAIL']
    # receiver_email='hieulam1312@gmail.com'
    email = MIMEMultipart()
    email["From"] = sender_email
    # email["To"] = 'abc'
    email['Subject']=subject



    html3="""
    <html>
    Tổng số khối: <b>{}</b><br>
    QC kiểm: <b>{}</b><br>
    Mã lô: <b>{}</b><br>
    Ngày kiểm: <b>{}</b><br>

    </html>
    """.format(total,qc,ml,td)


   
    fp = open('code128.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', 'barcode')
    email.attach(msgImage)

    html4="""
    <html>
    Tổng số khối: <b>{}</b><br>
    </html>
    """.format(total)
    part1 = MIMEText(html, 'html')
    part2=MIMEText(html3,'html')
    part3=MIMEText(html4,'html')
    email.attach(part2)
    email.attach(part3)
    email.attach(part1)
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_email, password) #login with mail_id and password
    
        for receiver_email in receiver_list:
            email['To'] = receiver_email
            text = email.as_string()
            session.sendmail(sender_email, receiver_email, text)
        st.success('Đã gửi mail thành công')
        return(1)
    except:
        print("Could not send mail to {}".format(receiver_email))
        return(0)

def push(df):
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
    spreadsheet_key='1KBTVmlT5S2_x9VGseHdk_QDvZIfNBOLJy78lM0p3ORQ'

    sheet_index_no1=1

    sh = gc.open_by_key(spreadsheet_key)
    worksheet1 = sh.get_worksheet(sheet_index_no1)#-> 0 - first sheet, 1 - second sheet etc. 

    import gspread_dataframe as gd
    import gspread as gs

    ws = gc.open("Kho NVL - NCC").worksheet('Sheet2')
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(df)
    gd.set_with_dataframe(ws, updated)
    st.success('Tải lại trang để tiếp tục nhập liệu')
# from cv import push
list_email=['qlcl@tanthanhgroup.com','hieulam@tanthanhgroup.com']
if st.button('Hoàn tất'):
    send_email("Thẻ kiện: "+tk+" - "+NCC+" - "+qc[0],total,tk,qr_code(link=tk),NCC,qc[0],ml,td,html,list_email)
    push(df)
