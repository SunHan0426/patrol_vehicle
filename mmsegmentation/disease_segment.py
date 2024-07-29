import os
import numpy as np
import cv2
from tqdm import tqdm
from mmseg.apis import init_model, inference_model


config_file = 'path/to/config'
checkpoint_file = 'path/to/weight'

device = 'cuda:0'
model = init_model(config_file, checkpoint_file, device=device)

palette = [
    ['background', [0, 0, 0]],
    ['PR', [0, 0, 128]],
    ['PA', [0, 128, 0]],
    ['PBS', [0, 128, 128]]
]

palette_dict = {}
for idx, each in enumerate(palette):
    palette_dict[idx] = each[1]

opacity = 0.25

def process_single_img(img_path, save=False):
    img_bgr = cv2.imread(img_path)

    result = inference_model(model, img_bgr)
    pred_mask = result.pred_sem_seg.data[0].cpu().numpy()

    pred_mask_bgr = np.zeros((pred_mask.shape[0], pred_mask.shape[1], 3))
    for idx in palette_dict.keys():
        pred_mask_bgr[np.where(pred_mask == idx)] = palette_dict[idx]
    pred_mask_bgr = pred_mask_bgr.astype('uint8')

    pred_viz = cv2.addWeighted(img_bgr, opacity, pred_mask_bgr, 1 - opacity, 0)

    if save:
        save_dir = os.path.join(input_dir, '../seg_img')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'seg-' + os.path.basename(img_path))
        cv2.imwrite(save_path, pred_viz)

input_dir = "./HKCam_imgs"

image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
image_files = sorted(image_files, key=os.path.getmtime, reverse=True)

latest_images = image_files[:3]

for img_path in tqdm(latest_images):
    process_single_img(img_path, save=True)


