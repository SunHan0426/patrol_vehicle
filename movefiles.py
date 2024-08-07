import os
import shutil
from datetime import datetime

def main():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    new_folder_path = os.path.join(os.getcwd(), formatted_datetime)
    os.makedirs(new_folder_path)
    folders_to_copy = ["chart", "deepmap", "HKCam_imgs", "img", "img_out", "logs", "npy"]
    
    for folder in folders_to_copy:
        source_folder = os.path.join(os.getcwd(), folder)
        destination_folder = os.path.join(new_folder_path, folder)
        shutil.copytree(source_folder, destination_folder)

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

    runs_folder_path = os.path.join(os.getcwd(), "runs")
    shutil.move(new_folder_path, runs_folder_path)

    print("OK！")

if __name__ == "__main__":
    main()
