# patrol_vehicle
# A Novel Method Utilizing Patrol Vehicle for Automated Detection

This is complete code for orchard Patrol Vehicle control and detection. In this novel approach, an automatic patrol vehicle was developed to save labor in crop monitoring. A CNN-based semantic segmentation method was used to combine with binocular vision and perceive the distance of fruit trees. A Transformer-based semantic segmentation method was used to detect fruit tree diseases efficiently and accurately.

<div align="center">

| Patrol Vehicle  |
| ---------- |
| ![](/img/Patrol Vehicle.jpg) |

</div>

## Instructions
### Requirements
  pyzed==4.1
  opencv_python==4.5.5
  torch==1.13.0
  torchvision==0.14.0
  PyQt5==5.15
  mmcv==2.0.0
  mmsegmentation==1.2.2
### How to use?
Just run the following code to open the GUI page:
  python /main_script.py
In this project, the interactive interface has been made. You can easily realize distance perception, image acquisition, image inference and other operations by using the GUI.
<div align="center">

| The GUI  |
| ---------- |
| ![](/img/GUI.jpg) |

</div>
### Save route
  The ranging data is saved in "/npy" in the form of .npy
  Visualized data is saved in "/chart"
  The depth image output by the camera is saved in "/deepmap"
  The recognition image output by the algorithm is saved in "/img_out"
  Logs are saved in "/logs"
  The images acquire by HD-camera are saved in "/HKCam_imgs"
  The results of disease segmentation are saved in "seg_img"

## Contribution

## Reference
