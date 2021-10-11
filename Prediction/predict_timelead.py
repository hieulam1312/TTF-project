# Import Library
import streamlit as st
from datetime import datetime as dt #-> Để xử lý data dạng datetime

import gspread #-> Để update data lên Google Spreadsheet
import numpy as np
import pandas as pd #-> Để update data dạng bản
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from google.oauth2 import service_account




def collect_data():
    ## Collect QR scan database from Googlesheet
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'],
    )
    gc1 = gspread.authorize(credentials)
    spreadsheet_key = '1pMA3ZDjkL8gtIzQMyEkHwL_8-wDrXiO45OgtsPrkFec' # input SPREADSHEET_KEY HERE

    gc2=gspread.authorize(credentials)
    spreadsheet_key='1Kf79UeBTa0q2NAh4PaW2Y1nqE__S0wiSQSOkk2dkQm0'

    sh6=gc2.open("MẪU 2021 - COLLECT DATA").worksheet('XL+ SL')
    xl_sl=sh6.get_all_values()
    xl_sl_df=pd.DataFrame(xl_sl)
    xl_sl_df=xl_sl_df.replace("",np.nan)
    xl_sl_df.columns=xl_sl_df.iloc[0]
    xl_sl_df=xl_sl_df[1:]
    # xl_sl_df
    sh4=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('D.SÁCH')
    order_df=sh4.get_all_records()
    order_df=pd.DataFrame(order_df)
    order_df=order_df.replace("",np.nan)
    # order_df
    sh2=gc1.open("MẪU 2021 - COLLECT DATA").worksheet('TD')
    td_df=sh2.get_all_values()
    td_df=pd.DataFrame(td_df)
    td_df=td_df.replace("",np.nan)
    td_df=td_df.drop(columns=13,axis=0)
    td_df.columns=td_df.iloc[0]
    td_df=td_df[1:]
    # td_df

    sh3=gc1.open("MẪU 2021 - COLLECT DATA").worksheet('TD X4-NỆM')
    td_x4_df=sh3.get_all_values()
    td_x4_df=pd.DataFrame(td_x4_df)
    td_x4_df=td_x4_df.replace("",np.nan)
    td_x4_df.columns=td_x4_df.iloc[0]
    td_x4_df=td_x4_df[1:]
    # td_x4_df
    sh5=gc2.open('TTF - MẪU 2021 - TRIỂN KHAI').worksheet('T.DÕI')
    td_old_df=sh5.get_all_records()
    td_old_df=pd.DataFrame(td_old_df)
    td_old_df=td_old_df.replace("",np.nan)
    # td_old_df.columns=td_old_df.iloc[0].tolist()
    # td_old_df=td_old_df[1:]
    # td_old_df

    nm_df=td_df.loc[(td_df['NHÀ MÁY']!='X4')|(td_df['NHÀ MÁY']!='NM NỆM')]
    td_new_df=pd.concat([nm_df,td_x4_df])
    td_new_df=td_new_df[['SỐ ĐƠN HÀNG','BƯỚC','IN','OT','NHÀ MÁY','NMVLM','BỘ PHẬN','NGÀY GIẢI QUYẾT','NHÓM MẪU']]
    td_new_df=td_new_df.rename(columns={'IN': 'NGÀY NHẬN','OT':'NGÀY GIAO','NMVLM':'NVLM'})
    td_new_df['BƯỚC']=td_new_df['BƯỚC'].astype(float)

    # td_old_df.columns=td_old_df.columns.str.replace(" ","_")
    td_old_df['BƯỚC']=td_old_df['BƯỚC'].astype(float)
    td_old_df['NGÀY GIẢI QUYẾT']=td_old_df['NGÀY GIẢI QUYẾT'].astype(float)
    td_new_df['NGÀY GIẢI QUYẾT']=td_new_df['NGÀY GIẢI QUYẾT'].astype(float)
    td_all_df=pd.concat([td_old_df,td_new_df])
    # td_all_df


    td_all_df=td_all_df.replace('',np.nan)
    td_2021_df=td_all_df[td_all_df['SỐ ĐƠN HÀNG'].notnull()]
    # td_2021_df


    nvlm=td_all_df.copy()
    nvlm=nvlm[['SỐ ĐƠN HÀNG','NVLM']]
    nvlm_df=nvlm.drop_duplicates()
    nvlm_df=nvlm_df.dropna()
    nvlm_df['NVLM']=nvlm_df['NVLM'].astype(str)
    
    # xl_sl_df.columns=xl_sl_df.columns.str.replace(' ','_')
    xl=xl_sl_df.loc[xl_sl_df['THAO TÁC']==' Giao đơn hàng']
    xl_df=xl[['SỐ ĐH','XẾP LOẠI','SL THỰC TẾ']]
    xl_df['SỐ ĐH']=xl_df['SỐ ĐH'].astype(str)
    xl_df=xl_df.rename(columns={'SỐ ĐH':'SỐ ĐƠN HÀNG'})
    xl_df['XẾP LOẠI']=xl_df['XẾP LOẠI'].astype(str)
    # order_df
    order_df=order_df.drop(['BAO BÌ','GHI CHÚ','HÌNH ẢNH'], axis = 1)
    order_df['TÊN SẢN PHẨM']=order_df['TÊN SẢN PHẨM'].astype(str)
    order_df['SƠN']=order_df['SƠN'].astype(str)
    order_df['LOẠI SP']=order_df['LOẠI SP'].astype(str)
    order_df['NHÀ MÁY']=order_df['NHÀ MÁY'].astype(str)
    order_df['TÌNH TRẠNG']=order_df['TÌNH TRẠNG'].astype(str)
    order_df['NOTE']=order_df['NOTE'].astype(str)

    order_df['NV PKTH VẼ']=order_df['NV PKTH VẼ'].astype(str)
    # order_df
    new_order=order_df.merge(xl_df,how='left',on='SỐ ĐƠN HÀNG')
    new_order['XẾP LOẠI']=new_order['XẾP LOẠI'].astype(str)
    new_order['SL THỰC TẾ']=new_order['SL THỰC TẾ'].astype(float)

    order_2021_df=new_order.copy()
    # order_2021_df
    order_new=order_2021_df .merge(nvlm_df,how='left',on='SỐ ĐƠN HÀNG')
    # order_new
    order_new=order_new.replace(np.nan,0)
    order_new['NVLM']=order_new['NVLM'].astype(str)
    order_new['NGÀY GIAO']=pd.to_datetime(order_new['NGÀY GIAO'],dayfirst=True,errors='coerce')
    order_new['NGÀY LẬP']=pd.to_datetime(order_new['NGÀY LẬP'],dayfirst=True,errors='coerce')
    td_2021_df['NGÀY NHẬN']=pd.to_datetime(td_2021_df['NGÀY NHẬN'],dayfirst=True,errors='coerce')
    td_2021_df['NGÀY GIAO']=pd.to_datetime(td_2021_df['NGÀY GIAO'],dayfirst=True,errors='coerce')

    category=td_2021_df[['SỐ ĐƠN HÀNG','NHÓM MẪU']].dropna().drop_duplicates()

    return order_new,td_2021_df,category
