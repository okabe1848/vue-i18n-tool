# -*- coding: utf-8 -*-
import json
import os
from typing import List

import requests

from i18n.constants import READ_COL_I18N, READ_ROW_STARTING, READ_COL_EN, READ_COL_JA
from i18n.shared_logic import get_ss_worksheet


class InvalidI18nDataException(Exception):
    def __init__(self, message):
        self.message = message

    class Code:
        NO_TARGETS = "NO_TARGETS"
        DUPLICATED_I18N_CODE = "DUPLICATED_I18N_CODE"
        EXISTS_ALREADY = "EXISTS_ALREADY"


def get_targets() -> List:
    worksheet = get_ss_worksheet()
    res = []
    for row in range(READ_ROW_STARTING, 100):
        i18n = worksheet.acell(f"{READ_COL_I18N}{row}").value
        if not i18n:
            break
        ja = worksheet.acell(f"{READ_COL_JA}{row}").value
        en = worksheet.acell(f"{READ_COL_EN}{row}").value
        res.append({"i18n": i18n, "ja": ja, "en": en})
    print(f"### get_targets={get_targets}")
    return res
    # return [
    #     {"i18n": "okabe_test100", "ja": "岡部テスト02", "en": "Okabe Test 02"},
    #     {"i18n": "okabe_test200", "ja": "岡部テスト03", "en": "Okabe Test 03"},
    # ]


def assert_targets(targets: List):
    if not targets or len(targets) < 1:
        raise InvalidI18nDataException(InvalidI18nDataException.Code.NO_TARGETS)

    i18n_set = set([e.get('i18n') for e in targets])
    if len(i18n_set) != len(targets):
        raise InvalidI18nDataException(InvalidI18nDataException.Code.DUPLICATED_I18N_CODE)

    for target in targets:
        exists = __lookup_dict_code(target.get("i18n"))
        if exists:
            raise InvalidI18nDataException(InvalidI18nDataException.Code.EXISTS_ALREADY)


def __lookup_dict_code(input_code: str) -> bool:
    url = os.getenv("DICTIONARY_API_LOOKUP_URL")
    headers = {'x-api-key': os.getenv("DICTIONARY_API_KEY"), 'Content-Type': 'application/json'}
    payload = {
        'inputCode': f"{input_code}"
    }
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return True if res.status_code == 500 or '{\"message\":true}' in res.text else False


def __register_dictionary(targets: List):
    url = os.getenv("DICTIONARY_API_CREATE_URL")
    headers = {'x-api-key': os.getenv("DICTIONARY_API_KEY"), 'Content-Type': 'application/json'}

    for target in targets:
        payload = {
            'inputCode': target.get("i18n"),
            'jaText': target.get("ja"),
            'enText': target.get("en"),
            'scopeLang': 'standard16',
            'target': 'staticProxy',
            'creator': 'Hisamitsu Okabe',
            'skipMachineTranslation': 'False',
            'tenantId': '9',
            'source': ''
        }
        print(f"### payload={payload}")
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"### res={res.text}")


def __main_proc():
    try:
        targets = get_targets()
        assert_targets(targets=targets)
        __register_dictionary(targets)
    except InvalidI18nDataException as e:
        print(f"### Register dictionary error. {e.message}")
        raise e

    print("## Dictionary registered successfully ")


if __name__ == '__main__':
    __main_proc()
