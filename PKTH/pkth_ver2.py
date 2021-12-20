from abc import ABCMeta
# from typing_extensions import Concatenate
from pandas.core.reshape.concat import concat
from pyasn1_modules.rfc2459 import Name
import streamlit as st
import gspread_dataframe
import numpy as np
from numpy import histogram
from numpy.lib.function_base import append
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
import gspread
from google.oauth2 import service_account
import datetime
from gspread_dataframe import set_with_dataframe

st.set_page_config(layout='wide')


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
)
gc1 = gspread.authorize(credentials)
# spreadsheet_key = '1Kf79UeBTa0q2NAh4PaW2Y1nqE__S0wiSQSOkk2dkQm0'
def push_done(done,new_done):
    import gspread as gs
    import gspread_dataframe as gd
    from gspread_dataframe import set_with_dataframe

    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],)
    gc=gs.authorize(credentials)
    done11=gc.open('test').worksheet('Sheet3')

    new_done=new_done[new_done['ID_CV'].isin(done['ID_CV'].tolist())==False]
    df=done.append(new_done)

    gd.set_with_dataframe(done11,df)
def push_doing(doing):
    import gspread as gs
    import gspread_dataframe as gd
    from gspread_dataframe import set_with_dataframe
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],)
    gc=gs.authorize(credentials)
    done11=gc.open('test').worksheet('Sheet6')
    gd.set_with_dataframe(done11,doing)

def dataset(gc1):
    sh1=gc1.open("TTF - MẪU 2021 - TRIỂN KHAI").worksheet('D.SÁCH')
    sh11=sh1.get_all_records()
    dhm=pd.DataFrame(sh11)


    sh2=gc1.open('LSX - lưu trữ').worksheet('LSX ĐÃ IN')
    sh22=sh2.get_all_records()
    lsx=pd.DataFrame(sh22)
    lsx=lsx.astype(str)



    sh3=gc1.open('TTF - TRIỂN KHAI BẢN VẼ & BOM').worksheet('D.SÁCH')
    sh33=sh3.get_all_values()
    pyc=pd.DataFrame(sh33)
    pyc=pyc[3:]
    pyc.columns=pyc.iloc[0]
    pyc=pyc[4:]


    sh4=gc1.open('test').worksheet('Sheet3')
    sh44=sh4.get_all_records()
    done=pd.DataFrame(sh44)
    done1=done.astype(str)
    sh5=gc1.open('test').worksheet('Sheet6')
    sh45=sh5.get_all_records()
    done22=pd.DataFrame(sh45)
    done2=done22.astype(str)
    list_done=done1['ID_CV'].tolist()+done2['ID_CV'].tolist()
    # list_done
    dhm=dhm[['SỐ ĐƠN HÀNG', 'TÊN KHÁCH HÀNG','TÊN SẢN PHẨM', 'S/L', 'GỖ', 'NGÀY GIAO', 'GHI CHÚ', 'NHÀ MÁY']]
    dhm['LOẠI CV']='Đơn hàng mẫu'
    dhm=dhm.replace("",np.nan)
    dhm['SỐ ĐƠN HÀNG']=dhm['SỐ ĐƠN HÀNG'].dropna()
    dhm=dhm[dhm['SỐ ĐƠN HÀNG'].str.contains('TM')==False]
    dhm.columns=['ID_CV','TÊN KH','TÊN SẢN PHẨM','S/L','GỖ','NGÀY GIAO','GHI CHÚ','NHÀ MÁY','LOẠI CV']
 

    lsx=lsx[['LỆNH SX',"SỐ ĐƠN HÀNG",'TÊN KHÁCH HÀNG', 'TÊN SẢN PHẨM TTF','SỐ LƯỢNG', 'LOẠI GỖ',  'NGÀY XUẤT', 'GHI CHÚ', 'NMSX','SẢN PHẨM (C/M)']]
    lsx['LOẠI CV']='Lệnh SX'
    lsx.columns=['ID_CV',"SỐ ĐƠN HÀNG",'TÊN KH','TÊN SẢN PHẨM','S/L','GỖ','NGÀY GIAO','GHI CHÚ','NHÀ MÁY','LOẠI ĐH','LOẠI CV']


    sxnc=lsx[lsx['LOẠI ĐH']=='C']
    sxnc['LOẠI CV']='SXNC'
    sxmoi=lsx[lsx['LOẠI ĐH']=='M']
    sxmoi['LOẠI CV']='SX MỚI'


    pyc['TÊN SẢN PHẨM']=pyc['TÊN SP'] +" - "+pyc['NỘI DUNG YC']
    pyc2=pyc[['SỐ PHIẾU', 'TÊN KH',  'TÊN SẢN PHẨM',  'NGÀY YC GIAO','ƯU TIÊN','Ghi chú']]
    pyc2['LOẠI CV']='Phiếu Y/C'
    pyc2['S/L']=1
    pyc2['GỖ']=""
    pyc2.columns=['ID_CV','TÊN KH','TÊN SẢN PHẨM','NGÀY GIAO','ƯU TIÊN','GHI CHÚ','LOẠI CV','S/L','GỖ']



    BB=lsx[lsx['LOẠI ĐH']=='M']
    BB['LOẠI CV']='Bao bì mới'
    BB['ID_CV']=BB['ID_CV']+'.BB'

    ### combine data source
    df=dhm.append([sxnc,sxmoi,pyc2,BB])
    df=df.replace("",np.nan)
    df=df[df['ID_CV'].isnull()==False]
    df=df.drop(columns=['LOẠI ĐH','ƯU TIÊN'])

    return sxmoi,sxnc,dhm,BB,pyc2,list_done,done1