def features(order_new,td_2021_df,category):
    order_new['SƠN'].unique()
    order_new['SƠN']=order_new['SƠN'].apply(lambda x: 0 if "KHÔNG" in x else 1)
    order_new['NỆM']=order_new['NỆM'].apply(lambda x: 0 if "KHÔNG" in x else 1)

    order_new=order_new[order_new['TÌNH TRẠNG']!="Ngừng"]

    info=order_new[['SỐ ĐƠN HÀNG', 'NGÀY LẬP', 'TÊN KHÁCH HÀNG',
            'NV PTM', 'GỖ', 'SƠN', 'NỆM','LOẠI SP',
        'NHÀ MÁY', 'NV PKTH VẼ', 'XẾP LOẠI', 'SL THỰC TẾ',
        'NVLM']]

    # replace_map2={'XẾP LOẠI':{'A+':7,'A':6,'B':5,'C':4,'D':3,'E':2,'F':1}}
    # category3= info['XẾP LOẠI'].astype('category').cat.categories.tolist()
    # _4 = {'XẾP LOẠI' : {k: v for k,v in zip(category3,list(range(1,len(category3)+1)))}}
    # info.replace(_4, inplace=True)

    date_out=td_2021_df[td_2021_df['BƯỚC']==10]
    date_out=date_out[['SỐ ĐƠN HÀNG','NGÀY GIAO']].drop_duplicates()
    info_df=info.merge(date_out,how='left',on='SỐ ĐƠN HÀNG')
    # info_df=info_df[info_df['SỐ ĐƠN HÀNG'].str.contains('M')]

    all_dataset=info_df.copy()
    all_dataset['NGÀY LẬP']=all_dataset['NGÀY LẬP'].apply(pd.to_datetime)
    all_dataset['NGÀY GIAO']=all_dataset['NGÀY GIAO'].apply(pd.to_datetime)
    all_dataset['SL THỰC TẾ']=all_dataset['SL THỰC TẾ'].astype(int)

    all_dataset_3=all_dataset[all_dataset['NGÀY LẬP'].dt.month>=3].sort_values(by='NGÀY LẬP',ascending=True).reset_index(drop=True)
    all_dataset=all_dataset_3.drop_duplicates()

    dict=[]
    for index,row in all_dataset.iterrows(): 
        row['TỒN BY ALL']=len(all_dataset[(all_dataset['NGÀY LẬP']<row['NGÀY LẬP'])&((all_dataset['NGÀY GIAO']>=row['NGÀY LẬP'])|(row['NGÀY GIAO'] is pd.NaT ))])
        row['TỒN BY NHÀ MÁY']=len(all_dataset[(all_dataset['NGÀY LẬP']<row['NGÀY LẬP'])&(all_dataset['NGÀY GIAO']>=row['NGÀY LẬP'])&(all_dataset['NHÀ MÁY']==row['NHÀ MÁY'])])
        dict.append(row)
    df=pd.DataFrame(dict)

    data=df.merge(category,how='left',on='SỐ ĐƠN HÀNG')

    holiday_dates = [pd.datetime(2021, 4, 30), pd.datetime(2021, 5, 1), pd.datetime(2011, 9, 1),
                    pd.datetime(2021, 4, 21), pd.datetime(2021, 9,2)]

    data['NGÀY_GIẢI_QUYẾT']=data.apply(lambda x: len(pd.bdate_range(x['NGÀY LẬP'],
                                                                    x['NGÀY GIAO'],holidays=holiday_dates,freq='C',
                                                                    weekmask = None)) if x.notnull().all() else np.nan, axis = 1)

    data['KIM LOẠI']=data['NHÓM MẪU'].apply(lambda x: 1 if "B1" in x or "B" in x else 0)

    data['VERNEER']=data['NHÓM MẪU'].apply(lambda x: 1 if "B2" in x or "B" in x else 0)

    a=data.copy()
    df=a[['SỐ ĐƠN HÀNG', 'NGÀY LẬP', 'TÊN KHÁCH HÀNG', 'NV PTM','SƠN',
        'NỆM',  'NHÀ MÁY','XẾP LOẠI', 'SL THỰC TẾ',
            'TỒN BY ALL', 'TỒN BY NHÀ MÁY', 'NHÓM MẪU',
            'KIM LOẠI', 'VERNEER','NGÀY_GIẢI_QUYẾT','NGÀY GIAO']]

    df=df.replace("",np.nan)
    df=df[(df['NHÀ MÁY'].isnull()==False)&(df['NHÓM MẪU']!='#N/A')]
    data_onehot = pd.get_dummies(df, columns=['NHÀ MÁY'], prefix = ['NHÀ MÁY'])
    data=data_onehot.copy()

    r={'B1':8,'B2':7,'B':9,'A':7,'C':6,'D':4}
    data['NHÓM MẪU']=[r[item] for item in  data['NHÓM MẪU']]
    return data
