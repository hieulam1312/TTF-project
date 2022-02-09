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
thaotac=st.selectbox('Chọn loại thao tác',['Nhập kho','Xuất kho'])


if not thaotac:
    st.info('Chọn loại thao tác để tiếp tục')
elif thaotac=='Nhập kho': 
    order_item=st.multiselect('Chọn đơn hàng',order_list)

    production= df[df['Đơn hàng'].isin(order_item)]

    pr=production['Tên vật tư'].tolist()
    sl=production['Số lượng'].tolist()
    dvt=production['ĐVT'].tolist()


    data=form(pr,sl,order_item,production)
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
    sanpham
    c3,c4=st.columns(2)
    with c3:
#         cd=st.multiselect('Xuất cho công đoạn:',['Lót PU','Lót PU trắng','Lót màu PU','Lót NC','Lót màu NC','Sơn màu PU','Bóng màu PU','Bóng màu NC'])
#     with c4:
        sl_sp=st.text_input('Cho số lượng ghế:',)
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
        st.write('Tổng số dòng: {}'.format(st.session_state.count ))
    h=st.session_state.count+4   
    with st.form(key='abc'):
        st.subheader('Bổ sung thêm các vật tư sau')
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
                b2.append(r2.text_input('Số lượng',key=f'dfuesidn {nr}'))
        st.form_submit_button('Hoàn tất')
        
        dic2={'Tên vật tư':b1,'Số lượng':b2}
        data2=pd.DataFrame.from_dict(dic2)

    if st.button('Hoàn tất xuất kho'):
        data=data2.copy()
        data['Tên Sản phẩm']=sanpham['TÊN SẢN PHẨM TTF'].tolist()[0]
        data['Nhà máy']=nm[0]
        data['Lệnh SX']=lsx[0]
#         data['Công đoạn']=cd[0]
        data['SL sản phẩm']=sl_sp
        data['Ngày xuất kho']=pd.to_datetime('today').date()
        data=data.astype(str)
        data
        # data1=data.drop(columns={'Ngày nhập kho','Đơn hàng'})   
        data1=data.copy()
        push(data1,gc,'Xuất kho')
        data2=data1[['Tên vật tư','Số lượng']]

        title_text ='TTF - Phiếu xuất kho ngày {}'.format(pd.to_datetime('today').date())
        subtitle_text = 'LSX: {} - Nhà máy: {}'.format(lsx[0],nm[0])
        annotation_text = 'Giám đốc nhà máy                                          Thủ kho sơn'
        sp='Tên sản phẩm: {} - số lượng ghế: {}'.format(sanpham['TÊN SẢN PHẨM TTF'].tolist()[0],sl_sp)
 
        footer_text = 'Ngày xuất {}'.format(pd.to_datetime('today').date())
        plt.figure(linewidth=1,
               
                tight_layout={'pad':1},
                # figsize=(5,4)
                )

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=data2.values,
                            rowLoc='right',
                            colLabels=data2.columns,
                            loc='center')

        # Scaling is the only influence we have over top and bottom cell padding.
        # Make the rows taller (i.e., make cell y scale larger).
        the_table.scale(1, 1.15)

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
                    size=9, style='italic',
                   
                )
        plt.figtext(0.1, 0.8,
                    sp,
                    horizontalalignment='left',
                    size=7,
                   
                )
        # Add footer
        # plt.figtext(0.95, 0.05, footer_text,
        #             horizontalalignment='right',
        #             size=6,
        #             weight='light',
                    
        #         )

        # Add annotation
        plt.figtext(0.5, 0.15,
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
