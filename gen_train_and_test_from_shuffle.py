import os
import random
from PIL import Image


def main():
    fixed_workspace = r'E:\training data\MR Cardiac(2)\pairs\all_fixed_pairs'
    moving_workspace = r'E:\training data\MR Cardiac(2)\pairs\all_moving_pairs'

    train_fixed_path = r'E:\training data\MR Cardiac(2)\train\fixed'
    train_moving_path = r'E:\training data\MR Cardiac(2)\train\moving'
    valid_fixed_path = r'E:\training data\MR Cardiac(2)\validate\fixed'
    valid_moving_path = r'E:\training data\MR Cardiac(2)\validate\moving'

    img_names = os.listdir(fixed_workspace)

    #shuffle
    random.shuffle(img_names)
    print('after: ', img_names)

    # generate train_set and valid_set
    all_nums = len(img_names)
    train_nums = int(all_nums*0.8)

    train_img_names = img_names[0:train_nums]
    train_fixed_img_paths = [os.path.join(fixed_workspace, _) for _ in train_img_names]
    train_moving_img_paths = [os.path.join(moving_workspace, _) for _ in train_img_names]
    print('processing training set')
    for i in range(len(train_img_names)):
        fixed_img = Image.open(train_fixed_img_paths[i]).convert('L')
        moving_img = Image.open(train_moving_img_paths[i]).convert('L')
        fixed_img.save(os.path.join(train_fixed_path, '{:>05}.png'.format(i+1)))
        moving_img.save(os.path.join(train_moving_path, '{:>05}.png'.format(i+1)))

    valid_img_names = img_names[train_nums:all_nums]
    valid_fixed_img_paths = [os.path.join(fixed_workspace, _) for _ in valid_img_names]
    valid_moving_img_paths = [os.path.join(moving_workspace, _) for _ in valid_img_names]
    print('processing validating set')
    for j in range(len(valid_img_names)):
        fixed_img = Image.open(valid_fixed_img_paths[j]).convert('L')
        moving_img = Image.open(valid_moving_img_paths[j]).convert('L')
        fixed_img.save(os.path.join(valid_fixed_path, '{:>05}.png'.format(j + 1)))
        moving_img.save(os.path.join(valid_moving_path, '{:>05}.png'.format(j + 1)))


if __name__ == '__main__':
    main()