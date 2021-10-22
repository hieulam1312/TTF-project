from gspread.utils import A1_ADDR_ROW_COL_RE


def ncc():
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

    sh=gc.open('Kho NVL - NCC').worksheet('Sheet1')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    A = ncc['TÊN NCC'].unique().tolist()
    return A
ncc_list=ncc()
ncc_list