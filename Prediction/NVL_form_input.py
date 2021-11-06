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
# import cv
# from cvcv import ncc_f
from ncc import ncc_list
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
# list_ncc
list_ncc = ncc_list['TÊN NCC'].unique().tolist()
list_int= ncc_list['MÃ'].unique().tolist()
# cv.ncc_f()