#Process item to created card into trello

#Call API Trello
import requests
import json
# import trello
from trello import TrelloClient
client = TrelloClient(
    api_key=st.secrets["api_key"],
    token=st.secrets["token"],
)
all_boards = client.list_boards()
my_board = all_boards[1]
my_lists = my_board.list_lists()
my_lists
get_lable=my_board.get_labels() 
dic={}
for lable in get_lable:
    dic[lable.name]=[lable.id,lable]
lable_table=pd.DataFrame.from_dict(dic,orient='index').reset_index()


# labledemo
#Created function to pull Trello
def add_card(dhn_demo,checklist,lable_table):
    dhn_demo=dhn_demo.rename(columns={'LOẠI CV':'index'})
    dhn_demo1=dhn_demo.merge(lable_table,how='left',on='index')
    labledemo=dhn_demo1[1].tolist()

    if checklist=="":

        dhm_list=(dhn_demo1['ID_CV']+'+'+dhn_demo1['TÊN SẢN PHẨM']).to_list()
        dhn_demo1=dhn_demo1.astype(str)
        dhm_name=(dhn_demo1['TÊN KH']+'\n'+dhn_demo1['TÊN SẢN PHẨM']+'\n'+dhn_demo1['S/L']+'\n'+dhn_demo1['GỖ']+'\n'+dhn_demo1['GHI CHÚ']).to_list()
        dhm_lable=dhn_demo1['index'].tolist()
        a=my_lists[0]   
        for i in dhm_list:
            n=a.add_card(i)
            n.set_description(str(dhm_name[dhm_list.index(i)]))
            n.add_label(labledemo[dhm_list.index(i)])
    else:
        list_order= dhn_demo['SỐ ĐƠN HÀNG'].unique().tolist()

        dhn_demo1=dhn_demo1.astype(str)
        
        a=my_lists[0]   
        for order in list_order:
            sxnc1=dhn_demo1[dhn_demo1['SỐ ĐƠN HÀNG'].str.contains(order)]
            n=a.add_card(order+"+")
            n.add_label(labledemo[list_order.index(order)])   
            n.add_checklist('Danh sách sản phẩm',checklist.get(order))   
    #  n.add_checklist(n,'list',['a','b','c'])
def add_lable(my_board,dhm_lable):
    color=['green','yellow','blue']
    for i in dhm_lable:
        my_board.add_label(i,color[dhm_lable.index(i)])

def literal_return(val):
    import csv,ast

    try:
        return ast.literal_eval(val)
    except ValueError:
        return (val)
