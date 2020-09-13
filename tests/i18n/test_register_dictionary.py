from typing import List

from i18n.register_dictionary import assert_targets, InvalidI18nDataException


def __get_error_message(targets: List) -> str:
    err = None
    try:
        assert_targets(targets)
    except InvalidI18nDataException as e:
        err = e.message
    return err


def test_no_target():
    err = __get_error_message([])
    assert (err == InvalidI18nDataException.Code.NO_TARGETS)
    err = __get_error_message(None)
    assert (err == InvalidI18nDataException.Code.NO_TARGETS)


def test_duplicated():
    targets = [
        {"i18n": "okabe_test", "ja": "岡部テスト02", "en": "Okabe Test 02"},
        {"i18n": "okabe_test", "ja": "岡部テスト03", "en": "Okabe Test 03"},
    ]
    err = __get_error_message(targets)
    assert (err == InvalidI18nDataException.Code.DUPLICATED_I18N_CODE)


def test_lookup_failed():
    targets = [
        {"i18n": "job10", "ja": "岡部テスト02", "en": "Okabe Test 02"},
    ]
    print()
    err = __get_error_message(targets)
    assert (err == InvalidI18nDataException.Code.EXISTS_ALREADY)


def test_success():
    targets = [
        {"i18n": "okabe_test_asdfadf", "ja": "岡部テスト02", "en": "Okabe Test 02"},
        {"i18n": "okabe_test_adfadfad", "ja": "岡部テスト03", "en": "Okabe Test 03"},
    ]
    print()
    err = __get_error_message(targets)
    assert (err is None)
