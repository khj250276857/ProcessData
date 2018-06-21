import os
import shutil

#将pairs文件夹中的每个子文件的fixed和moving中的图片，分别复制并重命名到统一的fixed和moving文件夹

def get_fixed_paths(workspace):
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    fixed_paths = []
    for file_path in file_paths:
        paths = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
        for path in paths:
            if path.endswith('fixed'):
                fixed_paths.append(path)
    return fixed_paths


def get_moving_paths(workspace):
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    moving_paths = []
    for file_path in file_paths:
        paths = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
        for path in paths:
            if path.endswith('moving'):
                moving_paths.append(path)
    return moving_paths


def copy_fixed_images(fixed_paths, new_fixed_path):
    for fixed_path in fixed_paths:
        print('processing {}...........'.format(fixed_path))
        file_names = [os.path.join(fixed_path, _) for _ in os.listdir(fixed_path)]
        num = len(os.listdir(new_fixed_path))
        for i in range(len(file_names)):
            file_name = file_names[i]
            new_file_name = os.path.join(new_fixed_path, '{:>05}.png'.format(num+i+1))
            shutil.copyfile(file_name, new_file_name)


def copy_moving_images(moving_paths, new_moving_path):
    for moving_path in moving_paths:
        print('processing {}...........'.format(moving_path))
        file_names = [os.path.join(moving_path, _) for _ in os.listdir(moving_path)]
        num = len(os.listdir(new_moving_path))
        for i in range(len(file_names)):
            file_name = file_names[i]
            new_file_name = os.path.join(new_moving_path, '{:>05}.png'.format(num+i+1))
            shutil.copyfile(file_name, new_file_name)


def main():
    workspace = r'E:\training data\MR Cardiac(2)\pairs'
    fixed_paths = get_fixed_paths(workspace)
    moving_paths = get_moving_paths(workspace)
    new_fixed_path = r'E:\training data\MR Cardiac(2)\pairs\all_fixed_pairs'
    new_moving_path = r'E:\training data\MR Cardiac(2)\pairs\all_moving_pairs'
    if not os.path.exists(new_fixed_path):
        os.mkdir(new_fixed_path)
    if not os.path.exists(new_moving_path):
        os.mkdir(new_moving_path)

    copy_fixed_images(fixed_paths, new_fixed_path)
    copy_moving_images(moving_paths, new_moving_path)


if __name__ == '__main__':
    main()