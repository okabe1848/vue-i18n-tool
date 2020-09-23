# -*- coding: utf-8 -*-
import os
from typing import Set

from googletrans import Translator

from i18n.constants import READ_COL_JA, READ_ROW_STARTING, READ_COL_EN
from i18n.shared_logic import get_ss_worksheet, get_ja_words


def __write_words_in_ss(words_set: Set[str]):
    worksheet = get_ss_worksheet()
    worksheet.clear()

    words = list(words_set)
    size = len(words)
    cells = worksheet.range(f"{READ_COL_JA}{READ_ROW_STARTING}:{READ_COL_EN}{str(size+READ_ROW_STARTING-1)}")
    translator = Translator()

    for i, cell in enumerate(cells):
        word_jp = words[i // 2]
        is_jp = True if i % 2 == 0 else False
        if is_jp:
            cell.value = word_jp
        else:
            translated = translator.translate(word_jp, src='ja', dest="en");
            cell.value = translated.text

    worksheet.update_cells(cells)


def __extract_ja_words():
    ja_words = get_ja_words()
    __write_words_in_ss(set(ja_words))


if __name__ == '__main__':
    print("## Extract JP words from ja.text")
    __extract_ja_words()
    print("## Successfully extracted in Spread Sheet")
    print(os.getenv("SPREAD_SHEET_URL"))
