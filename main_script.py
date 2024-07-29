import pyzed.sl as sl
import cv2
import os
import numpy as np
import logging
from pyfirmata import ArduinoMega, SERVO, PWM, OUTPUT
import time
from MvCameraControl_class import *
import datetime
import serial
import re
import piexif
import ctypes
from ctypes import c_ubyte, byref
from PIL import Image
import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot
from Ui import Ui_MainWindow
from PyQt5.Qt import Qt, QPixmap


board = ArduinoMega('/dev/ttyACM0')
pin = 10
board.digital[pin].mode = SERVO
board.servo_config(10, angle=75)
time.sleep(0.3)
enA = 9
in1 = 8
in2 = 7
board.digital[enA].mode = PWM
board.digital[in1].mode = OUTPUT
board.digital[in2].mode = OUTPUT
board.digital[enA].write(1)

ser = serial.Serial("/dev/ttyUSB0", 9600)

if ser.isOpen():
    print("GPS Serial Opened! Baudrate = 9600")
else:
    print("GPS Serial Open Failed!")

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    identifier = 1
    id_ZED = 1
    id_predict = 1
    img_folder_path = "./HKCam_imgs"
    utctime, lat, ulat, lon, ulon, numSv, msl = '', '', '', '', '', '', ''
    global GNSS
    global gps_t
    gps_t, GNSS = 0, 0
    global v_rod
    v_rod = 3.33
    with open('id.txt', 'w') as file:
        file.write(f'id={id_predict}')

    def calculate_euclidean_distance(self, point_cloud_np):
        x = point_cloud_np[:, :, 0]
        y = point_cloud_np[:, :, 1]
        z = point_cloud_np[:, :, 2]
        # euclidean_distances = point_cloud_np # if use deep info
        euclidean_distances = np.round(np.sqrt(x ** 2 + y ** 2 + z ** 2), 4) # if use distance info
        return euclidean_distances

    def image_capture(self):
        zed = sl.Camera()
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD1080
        init_params.camera_fps = 30
        init_params.depth_mode = sl.DEPTH_MODE.ULTRA
        init_params.coordinate_units = sl.UNIT.METER

        err = zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            exit(1)

        runtime_parameters = sl.RuntimeParameters()
        runtime_parameters.enable_fill_mode = True
        i = 0
        image_left = sl.Mat()
        image_right = sl.Mat()
        dep_npy = sl.Mat()
        dep_view = sl.Mat()
        point_cloud = sl.Mat()

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            self.textBrowser.append("OPEN CAMERA SUCCESS.")
            QApplication.processEvents()
            print("OPEN CAMERA SUCCESS.")
            zed.retrieve_image(image_left, sl.VIEW.LEFT)
            img_left = image_left.get_data()

            zed.retrieve_image(image_right, sl.VIEW.RIGHT)
            img_right = image_right.get_data()

            zed.retrieve_measure(dep_npy, sl.MEASURE.DEPTH)
            dep_map = dep_npy.get_data()

            zed.retrieve_image(dep_view, sl.VIEW.DEPTH)
            dep_visual = dep_view.get_data()

            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZ)
            point_cloud_np = point_cloud.get_data()
            print("point_cloud_np shape: ", point_cloud_np.shape)
            start_time1 = time.time()
            euclidean_distance = self.calculate_euclidean_distance(point_cloud_np)
            self.textBrowser.append("euclidean_distance= {}".format(euclidean_distance))
            QApplication.processEvents()
            print(euclidean_distance)
            end_time1 = time.time()
            elapsed_time1 = end_time1 - start_time1
            self.textBrowser.append(f"Calculate distance map time: {elapsed_time1:.2f} seconds")
            QApplication.processEvents()
            print(f"Calculate distance map time: {elapsed_time1:.2f} seconds")

            view_RGB_LEFT = img_left
            view_RGB_RIGHT = img_right
            view_Depth = dep_visual

            euclidean_distance_vis = (euclidean_distance - np.nanmin(euclidean_distance)) / (
                        np.nanmax(euclidean_distance) -
                        np.nanmin(euclidean_distance)) * 255.0
            euclidean_distance_vis = euclidean_distance_vis.astype("uint8")
            euclidean_distance_vis = cv2.applyColorMap(euclidean_distance_vis, cv2.COLORMAP_VIRIDIS)

            SavePath = os.path.join("./img", "RGB_LEFT_{:0>3d}.png".format(MainWindow.id_ZED))
            SavePath_1 = os.path.join("./img", "RGB_RIGHT_{:0>3d}.png".format(MainWindow.id_ZED))
            SavePath_2 = os.path.join("./deepmap", "Deep_{:0>3d}.png".format(MainWindow.id_ZED))
            SavePath_5 = os.path.join("./deepmap", "Distance_{:0>3d}.png".format(MainWindow.id_ZED))
            SavePath_3 = os.path.join("./npy", "deep_npy_ZED_{:0>3d}.npy".format(MainWindow.id_ZED))
            SavePath_4 = os.path.join("./npy", "distance_npy_ZED_{:0>3d}.npy".format(MainWindow.id_ZED))

            cv2.imwrite(SavePath, view_RGB_LEFT)
            cv2.imwrite(SavePath_1, view_RGB_RIGHT)
            print("{:0>3d} RGB IMAGE SAVED.".format(self.id_ZED))
            cv2.imwrite(SavePath_2, view_Depth)
            print("{:0>3d} DEEP IMAGE SAVED.".format(self.id_ZED))
            np.save(SavePath_3, dep_map)
            print("{:0>3d} DEEP npy SAVED.".format(self.id_ZED))
            np.save(SavePath_4, euclidean_distance)
            print("{:0>3d} DISTANCE npy SAVED.".format(self.id_ZED))
            cv2.imwrite(SavePath_5, euclidean_distance_vis)
            print("{:0>3d} DISTANCE IMAGE SAVED.".format(self.id_ZED))
            self.textBrowser.append("{:0>3d} RGB IMAGE SAVED.".format(self.id_ZED))
            self.textBrowser.append("{:0>3d} DEEP IMAGE SAVED.".format(self.id_ZED))
            self.textBrowser.append("{:0>3d} DEEP npy SAVED.".format(self.id_ZED))
            self.textBrowser.append("{:0>3d} DISTANCE npy SAVED.".format(self.id_ZED))
            self.textBrowser.append("{:0>3d} DISTANCE IMAGE SAVED.".format(self.id_ZED))
            QApplication.processEvents()
        zed.close()

    def run_predict(self):
        try:
            # run trunk detect script
            subprocess.run(["python", "./pspnet/predict.py"])

        except FileNotFoundError:
            print("NO SUCH SCRIPT.")

    def delete_bmp_files(self, directory):
        files = os.listdir(directory)
        for file in files:
            if file.endswith(".bmp"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)
                self.textBrowser.append(f"Deleted: {file_path}")
                QApplication.processEvents()
                print(f"Deleted: {file_path}")

    def Convert_to_degrees(self, in_data1, in_data2):
        len_data1 = len(in_data1)
        str_data2 = "%05d" % int(in_data2)
        temp_data = int(in_data1)
        symbol = 1
        if temp_data < 0:
            symbol = -1
        degree = int(temp_data / 100.0)
        str_decimal = str(in_data1[len_data1 - 2]) + str(in_data1[len_data1 - 1]) + str(str_data2)
        f_degree = int(str_decimal) / 60.0 / 100000.0
        if symbol > 0:
            result = degree + f_degree
        else:
            result = degree - f_degree
        return result

    def decimal_to_dms(self, decimal):
        degree = int(decimal)
        temp = (decimal - degree) * 60
        minute = int(temp)
        second = (temp - minute) * 60
        return ((degree, 1), (minute, 1), (int(second * 100), 100))

    def opencam(self):
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        # Enum device
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            print("enum devices fail! ret[0x%x]" % ret)
            sys.exit()
        if deviceList.nDeviceNum == 0:
            print("find no device!")
            sys.exit()
        self.textBrowser.append("find %d camera!" % deviceList.nDeviceNum)
        QApplication.processEvents()
        print("find %d camera!" % deviceList.nDeviceNum)

        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print("\nu3v device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print("user serial number: %s" % strSerialNumber)

        nConnectionNum = 0

        if int(nConnectionNum) >= deviceList.nDeviceNum:
            print("intput error!")
            sys.exit()
        # Creat Camera Object
        global cam
        cam = MvCamera()
        # Select device and create handle
        stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
        ret = cam.MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            sys.exit()
        # Open device
        ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            sys.exit()
        # Set auto exposure to continuous
        ret = cam.MV_CC_SetEnumValue("ExposureAuto", MV_EXPOSURE_AUTO_MODE_CONTINUOUS)
        if ret != 0:
            print("set auto exposure to continuous fail! ret[0x%x]" % ret)
            sys.exit()
        # Set the automatic gain to continuous
        ret = cam.MV_CC_SetEnumValue("GainAuto", MV_GAIN_MODE_CONTINUOUS)
        if ret != 0:
            print("set the automatic gain to continuous fail! ret[0x%x]" % ret)
            sys.exit()
        # Set brightness
        cam.MV_CC_SetFloatValue("nAverageBrightness", float(120))
        # Set trigger mode as off
        ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()
        # Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
        ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)
            sys.exit()
        global nPayloadSize
        nPayloadSize = stParam.nCurValue
        # Start grab image

        ret = cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            sys.exit()
        time.sleep(1.5)

    def get_img(self):
        # Creat Camera Object
        global formatted_datetime
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")  # 转换时间格式

        stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(stDeviceList), 0, sizeof(stDeviceList))
        data_buf = (c_ubyte * nPayloadSize)()

        ret = cam.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stDeviceList, 1000)
        if ret == 0:
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
                stDeviceList.nWidth, stDeviceList.nHeight, stDeviceList.nFrameNum))
            bmpsize = stDeviceList.nWidth * stDeviceList.nHeight * 3 + 54
            stConvertParam = MV_SAVE_IMAGE_PARAM_EX()
            stConvertParam.nWidth = stDeviceList.nWidth
            stConvertParam.nHeight = stDeviceList.nHeight
            stConvertParam.pData = data_buf
            stConvertParam.nDataLen = stDeviceList.nFrameLen
            stConvertParam.enPixelType = stDeviceList.enPixelType
            stConvertParam.nImageLen = stConvertParam.nDataLen
            stConvertParam.enImageType = MV_Image_Bmp
            # Due to Xavier's cache problem, it is saved in bmp format and then converted to jpg.
            stConvertParam.pImageBuffer = (c_ubyte * bmpsize)()
            stConvertParam.nBufferSize = bmpsize
            ret = cam.MV_CC_SaveImageEx2(stConvertParam)
            if ret != 0:
                print("convert pixel fail ! ret[0x%x]" % ret)
                del data_buf
                sys.exit()
            file_path = os.path.join(MainWindow.img_folder_path, formatted_datetime + ".bmp")
            file_open = open(file_path.encode('ascii'), 'wb+')
            img_buff = (c_ubyte * stConvertParam.nImageLen)()
            ctypes.memmove(img_buff, stConvertParam.pImageBuffer, stConvertParam.nImageLen)
            file_open.write(bytes(img_buff))
            # Convert bmp to jpg
            bmp_file_path = os.path.join(MainWindow.img_folder_path, formatted_datetime + ".bmp")
            global jpg_save_path
            global open_jpg_save_path
            open_jpg_save_path = os.path.join(MainWindow.img_folder_path, formatted_datetime + ".jpg")
            jpg_save_path = os.path.join(MainWindow.img_folder_path, formatted_datetime + ".jpg")
            with Image.open(bmp_file_path) as img:
                img.convert('RGB').save(jpg_save_path, 'JPEG', quality=99)
            with open("datatime.txt", "w") as f:
                f.write(str(formatted_datetime))
        print("Current time:", formatted_datetime)
        self.textBrowser.append("Current time: {}".format(formatted_datetime))
        time.sleep(0.3)
        print("Save Image succeed!")
        self.textBrowser.append("Save Image succeed!")
        QApplication.processEvents()

    def closecam(self):
        # Stop grab image
        ret = cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            sys.exit()
        # Close device
        ret = cam.MV_CC_CloseDevice()
        if ret != 0:
            print("close deivce fail! ret[0x%x]" % ret)
            sys.exit()
        # Destroy handle
        ret = cam.MV_CC_DestroyHandle()
        if ret != 0:
            print("destroy handle fail! ret[0x%x]" % ret)
            sys.exit()

    def GPS_read(self):
        global utctime
        global lat
        global ulat
        global lon
        global msl
        global exif_dict
        global ulon
        global numSv
        global gps_t
        if ser.inWaiting():
            if ser.read(1) == b'G':
                if ser.inWaiting():
                    if ser.read(1) == b'N':
                        if ser.inWaiting():
                            choice = ser.read(1)
                            if choice == b'G':
                                if ser.inWaiting():
                                    if ser.read(1) == b'G':
                                        if ser.inWaiting():
                                            if ser.read(1) == b'A':
                                                GGA = ser.read(70)
                                                GGA_g = re.findall(r"\w+(?=,)|(?<=,)\w+", str(GGA))
                                                if len(GGA_g) < 13:
                                                    print("GPS not found")
                                                    gps_t = 0
                                                    return 0
                                                else:
                                                    utctime = GGA_g[0]
                                                    lat = "%.8f" % self.Convert_to_degrees(str(GGA_g[2]), str(GGA_g[3]))
                                                    ulat = GGA_g[4]
                                                    lon = "%.8f" % self.Convert_to_degrees(str(GGA_g[5]), str(GGA_g[6]))
                                                    ulon = GGA_g[7]
                                                    numSv = GGA_g[9]
                                                    msl = GGA_g[12] + '.' + GGA_g[13] + GGA_g[14]
                                                    gps_t = 1
                                                    return 1
                            elif choice == b'V':
                                if ser.inWaiting():
                                    if ser.read(1) == b'T':
                                        if ser.inWaiting():
                                            if ser.read(1) == b'G':
                                                if gps_t == 1:
                                                    VTG = ser.read(40)

    def rod_HKcam_ctrl(self, GNSS, v_rod):
        print("Camera turn middle")
        # The servo is fixed in the middle position first
        self.textBrowser.append("Camera turn middle.")
        QApplication.processEvents()
        board.servo_config(10, angle=75)
        time.sleep(0.5)

        with open("trunk_distance.txt", "r") as f:
            file_content = f.read().strip()

        if file_content:
            trunk_distance = float(file_content)
        else:
            trunk_distance = 0.8

        print("trunk_distance=", trunk_distance)
        self.textBrowser.append("trunk_distance={}".format(trunk_distance))
        rod_distance = trunk_distance - 0.8
        global t_rod
        t_rod = rod_distance * 100 / v_rod
        print("t_rod=", t_rod)
        self.textBrowser.append("t_rod={}".format(t_rod))
        QApplication.processEvents()
        if t_rod > 15:
            t_rod = 15
            print("Distance exceeds threshold, push rod to farthest.")
            self.textBrowser.append("Distance exceeds threshold, push rod to farthest.")
        if t_rod < 0:
            t_rod = 0.01
            print("Distance less than set value, rod static.")
            self.textBrowser.append("Distance less than set value, rod static.")
        with open("t_rod.txt", "w") as f:
            f.write(str(t_rod))
        print("Rod leaving...")
        self.textBrowser.append("Rod leaving...")
        QApplication.processEvents()
        board.digital[in1].write(0)
        board.digital[in2].write(1)
        time.sleep(t_rod)
        board.digital[in1].write(0)
        board.digital[in2].write(0)
        time.sleep(0.3)
        with open("trunk_distance.txt", "w") as f:
            f.write(str(0))  # trunk_distance -> 0
        # servo up
        print("Camera turn middle")
        self.textBrowser.append("Camera turn up.")
        QApplication.processEvents()
        board.servo_config(10, angle=50)
        time.sleep(3)
        # get img
        self.get_img()
        global a1
        with open("datatime.txt", "r") as f:
            a1 = str(f.read())
        # Get geographic information and save
        try:
            while GNSS < 1:
                if self.GPS_read():
                    print("*********************")
                    print('UTC Time:' + utctime)
                    print('Latitude:' + lat + ulat)
                    print('Longitude:' + lon + ulon)
                    print('Number of satellites:' + numSv)
                    print('Altitude:' + msl)
                    print("*********************")
                    self.textBrowser.append("*********************")
                    self.textBrowser.append('UTC Time: {}'.format(utctime))
                    self.textBrowser.append('Latitude: {}{}'.format(lat, ulat))
                    self.textBrowser.append('Longitude: {}{}'.format(lon, ulon))
                    self.textBrowser.append('Number of satellites: {}'.format(numSv))
                    self.textBrowser.append('Altitude: {}'.format(msl))
                    self.textBrowser.append("*********************")
                    QApplication.processEvents()
                    img = Image.open(jpg_save_path)
                    if "exif" not in img.info:
                        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
                    else:
                        exif_dict = piexif.load(img.info["exif"])

                    exif_dict["GPS"] = {
                        piexif.GPSIFD.GPSLatitudeRef: ulat,
                        piexif.GPSIFD.GPSLatitude: self.decimal_to_dms(float(lat)),
                        piexif.GPSIFD.GPSLongitudeRef: ulon,
                        piexif.GPSIFD.GPSLongitude: self.decimal_to_dms(float(lon)),
                        piexif.GPSIFD.GPSAltitudeRef: 0,
                        piexif.GPSIFD.GPSAltitude: (int(msl.split('.')[0]), 1)
                    }
                    # Save EXIF information
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(jpg_save_path, exif=exif_bytes)
                    print("Image saved with GPS information.")
                    self.textBrowser.append("Image saved with GPS information.")
                    GNSS += 1

        except KeyboardInterrupt:
            ser.close()
            print("GPS serial Close!")

        GNSS = 0
        # servo middle
        print("Camera turn down.")
        self.textBrowser.append("Camera turn middle.")
        QApplication.processEvents()
        board.servo_config(10, angle=65)
        time.sleep(3)
        # get img
        self.get_img()
        global a2
        with open("datatime.txt", "r") as f:
            a2 = str(f.read())
        # Get geographic information and save
        try:
            while GNSS < 1:
                if self.GPS_read():
                    print("*********************")
                    print('UTC Time:' + utctime)
                    print('Latitude:' + lat + ulat)
                    print('Longitude:' + lon + ulon)
                    print('Number of satellites:' + numSv)
                    print('Altitude:' + msl)
                    print("*********************")

                    img = Image.open(jpg_save_path)
                    if "exif" not in img.info:
                        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
                    else:
                        exif_dict = piexif.load(img.info["exif"])

                    exif_dict["GPS"] = {
                        piexif.GPSIFD.GPSLatitudeRef: ulat,
                        piexif.GPSIFD.GPSLatitude: self.decimal_to_dms(float(lat)),
                        piexif.GPSIFD.GPSLongitudeRef: ulon,
                        piexif.GPSIFD.GPSLongitude: self.decimal_to_dms(float(lon)),
                        piexif.GPSIFD.GPSAltitudeRef: 0,
                        piexif.GPSIFD.GPSAltitude: (int(msl.split('.')[0]), 1)
                    }
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(jpg_save_path, exif=exif_bytes)
                    print("Image saved with GPS information.")
                    self.textBrowser.append("Image saved with GPS information.")
                    GNSS += 1

        except KeyboardInterrupt:
            ser.close()
            print("GPS serial Close!")

        GNSS = 0
        # servo down
        print("Camera turn up")
        self.textBrowser.append("Camera turn down.")
        QApplication.processEvents()
        board.servo_config(10, angle=80)
        time.sleep(3)
        # get image
        self.get_img()
        global a3
        with open("datatime.txt", "r") as f:
            a3 = str(f.read())
        # Get geographic information and save
        try:
            while GNSS < 1:
                if self.GPS_read():
                    print("**************GNSS info**************")
                    print('UTC Time:' + utctime)
                    print('Latitude:' + lat + ulat)
                    print('Longitude:' + lon + ulon)
                    print('Number of satellites:' + numSv)
                    print('Altitude:' + msl)
                    print("*************************************")

                    img = Image.open(jpg_save_path)
                    if "exif" not in img.info:
                        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
                    else:
                        exif_dict = piexif.load(img.info["exif"])

                    exif_dict["GPS"] = {
                        piexif.GPSIFD.GPSLatitudeRef: ulat,
                        piexif.GPSIFD.GPSLatitude: self.decimal_to_dms(float(lat)),
                        piexif.GPSIFD.GPSLongitudeRef: ulon,
                        piexif.GPSIFD.GPSLongitude: self.decimal_to_dms(float(lon)),
                        piexif.GPSIFD.GPSAltitudeRef: 0,
                        piexif.GPSIFD.GPSAltitude: (int(msl.split('.')[0]), 1)
                    }
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(jpg_save_path, exif=exif_bytes)
                    print("Image saved with GPS information")

                    GNSS += 1

        except KeyboardInterrupt:
            ser.close()
            print("GPS serial Close!")
        GNSS = 0

        # servo middle
        print("Camera turn middle")
        self.textBrowser.append("Camera turn middle.")
        QApplication.processEvents()
        board.servo_config(10, angle=75)

        self.delete_bmp_files(MainWindow.img_folder_path)

        return a1, a2, a3
    @pyqtSlot()
    def on_Volt_1_clicked(self):
        pass
    
    @pyqtSlot()
    def on_Volt_2_clicked(self):
        pass
    
    @pyqtSlot()
    def on_get_distance_clicked(self):
        self.textBrowser.append("main_script: EPOCH: {:0>3d}".format(MainWindow.identifier))
        self.image_capture()
        self.textBrowser.append("Trunk Locating...")
        QApplication.processEvents()
        time.sleep(0.5)
        self.run_predict()

        self.Get_Leaf_Images.setEnabled(True)
        self.get_distance.setDisabled(True)
        # show images
        pixmap_RGB_Left = QPixmap("./img/RGB_LEFT_{:0>3d}.png".format(MainWindow.id_ZED))
        pixmap_RGB_Right = QPixmap("./img/RGB_RIGHT_{:0>3d}.png".format(MainWindow.id_ZED))
        pixmap_Trunk_detect_res = QPixmap("./img_out/RGB_trunk_predicted_{:0>3d}.png".format(MainWindow.id_ZED))
        pixmap_Distance_map = QPixmap("./deepmap/Distance_{:0>3d}.png".format(MainWindow.id_ZED))

        self.RGB_Left.setPixmap(pixmap_RGB_Left.scaled(self.RGB_Left.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.RGB_Right.setPixmap(pixmap_RGB_Right.scaled(self.RGB_Right.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.Trunk_detect_res.setPixmap(
            pixmap_Trunk_detect_res.scaled(self.Trunk_detect_res.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.Distance_map.setPixmap(
            pixmap_Distance_map.scaled(self.Distance_map.size(), aspectRatioMode=Qt.KeepAspectRatio))
        MainWindow.id_ZED += 1
        MainWindow.identifier += 1
        MainWindow.id_predict += 1
        with open('id.txt', 'w') as file:
            file.write(f'id={MainWindow.id_predict}')

        self.opencam()
        time.sleep(0.5)

    @pyqtSlot()
    def on_Get_Leaf_Images_clicked(self):
        self.rod_HKcam_ctrl(GNSS, v_rod)
        self.Rod_Return.setEnabled(True)
        # show images
        pixmap_image_1 = QPixmap("./HKCam_imgs/" + a1 + ".jpg")
        pixmap_image_2 = QPixmap("./HKCam_imgs/" + a2 + ".jpg")
        pixmap_image_3 = QPixmap("./HKCam_imgs/" + a3 + ".jpg")
        self.RGB_1.setPixmap(pixmap_image_1.scaled(self.RGB_1.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.RGB_2.setPixmap(pixmap_image_2.scaled(self.RGB_2.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.RGB_3.setPixmap(pixmap_image_3.scaled(self.RGB_3.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.Analyze_Current.setEnabled(True)
    @pyqtSlot()
    def on_Analyze_Current_clicked(self):


        self.textBrowser.append("Images inferring...")
        QApplication.processEvents()

        subprocess.run(["python", "mmsegmentation/disease_segment.py"])

        pixmap_image_a = QPixmap("./seg_img/" + "seg-" + a1 + ".jpg")
        pixmap_image_b = QPixmap("./seg_img/" + "seg-" + a2 + ".jpg")
        pixmap_image_c = QPixmap("./seg_img/" + "seg-" + a3 + ".jpg")
        self.Detect_res_1.setPixmap(pixmap_image_a.scaled(self.Detect_res_1.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.Detect_res_2.setPixmap(pixmap_image_b.scaled(self.Detect_res_1.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.Detect_res_3.setPixmap(pixmap_image_c.scaled(self.Detect_res_1.size(), aspectRatioMode=Qt.KeepAspectRatio))
        self.textBrowser.append("Images inference has completed.")
        QApplication.processEvents()

    @pyqtSlot()
    def on_Rod_Return_clicked(self):

        self.closecam()

        with open("trunk_distance.txt", "w") as f:
            f.write("")
        self.textBrowser.append("Rod returning...")
        QApplication.processEvents()
        board.digital[in1].write(1)
        board.digital[in2].write(0)
        time.sleep(15.5)
        board.digital[in1].write(0)
        board.digital[in2].write(0)
        time.sleep(0.5)
        with open("t_rod.txt", "w") as f:
            f.write("")
        self.textBrowser.append("Rod has returned.")
        QApplication.processEvents()
        subprocess.run(["python", "movefiles.py"])
        self.get_distance.setEnabled(True)
        self.Get_Leaf_Images.setDisabled(True)
        self.Rod_Return.setDisabled(True)
        self.Analyze_Current.setDisabled(True)

    @pyqtSlot()
    def on_Analyze_All_clicked(self):
        # TODO: Not complete yet. This feature will be added in future versions.
        pass
    
    @pyqtSlot()
    def on_Generate_Heat_Map_clicked(self):
        # TODO: Not complete yet. This feature will be added in future versions.
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())