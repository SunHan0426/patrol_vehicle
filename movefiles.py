import os
import shutil
from datetime import datetime

def main():
    # 获取当前日期时间
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # 创建以当前日期时间命名的文件夹
    new_folder_path = os.path.join(os.getcwd(), formatted_datetime)
    os.makedirs(new_folder_path)

    # 复制文件夹及其内容到新文件夹中
    folders_to_copy = ["chart", "deepmap", "HKCam_imgs", "img", "img_out", "logs", "npy"]
    for folder in folders_to_copy:
        source_folder = os.path.join(os.getcwd(), folder)
        destination_folder = os.path.join(new_folder_path, folder)
        shutil.copytree(source_folder, destination_folder)

        # 清空文件夹内的文件
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

    # 将时间日期文件夹移动到名为 "runs" 的文件夹内
    runs_folder_path = os.path.join(os.getcwd(), "runs")
    shutil.move(new_folder_path, runs_folder_path)

    print("OK！")

if __name__ == "__main__":
    main()