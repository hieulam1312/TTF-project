import datetime as dt
import pandas as pd
from pyasn1.debug import Scope
import streamlit as st
import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials

Cre=service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)

gc=gspread.authorize(Cre)

sheet1=gc.open("Kho sơn - DS đặt hàng").worksheet('Sheet1')

data=sheet1.get_all_records()
df=pd.DataFrame(data)
df

order_list=df['Đơn hàng'].unique().tolist()
order_item=st.multiselect('Chọn đơn hàng',order_list)
production= df[df['Đơn hàng'].isin(order_item)]
production
pr=production['Tên vật tư'].tolist()
sl=production['Số lượng'].tolist()
dvt=production['ĐVT'].tolist()
def form(ncc):
    with st.form(key='columns_in_form'):
        rowss=len(production['Đơn hàng'].tolist())
        if not ncc:
            st.info('Nhập đầy đủ thông tin ở phía trên')
        else:
            r1,r2,=st.columns(2)
            with r1:
                b1=[]
                for nr in range(rowss):
                    b1.append(r1.selectbox('Tên vật tư', [pr[nr]],key=f'dfuestidn {nr}'))

            with r2:
                b2=[]
                for nr in range (rowss):
                    b2.append(r2.text_input('Số lượng',sl[nr],key=f'dfuesidn {nr}'))
        st.form_submit_button('Nhập kho')
        dic={'Tên vật tư':b1,'Số lượng':b2}
        data=pd.DataFrame.from_dict(dic)
        data['Đơn hàng']=order_item[0]
        data['Ngày nhập kho']=pd.to_datetime('today').date()
        return data
data=form(order_item)
data