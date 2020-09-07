# -*- coding: utf-8 -*-
import re

from i18n.constants import READ_ROW_STARTING, READ_COL_JA, READ_COL_I18N
from i18n.shared_logic import get_ss_worksheet, get_ja_text, get_ja_words_with_quot


def __get_i18n_map():
    worksheet = get_ss_worksheet()
    res = {}
    for row in range(READ_ROW_STARTING, 100):
        word_ja = worksheet.acell(f"{READ_COL_JA}{row}").value
        if not word_ja:
            break
        res[word_ja] = worksheet.acell(f"{READ_COL_I18N}{row}").value
    return res


def __convert_words():
    i18n_map = __get_i18n_map()
    i18n_values = list(i18n_map.values())
    if i18n_values.count("") > 0:
        print(f"###### Failed!!! i18n key is not set. ######")
        return

    text = get_ja_text()
    ja_words = get_ja_words_with_quot()
    ja_words_sorted = sorted(ja_words, key=len, reverse=True)
    for ja_word in ja_words_sorted:
        k = re.sub("['`\"]", "", ja_word)
        v = i18n_map.get(k)
        matched = re.match("^['`\"]", ja_word)
        is_logic = True if matched and matched.start() == 0 else False
        text = text.replace(ja_word, f"i18n.t(\"{v}\").toString()" if is_logic else f"{{{{ $t(\"{v}\") }}}}")

    with open("i18n/resource/en.txt", mode='w') as f:
        f.write(text)


if __name__ == '__main__':
    print("## Read JP words and its conversation")
    __convert_words()
    print("## Successfully finished conversation")