def predict_by_fac(train_df):
    train_df=train_df.drop(columns=['TỒN BY ALL'],axis=0)
    train_df=train_df[train_df['NGÀY_GIẢI_QUYẾT']<=train_df['NGÀY_GIẢI_QUYẾT'].quantile(0.95)]
    sns.histplot(train_df['NGÀY_GIẢI_QUYẾT'])

    from sklearn.preprocessing import MinMaxScaler
    min_max_scaler = MinMaxScaler()
    train_df[[ 'TỒN BY NHÀ MÁY', 'NHÓM MẪU','SL THỰC TẾ'	]] = min_max_scaler.fit_transform(train_df[['TỒN BY NHÀ MÁY', 'NHÓM MẪU','SL THỰC TẾ']])
    x = train_df.iloc[:,1:-1]
    y = train_df.iloc[:,-1]



    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.3,random_state=52)

    from sklearn.linear_model import LinearRegression
    reg=LinearRegression().fit(x_train,y_train)

    coef=pd.DataFrame([x_train.columns,reg.coef_]).T
    coef=coef.rename(columns={0:'Atributes',1:'Coefficients'})
    coef.sort_values('Coefficients')
    ytest_pred=reg.predict(x_test)

    from sklearn import metrics
    lin_acc=metrics.r2_score(ytest_pred,y_test)
    st.write('R^2: ',lin_acc)
    st.write('MAE: ',metrics.mean_absolute_error(ytest_pred,y_test))
    st.write('MSE: ',metrics.mean_squared_error(ytest_pred,y_test))
    st.write('RMSE: ',np.sqrt(metrics.mean_squared_error(ytest_pred,y_test)))
    st.write('Max Error: ',metrics.max_error(ytest_pred,y_test))
    fig, ax = plt.subplots()
    x_ax = range(len(x_test))
    plt.plot(x_ax, y_test, lw=1, color="blue", label="original")
    plt.plot(x_ax, ytest_pred, lw=0.8, color="red", label="predicted",marker="o", markersize=4)
    # plt.legend()
    plt.show()
    st.pyplot(fig)
    return reg

