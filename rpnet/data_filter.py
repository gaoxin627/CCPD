import os
import shutil

import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont


provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
             "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']


def parse_points(points_str):
    points = []
    points_split = points_str.split('_')
    for point_str in points_split:
        point_split = point_str.split('&')
        x = int(point_split[0])
        y = int(point_split[1])
        points.append((x, y))
    return points


def parse_name(file_name):
    data = file_name.split('-')
    if len(data) == 7:
        points = parse_points(data[2])
        points.extend(parse_points(data[3]))
        lpn_split = data[4].split('_')
        lpn_list = [ads[int(lpn_split[i])] for i in range(2, len(lpn_split))]
        lpn_str = provinces[int(lpn_split[0])] + alphabets[int(lpn_split[1])] + ''.join(lpn_list)
        return points, lpn_str, provinces[int(lpn_split[0])]
    else:
        return None, None, None


def putText(img, x, y, str):
    img = cv2.copyMakeBorder(img, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype('simhei.ttf', 40, encoding="utf-8")
    draw.text((x, y), str, (255, 0, 0), font=font)
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return cv2charimg


if __name__ == '__main__':

    root_path = '/Users/gaoxin/Downloads/data'
    out_path = '/Users/gaoxin/Downloads/data_out'
    num = 500

    province_num = dict()
    province_num_out = dict()
    for dir_name in os.listdir(root_path):
        dir_path = os.path.join(root_path, dir_name)
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                if file_name.endswith('jpg'):
                    points, lpn, province = parse_name(file_name)
                    if points:
                        # file_path = os.path.join(root_path, file_name)
                        # img = cv2.imread(file_path)
                        # # for point in points:
                        # #     cv2.circle(img, point, 1, (0, 0, 255), 4)
                        # cv2.rectangle(img, points[0], points[1], (0, 0, 255), 2)
                        # img_text = putText(img, points[0][0], points[0][1], lpn)
                        # cv2.imshow('img', img_text)
                        # key = cv2.waitKey(0)
                        # if key == 27:
                        #     break

                        if province in province_num:
                            province_num[province] += 1
                        else:
                            province_num[province] = 1

                        if province_num[province] <= num:
                            source_dir = os.path.join(dir_path, file_name)
                            target_dir = os.path.join(out_path, file_name)
                            shutil.copy(source_dir, target_dir)
                            if province in province_num_out:
                                province_num_out[province] += 1
                            else:
                                province_num_out[province] = 1
                    else:
                        print('parse error:', file_name)

    print(province_num)
    print(province_num_out)
