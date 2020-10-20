import datetime
import re
import sys

import requests

import base64_file

TOP_URL = 'https://www.e-kakushin.com/login/'
COMPANY_NO = '' # 企業コード
USER_ID = '' # ユーザーID

STOP_WORD = '報告可能な災害がないため、現在この機能はご利用できません。'

NAME_TUPLE = (
    'org.apache.struts.taglib.html.TOKEN',
    'menuKbn',
    'subMenuKbn',
    'actionEvent',
    'language',
    'saigaiCd2',
    'anotherFlg',
    'gpsUpdFlg',
    'gpsFlg',
    'lat',
    'lon',
    'jdgSanshoFlg',
    'ecCd',
    'saigaiBean.knkySanshSybt',
    'saigaiJykyBean.ekakCstmrCd',
    'saigaiJykyBean.saigaiCd',
    'saigaiJykyBean.usrCd',
    'saigaiJykyBean.mltLangUseFlg',
    'saigaiList[0].saigaiCd',
    'saigaiList[0].saigaiNm',
    'saigaiList[0].anpSosnSybtKbn',
    'saigaiList[0].jdgSanshoFlg',
    'saigaiList[0].knkySanshSybt',
    'saigaiList[0].answrKbn',
    'saigaiList[0].jdgSelectFlg',
    'saigaiList[0].hssiYmdHms',
    'saigaiList[0].insDt',
    'taiUsrBean.usrCd',
    'taiUsrBean.usrNm',
    'taiUsrBean.orgCd',
    'taiUsrBean.orgNm',
    'saigaiJykyBean.cmntAriFlg',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoTgetNmBr',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].inpFomKbn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].hyjiFomKbn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].hisuFlg',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].jdgSelectFlg',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[0].outoJykyNmBr',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].outoJykyRrkiList[1].outoJykyNmBr',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoTgetNmBr',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].inpFomKbn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].hyjiFomKbn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].hisuFlg',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].jdgSelectFlg',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[0].outoJykyNmBr',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNm',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmEng',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmCn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmTw',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmVn',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmNp',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmPt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].outoJykyRrkiList[1].outoJykyNmBr',
    'saigaiCd',
    'saigaiJykyBean.answrDt',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].saigaiJykyKndCd',
    'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].saigaiJykyKndCd',
    'saigaiJykyBean.jykyDtl',
)


def search_input_name(name, line: str) -> dict:
    result = {}
    if '<input type="hidden" name="'+name+'"' in line:
        search_word = name.replace(r'[', r'\[').replace(r']', r'\]')
        m = re.match(r'.*<input type="hidden" name="'+search_word+r'" value="([^"]*)">.*?', line.strip())
        if m:
            value = m.group(1)
            if value == '':
                value = None
            result = {name: value}
        else:
            result = {name: None}
    return result


def print_with_time(string: str):
    print(datetime.datetime.now(), string)

def exit_with_time(string: str):
    sys.exit(str(datetime.datetime.now()) + ' ' + string)


if __name__ == '__main__':
    if not base64_file.exist_password_file():
        exit_with_time('パスワードファイルを作成してください')

    session = requests.session()

    BASE_URL = 'https://www2'
    # res = session.get(TOP_URL)
    # res.encoding = res.apparent_encoding
    # res.raise_for_status()
    # for line in res.text.splitlines():
    #     if 'e-kakushin.com/emember/servicetop.do' in line:
    #         m = re.match(r'<a href="(https://www[0-9]?)\.e-kakushin\.com.*', line.strip())
    #         if m:
    #             BASE_URL = m.group(1)
    # if BASE_URL == '':
    #     exit_with_time('BASE_URLが取得できませんでした')

    TOKEN_URL = BASE_URL + '.e-kakushin.com/emember/servicetop.do'
    LOGIN_URL = BASE_URL + '.e-kakushin.com/emember/docroot/realm/login'
    REPORT_URL = BASE_URL + '.e-kakushin.com/eanpi/disaster/UsrVnRegistSafety.do'

    # トップページ取得
    res = session.get(TOKEN_URL)
    res.encoding = res.apparent_encoding
    res.raise_for_status()

    # ログイン用TOKEN抽出
    TOKEN = ''
    for line in res.text.splitlines():
        if 'org.apache.struts.taglib.html.TOKEN' in line:
            m = re.match(r'<input type="hidden" name="org.apache.struts.taglib.html.TOKEN" value="([^"]+)" />', line.strip())
            if m:
                TOKEN = m.group(1)

    if TOKEN == '':
        exit_with_time('TOKENが取得できませんでした')

    # ログイン情報
    login_info = {
        'customerCodeAlias': COMPANY_NO,
        'userCodeAlias': USER_ID,
        'password': base64_file.get_password(),
        'actionEvent': 'loginEvent',
        'org.apache.struts.taglib.html.TOKEN': TOKEN,
    }

    # ログイン
    res = session.post(LOGIN_URL, data=login_info)
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    del login_info

    # 報告用ページ取得
    res = session.get(REPORT_URL)
    res.encoding = res.apparent_encoding
    res.raise_for_status()

    # 報告用情報抽出
    report_info = {}
    report_info_update = { # 上書きの必要があるものを指定
        'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[0].saigaiJykyKndCd': '01',
        'saigaiJykyBean.outoRrkiBean.outoTgetRrkiList[1].saigaiJykyKndCd': '01',
        'saigaiJykyBean.jykyDtl': None,
        'actionEvent': 'report',
    }
    for line in res.text.splitlines():
        if STOP_WORD in line:
            exit_with_time('報告可能な災害がありません')
        for v in NAME_TUPLE:
            report_info.update(search_input_name(v, line))
    report_info.update(report_info_update) # 値を上書き

    if 'saigaiJykyBean.answrDt' in report_info:
        exit_with_time('既に報告済みです')

    # 報告処理
    res = session.post(REPORT_URL, data=report_info)
    res.encoding = res.apparent_encoding
    res.raise_for_status()

    if '報告が完了しました。' in res.text:
        print_with_time('報告が完了しました')
    else:
        print_with_time('報告に失敗しました')