def predict_by_cus(train_df):
    train_df=train_df[['SỐ ĐƠN HÀNG',  'SƠN', 'NỆM',  'SL THỰC TẾ','TỒN BY ALL',
       'KIM LOẠI', 'VERNEER', 'NGÀY_GIẢI_QUYẾT']]
    train_df=train_df[train_df['NGÀY_GIẢI_QUYẾT']<=train_df['NGÀY_GIẢI_QUYẾT'].quantile(0.95)]
    from sklearn.preprocessing import MinMaxScaler
    min_max_scaler = MinMaxScaler()
    train_df[[ 'TỒN BY ALL','SL THỰC TẾ']] = min_max_scaler.fit_transform(train_df[['TỒN BY ALL','SL THỰC TẾ']])
    x = train_df.iloc[:,1:-1]
    y = train_df.iloc[:,-1]

    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.3,random_state=52)

    from sklearn.linear_model import LinearRegression
    reg=LinearRegression().fit(x_train,y_train)

    coef=pd.DataFrame([x_train.columns,reg.coef_]).T
    coef=coef.rename(columns={0:'Atributes',1:'Coefficients'})
    coef.sort_values('Coefficients')
    ytest_pred=reg.predict(x_test)

    from sklearn import metrics
    lin_acc=metrics.r2_score(ytest_pred,y_test)
    st.write('R^2: ',lin_acc)
    st.write('MAE: ',metrics.mean_absolute_error(ytest_pred,y_test))
    st.write('MSE: ',metrics.mean_squared_error(ytest_pred,y_test))
    st.write('RMSE: ',np.sqrt(metrics.mean_squared_error(ytest_pred,y_test)))
    st.write('Max Error: ',metrics.max_error(ytest_pred,y_test))
    st.set_option('deprecation.showPyplotGlobalUse', False)
    x_ax = range(len(x_test))
    plt.plot(x_ax, y_test, lw=1, color="blue", label="original")
    plt.plot(x_ax, ytest_pred, lw=0.8, color="red", label="predicted",marker="o", markersize=4)
    plt.legend()
    # plt.show()
    st.pyplot()
    return reg

def test_predict_customer(test_df,reg):
    test_df1=test_df[['NGÀY LẬP', 'SƠN', 'NỆM', 'SL THỰC TẾ', 
       'TỒN BY ALL',  'KIM LOẠI', 'VERNEER']]
    x_test=test_df1[[ 'SƠN', 'NỆM', 'SL THỰC TẾ', 
       'TỒN BY ALL',  'KIM LOẠI', 'VERNEER']]
    ytest_pred=reg.predict(x_test)
    test_df['NGÀY DỰ KIẾN']=ytest_pred.tolist()
    test_df=test_df[['NGÀY LẬP','NGÀY DỰ KIẾN']].reset_index(drop=True)
    test_df['DATE']=test_df['NGÀY LẬP'].astype('datetime64')+round(test_df['NGÀY DỰ KIẾN']).astype('timedelta64[D]')
    # df['new_date'] = df['orig_date'] + df['offset'].astype('timedelta64[D]'))
    return test_df

