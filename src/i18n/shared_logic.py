import os
import re
from functools import reduce

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_ss_worksheet():
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("SPREAD_SHEET_CREDENTIAL_FILE"), scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(os.getenv("SPREAD_SHEET_KEY")).sheet1
    return worksheet


def get_ja_text():
    data = open("i18n/resource/ja.txt")
    return reduce(lambda s, e: s + e, data, "")


def get_ja_words_with_quot():
    t = get_ja_text()
    return re.findall("[\"'`]*[一-龥ぁ-んァ-ヶー]+[\"'`]*", t)


def get_ja_words():
    t = get_ja_text()
    return re.findall("[一-龥ぁ-んァ-ヶー]+", t)
