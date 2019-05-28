import os
import pickle
from PIL import Image
import numpy as np


def gen_2d_img(img_path: str, out_dir: str, transpose_axis: list = None, res_corr: bool = False, img_name=None):
    # 创建输出文件夹
    if img_name is None:
        img_name = os.path.splitext(os.path.split(img_path)[-1])[0]
    img_out_dir = os.path.join(out_dir, img_name)
    if not os.path.isdir(img_out_dir):
        os.makedirs(img_out_dir)

    # 加载数据
    f = open(img_path, 'rb')
    data = pickle.load(f)
    if data.ndim == 5:
        data = data[0, :, :, :, 0]

    # 分辨率矫正(resolution correction)
    if res_corr is True:
        _corr_factor = 0.140625
        _ori_height, _ori_width = data.shape[0:2]
        _height_start, _height_end = int(_ori_height * _corr_factor), _ori_height - int(_ori_height * _corr_factor)
        _width_start, _width_end = int(_ori_width * _corr_factor), _ori_width - int(_ori_width * _corr_factor)
        for i in range(data.shape[2]):
            img_arr = data[_height_start: _height_end, _width_start: _width_end, i]
            img = Image.fromarray(img_arr).resize([_ori_width, _ori_height], resample=Image.BICUBIC)
            data[:, :, i] = np.array(img)

    # 转秩
    if transpose_axis is not None:
        data = data.transpose(transpose_axis)
    # 极值归一化
    data = (data - data.min()) / (data.max() - data.min())

    # 保存数据
    for i in range(data.shape[2]):
        img_arr = (data[:, :, i] * 255).astype(np.uint8)
        img = Image.fromarray(img_arr)
        img.save(os.path.join(img_out_dir, "{:>03}.jpg".format(i)))

    # 释放资源
    f.close()


def gen_2d_img_ori_v2(input_pickle_path: str, img_out_dir_path: str, ):
    """
    将5维的pickle转化成一堆二维图片，保存原来的浮点数据
    :param input_pickle_path:
    :param img_out_dir_path:
    :return:
    """
    # create output dir if output dir does not exist
    if not os.path.exists(img_out_dir_path):
        os.mkdir(img_out_dir_path)

    # load data. shape: [batch_size, img_height, img_width, img_depth, channel]
    with open(input_pickle_path, 'rb') as f:
        data = pickle.load(f)

    # save image original data
    for i in range(data.shape[1]):
        arr = data[0, i, :, :, 0].transpose([1, 0])
        img_inst = Image.fromarray(arr)
        img_inst.save(os.path.join(img_out_dir_path, "{:>03}.tif".format(i)))


def test():
    gen_2d_img_ori_v2(
        input_pickle_path=r"X:\registration_patches\2019_03_07_淋巴瘤176例\1_非霍奇金淋巴瘤\3D\suv_whole_body.pkl",
        img_out_dir_path=r"X:\registration_patches\2019_03_07_淋巴瘤176例\1_非霍奇金淋巴瘤\analyze\2d_suv_imgs"
    )


if __name__ == '__main__':
    test()