def test_predict_factory(test_df,reg):
    test_df1=test_df[['SỐ ĐƠN HÀNG','NGÀY LẬP', 'SƠN', 'NỆM', 'SL THỰC TẾ', 
        'TỒN BY NHÀ MÁY', 'NHÓM MẪU', 'KIM LOẠI', 'VERNEER',
        'NHÀ MÁY_NM NỆM', 'NHÀ MÁY_NM1', 'NHÀ MÁY_NM3', 'NHÀ MÁY_X4', 'NGÀY_GIẢI_QUYẾT']]
    x_test=test_df1.iloc[:,2:-1]
    x_test.head(2)

    from sklearn.preprocessing import MinMaxScaler
    min_max_scaler = MinMaxScaler()
    x_test[[ 'TỒN BY NHÀ MÁY', 'NHÓM MẪU','SL THỰC TẾ'	]] = min_max_scaler.fit_transform(x_test[['TỒN BY NHÀ MÁY', 'NHÓM MẪU','SL THỰC TẾ']])
    x_test.head(2)
    ytest_pred=reg.predict(x_test)

    test_df['NGÀY DỰ KIẾN']=ytest_pred.tolist()
    test_df=test_df[['SỐ ĐƠN HÀNG','TÊN KHÁCH HÀNG', 'NV PTM','NGÀY LẬP','NGÀY DỰ KIẾN']].reset_index(drop=True)
    test_df['DATE']=test_df['NGÀY LẬP']+round(test_df['NGÀY DỰ KIẾN']).astype('timedelta64[D]')
    # df['new_date'] = df['orig_date'] + df['offset'].astype('timedelta64[D]'))
    return test_df
list=collect_data()
order_new=list[0]
td_2021_df=list[1]
category=list[2]
data=features(order_new,td_2021_df,category)
train_df=data[data['NGÀY_GIẢI_QUYẾT'].isnull()==False]
train_df=train_df[['SỐ ĐƠN HÀNG',  'SƠN', 'NỆM',  'SL THỰC TẾ','TỒN BY ALL',
       'TỒN BY NHÀ MÁY', 'NHÓM MẪU', 'KIM LOẠI', 'VERNEER',
       'NHÀ MÁY_NM NỆM', 'NHÀ MÁY_NM1', 'NHÀ MÁY_NM3', 'NHÀ MÁY_X4', 'NGÀY_GIẢI_QUYẾT']]
# reg_fac=predict_by_fac(train_df)


a=st.sidebar.selectbox("Chọn",["predict by factory status",'predict by production info'])
if a=="predict by factory status":
    reg_fac=predict_by_fac(train_df)
    test_df=data[data['NGÀY_GIẢI_QUYẾT'].isnull()]
    test_df=test_df[['SỐ ĐƠN HÀNG','TÊN KHÁCH HÀNG', 'NV PTM', 'NGÀY LẬP', 'SƠN', 'NỆM', 'SL THỰC TẾ', 
        'TỒN BY NHÀ MÁY', 'NHÓM MẪU', 'KIM LOẠI', 'VERNEER',
        'NHÀ MÁY_NM NỆM', 'NHÀ MÁY_NM1', 'NHÀ MÁY_NM3', 'NHÀ MÁY_X4', 'NGÀY_GIẢI_QUYẾT']]
    predict_factory=test_predict_factory(test_df,reg_fac)
    predict_factory
    # cus=st.multiselect('Chọn khách hàng', predict_factory['TÊN KHÁCH HÀNG'].unique())
    # show=predict_factory[predict_factory['TÊN KHÁCH HÀNG'].isin(cus)]
    # show=show[['SỐ ĐƠN HÀNG', 'NV PTM','NGÀY LẬP','NGÀY DỰ KIẾN','DATE']]
    # show
if a=='predict by production info':
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        cus1=st.multiselect('NỆM:',['Có','Không'])
    with col2:
        cus2=st.multiselect('SƠN:',['Có','Không'])
    with col3:
        cus3=st.number_input('S/L:')
    with col4:
        cus4=st.multiselect('KIM LOẠI:',['Có','Không'])
    with col5:
         cus5=st.multiselect('VERNEER:',['Có','Không'])

    table_cus=pd.DataFrame({'NỆM':cus1,'SƠN':cus2,'SL THỰC TẾ':cus3,'KIM LOẠI':cus4,'VERNEER':cus5})
    table_cus['NGÀY LẬP']=pd.to_datetime("today").strftime("%m/%d/%Y")
    table_cus['TỒN BY ALL']=len(data[data['NGÀY GIAO'].isnull()])
    reg_cus=predict_by_cus(train_df)
    table_cus=table_cus.replace('Có',1)
    table_cus=table_cus.replace('Không',0)
    st.write(test_predict_customer(table_cus,reg_cus))