#Pull data transecsiton
def pull(my_board,lable_table):
    dict1={}
    dict2={}
    dict3={}
    cards={}
    for lists in my_board.list_lists():
        my_list = my_board.get_list(lists.id)   
        for card in my_list.list_cards():
            # print(card)
            dict1[card]=[card.get_list().name,card.created_date,card.name,card.date_last_activity]
            # print(card.

            for cl in card.fetch_checklists():
                cards[card.name]=len(card.fetch_checklists()[0].items)
            dict2[card.name]=card.listCardMove_date()
            dict3[card]=card.idLabels
    a=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict2.items()]))
    b=a.transpose().reset_index()
    b=b.rename(columns={'index':'LSX'})

    SL=pd.DataFrame.from_dict(cards,orient='index').reset_index().rename(columns={'index':'TÊn',0:'S/L'})

    df_1=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict3.items()]))
    df_l=df_1.transpose().reset_index()

    df_lable=df_l.merge(lable_table,how='left',on=0)
    df_lable=df_lable.rename(columns={"index_x":"LSX",'index_y':'Lable'	})

    df_2=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict1.items()]))
    doing=df_2.transpose().reset_index()

    doing.columns=['LSX','Bộ phận hiện tại','Ngày tạo CV','TÊn','NGÀY NHẬN']
    doing=doing.merge(SL,how='left',on='TÊn')
    doing['S/L']=doing['S/L'].fillna(1)
    doing=doing.merge(df_lable,how='left',on='LSX').drop(columns={'LSX',0,1})
    doing[['ID_CV','TÊN SP']]=doing['TÊn'].astype(str).str.split('+',1, expand=True)

    doing_df=doing[doing['Bộ phận hiện tại']!='HOÀN THÀNH'].drop(columns={'TÊn'}).reset_index(drop=True)

    DONE=doing[doing['Bộ phận hiện tại']=='HOÀN THÀNH']
    DONE_ID=DONE['TÊn'].to_list()
    b=b[b['LSX'].isin(DONE_ID)].drop(columns={0})

    melt=b.melt(id_vars='LSX',value_name='History')
    melt=melt[melt['History'].isnull()!=True]
    melt['History']=melt['History'].apply(literal_return)
    d=melt.set_index(['LSX','variable']).apply(lambda x: x.apply(pd.Series).stack()).reset_index()
    e=d[['LSX',"variable",'level_2','History']]
    pivot=e.pivot(index=['LSX',"variable"],columns='level_2',values='History').reset_index()
    pivot=pivot[pivot[1]!='KÝ DUYỆT'][['LSX', 1, 2]]
    pivot.columns=['TÊn','Nhân viên','Thời gian nhận']

    done_df=DONE.merge(pivot,how='left',on='TÊn')[[ 'ID_CV','TÊN SP', 'S/L','Nhân viên', 'Ngày tạo CV', 'Thời gian nhận','NGÀY NHẬN', 'Lable']]
    done_df.columns=['ID_CV', 'TÊN SP', 'S/L', 'Nhân viên', 'Ngày tạo CV', 'Thời gian nhận','Ngày hoàn thành', 'Loại CV']

    return doing_df,done_df

st.subheader('MỚI')
# with st.form(key='abc'):

dhn_demo=dataset(gc1)
sxmoi,sxnc,dhm,BB,pyc,list_done,done=dhn_demo[0],dhn_demo[1],dhn_demo[2],dhn_demo[3],dhn_demo[4],dhn_demo[5],dhn_demo[6]
b=st.selectbox('Loại công việc',['SX MỚI','SXNC','Đơn hàng mẫu','Phiếu Y/C','Bao bì mới'])
def trello_df():
    if b=='SX MỚI':
        doing=sxmoi[(sxmoi['ID_CV'].isin(list_done)==False)&(sxmoi['LOẠI CV']=="SX MỚI")].reset_index(drop=True)
        list_id=""
    elif b=='Đơn hàng mẫu':
        doing=dhm[dhm['ID_CV'].isin(list_done)==False].reset_index(drop=True)
        list_id=""
    elif b=='Phiếu Y/C':
        doing=pyc[(pyc['ID_CV'].isin(list_done)==False)&(pyc['LOẠI CV']==b)].reset_index(drop=True)
        list_id=""
    elif b=='SXNC':
        doing=sxnc[(sxnc['ID_CV'].isin(list_done)==False)&(sxnc['LOẠI CV']==b)].reset_index(drop=True)
        list_order=doing['SỐ ĐƠN HÀNG'].unique().tolist()
        list_id={}
        for order in list_order:
            sxnc1=doing[doing['SỐ ĐƠN HÀNG'].str.contains(order)]
            list_id[order]=(sxnc1['ID_CV']+" | "+sxnc1['TÊN KH']+" | "+sxnc1['TÊN SẢN PHẨM']+" | "+sxnc1['S/L']+" | "+sxnc1['GỖ']).to_list()
    elif b=='Bao bì mới':
        doing=BB[(BB['ID_CV'].isin(list_done)==False)&(BB['LOẠI CV']==b)].reset_index(drop=True)
        list_order= doing['SỐ ĐƠN HÀNG'].unique().tolist()
        list_id={}
        for order in list_order:
            BB1=doing[doing['SỐ ĐƠN HÀNG'].str.contains(order)]
            list_id[order]=(BB1['ID_CV']+" | "+BB1['TÊN KH']+" | "+BB1['TÊN SẢN PHẨM']+" | "+BB1['S/L']+" | "+BB1['GỖ']).to_list()
    return doing,list_id
df=trello_df()
doing,list_id=df[0],df[1]
doing
if st.button('Xuất lên Trello'):        
    add_card(doing,list_id,lable_table)

if st.button('Xuất Tiến độ'):
    data_dff=pull(my_board,lable_table)

    push_done(done,data_dff[1])
    push_doing(data_dff[0])
