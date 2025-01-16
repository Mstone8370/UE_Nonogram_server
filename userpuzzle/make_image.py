import cv2
import numpy as np
import os

from django.conf import settings

filled_color = 32
blank_color = 255

def to_color_mat(row: list) -> list:
    return [filled_color if x == 1 else blank_color for x in row]

def board_to_matrix(board: list):
    return list(map(to_color_mat, board))

def save_to_img(board: list, file_name: str = 'default_file_name'):
    if not os.path.exists(settings.TEMP_MEDIA_ROOT):
        os.mkdir(settings.TEMP_MEDIA_ROOT)
    img_dir = os.path.join(settings.TEMP_MEDIA_ROOT, file_name + ".png")
    img_saved = cv2.imwrite(img_dir, np.array(board_to_matrix(board), dtype=np.uint8))

    return img_dir if img_saved else ""

def num_to_char(n: int):
    ret = chr(ord('A') + n)
    if ret > ord('Z'):
        ret += (ord('a') - ord('Z') - 1)
    return ret

def char_to_num(c):
    return ord(c) - ord('A') if ord(c) < ord('a') else ord(c) - 71 # ord(c) - ord('A') - (ord('a') - ord('Z') - 1)

def decode_puzzle(data: str):
    row_datas = data.split('|')
    puzzle = []
    for i in range(len(row_datas)):
        puzzle_row = list()
        filled = False
        for c in row_datas[i]:
            if ord('0') <= ord(c) and ord(c) < ord('4'):
                filled = (ord(c) - ord('0') == 1)
            else:
                num = char_to_num(c)
                puzzle_row.extend([1] * num if filled else [2] * num)
        puzzle.append(puzzle_row)
    return puzzle

def save_img_with_encoded_puzzle(encoded_board: str, file_name: str = 'default_file_name'):
    return save_to_img(decode_puzzle(encoded_board), file_name)