# -- coding: utf-8 --

import sys
import copy
import ctypes
import os

from ctypes import *
from CameraParams_const import *
from CameraParams_header import *
from MvCameraControl_header import *
from MvErrorDefine_const import *
from PixelType_const import *
from PixelType_header import *

MvCamCtrldll = ctypes.cdll.LoadLibrary(os.getenv('MVCAM_COMMON_RUNENV') + "/aarch64/libMvCameraControl.so")

class _MV_PY_OBJECT_(Structure):
    pass
_MV_PY_OBJECT_._fields_ = [
    ('PyObject', py_object),
]
MV_PY_OBJECT = _MV_PY_OBJECT_

class MvCamera():

    def __init__(self):
        self._handle = c_void_p()
        self.handle = pointer(self._handle)

    
    @staticmethod
    def MV_CC_GetSDKVersion():
        MvCamCtrldll.MV_CC_GetSDKVersion.restype = c_uint
        return MvCamCtrldll.MV_CC_GetSDKVersion()

    @staticmethod
    def MV_CC_EnumDevices(nTLayerType, stDevList):
        MvCamCtrldll.MV_CC_EnumDevices.argtype = (c_uint, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevices.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumDevices(c_uint(nTLayerType), byref(stDevList))

    def MV_CC_CreateHandle(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandle.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandle.restype = c_uint
        return MvCamCtrldll.MV_CC_CreateHandle(byref(self.handle), byref(stDevInfo))

    def MV_CC_CreateHandleWithoutLog(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.restype = c_uint
        return MvCamCtrldll.MV_CC_CreateHandleWithoutLog(byref(self.handle), byref(stDevInfo))

    def MV_CC_DestroyHandle(self):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        return MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

    def MV_CC_OpenDevice(self, nAccessMode=MV_ACCESS_Exclusive, nSwitchoverKey=0):
        MvCamCtrldll.MV_CC_OpenDevice.argtype = (c_void_p, c_uint32, c_uint16)
        MvCamCtrldll.MV_CC_OpenDevice.restype = c_uint
        return MvCamCtrldll.MV_CC_OpenDevice(self.handle, nAccessMode, nSwitchoverKey)

    def MV_CC_CloseDevice(self):
        MvCamCtrldll.MV_CC_CloseDevice.argtype = c_void_p
        MvCamCtrldll.MV_CC_CloseDevice.restype = c_uint
        return MvCamCtrldll.MV_CC_CloseDevice(self.handle)

    def MV_CC_RegisterImageCallBackEx(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterImageCallBackEx(self.handle, CallBackFun, pUser)

    def MV_CC_StartGrabbing(self):
        MvCamCtrldll.MV_CC_StartGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StartGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StartGrabbing(self.handle)

    def MV_CC_StopGrabbing(self):
        MvCamCtrldll.MV_CC_StopGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StopGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StopGrabbing(self.handle)

    def MV_CC_GetOneFrameTimeout(self, pData, nDataSize, stFrameInfo, nMsec=1000):
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.restype = c_uint
        return MvCamCtrldll.MV_CC_GetOneFrameTimeout(self.handle, pData, nDataSize, byref(stFrameInfo), nMsec)

    def MV_CC_SetImageNodeNum(self, nNum):
        MvCamCtrldll.MV_CC_SetImageNodeNum.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetImageNodeNum.restype = c_uint
        return MvCamCtrldll.MV_CC_SetImageNodeNum(self.handle, nNum)

    def MV_CC_GetIntValue(self, strKey, stIntValue):
        MvCamCtrldll.MV_CC_GetIntValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetIntValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetIntValue(self.handle, strKey.encode('ascii'), byref(stIntValue))
    
    def MV_CC_SetIntValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetIntValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetIntValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetIntValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    def MV_CC_GetEnumValue(self, strKey, stEnumValue):
        MvCamCtrldll.MV_CC_GetEnumValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetEnumValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetEnumValue(self.handle, strKey.encode('ascii'), byref(stEnumValue))

    def MV_CC_SetEnumValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetEnumValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetEnumValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetEnumValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    def MV_CC_SetEnumValueByString(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetEnumValueByString.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetEnumValueByString.restype = c_uint
        return MvCamCtrldll.MV_CC_SetEnumValueByString(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))

    def MV_CC_GetFloatValue(self, strKey, stFloatValue):
        MvCamCtrldll.MV_CC_GetFloatValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFloatValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetFloatValue(self.handle, strKey.encode('ascii'), byref(stFloatValue))

    def MV_CC_SetFloatValue(self, strKey, fValue):
        MvCamCtrldll.MV_CC_SetFloatValue.argtype = (c_void_p, c_void_p, c_float)
        MvCamCtrldll.MV_CC_SetFloatValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetFloatValue(self.handle, strKey.encode('ascii'), c_float(fValue))

    def MV_CC_GetBoolValue(self, strKey, BoolValue):
        MvCamCtrldll.MV_CC_GetBoolValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetBoolValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetBoolValue(self.handle, strKey.encode('ascii'), byref(BoolValue))

    def MV_CC_SetBoolValue(self, strKey, bValue):
        MvCamCtrldll.MV_CC_SetBoolValue.argtype = (c_void_p, c_void_p, c_bool)
        MvCamCtrldll.MV_CC_SetBoolValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetBoolValue(self.handle, strKey.encode('ascii'), bValue)

    def MV_CC_GetStringValue(self, strKey, StringValue):
        MvCamCtrldll.MV_CC_GetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetStringValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetStringValue(self.handle, strKey.encode('ascii'), byref(StringValue))
    
    def MV_CC_SetStringValue(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetStringValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetStringValue(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))
    
    def MV_CC_SetCommandValue(self, strKey):
        MvCamCtrldll.MV_CC_SetCommandValue.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetCommandValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetCommandValue(self.handle, strKey.encode('ascii'))

    def MV_CC_RegisterExceptionCallBack(self, ExceptionCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterExceptionCallBack(self.handle, ExceptionCallBackFun, pUser)

    def MV_CC_RegisterEventCallBackEx(self, pEventName, EventCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.argtype = (c_void_p, c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterEventCallBackEx(self.handle, pEventName.encode('ascii'), EventCallBackFun, pUser)

    def MV_GIGE_ForceIpEx(self, nIP, nSubNetMask, nDefaultGateWay):
        MvCamCtrldll.MV_GIGE_ForceIpEx.argtype = (c_void_p, c_uint, c_uint, c_uint)
        MvCamCtrldll.MV_GIGE_ForceIpEx.restype = c_uint
        return MvCamCtrldll.MV_GIGE_ForceIpEx(self.handle, c_uint(nIP), c_uint(nSubNetMask), c_uint(nDefaultGateWay))
    
    def MV_GIGE_SetIpConfig(self, nType):
        MvCamCtrldll.MV_GIGE_SetIpConfig.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetIpConfig.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetIpConfig(self.handle, c_uint(nType))

    def MV_GIGE_SetTransmissionType(self, stTransmissionType):
        MvCamCtrldll.MV_GIGE_SetTransmissionType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_SetTransmissionType.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetTransmissionType(self.handle, byref(stTransmissionType))

    def MV_CC_SaveImageEx2(self, stSaveParam):
        MvCamCtrldll.MV_CC_SaveImageEx2.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageEx2.restype = c_uint
        return MvCamCtrldll.MV_CC_SaveImageEx2(self.handle, byref(stSaveParam))

    def MV_CC_SaveImageEx3(self, stSaveParam):
        MvCamCtrldll.MV_CC_SaveImageEx3.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageEx3.restype = c_uint
        return MvCamCtrldll.MV_CC_SaveImageEx3(self.handle, byref(stSaveParam))

    def MV_CC_SaveImageToFileEx(self, stSaveFileParam):
        MvCamCtrldll.MV_CC_SaveImageToFileEx.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageToFileEx.restype = c_uint
        return MvCamCtrldll.MV_CC_SaveImageToFileEx(self.handle, byref(stSaveFileParam))

    def MV_CC_ConvertPixelType(self, stConvertParam):
        MvCamCtrldll.MV_CC_ConvertPixelType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_ConvertPixelType.restype = c_uint
        return MvCamCtrldll.MV_CC_ConvertPixelType(self.handle, byref(stConvertParam))

    def MV_CC_ConvertPixelTypeEx(self, stConvertParam):
        MvCamCtrldll.MV_CC_ConvertPixelTypeEx.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_ConvertPixelTypeEx.restype = c_uint
        return MvCamCtrldll.MV_CC_ConvertPixelTypeEx(self.handle, byref(stConvertParam))

    def MV_CC_FeatureSave(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureSave.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureSave.restype = c_uint
        return MvCamCtrldll.MV_CC_FeatureSave(self.handle, pFileName.encode('ascii'))
    
    def MV_CC_FeatureLoad(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureLoad.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureLoad.restype = c_uint
        return MvCamCtrldll.MV_CC_FeatureLoad(self.handle, pFileName.encode('ascii'))

    def MV_CC_FileAccessRead(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessRead.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessRead.restype = c_uint
        return MvCamCtrldll.MV_CC_FileAccessRead(self.handle, byref(stFileAccess))

    def MV_CC_FileAccessWrite(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessWrite.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessWrite.restype = c_uint
        return MvCamCtrldll.MV_CC_FileAccessWrite(self.handle, byref(stFileAccess))

    def MV_CC_GetFileAccessProgress(self, stFileAccessProgress):
        MvCamCtrldll.MV_CC_GetFileAccessProgress.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFileAccessProgress.restype = c_uint
        return MvCamCtrldll.MV_CC_GetFileAccessProgress(self.handle, byref(stFileAccessProgress))

    def MV_CC_GetOptimalPacketSize(self):
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.restype = c_uint
        return MvCamCtrldll.MV_CC_GetOptimalPacketSize(self.handle)

    def MV_CC_HBDecode(self, stDecodeParam):
        MvCamCtrldll.MV_CC_HB_Decode.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_HB_Decode.restype = c_uint
        return MvCamCtrldll.MV_CC_HB_Decode(self.handle, byref(stDecodeParam))

    def MV_CC_GetImageBuffer(self, stFrame, nMsec):
        MvCamCtrldll.MV_CC_GetImageBuffer.argtype = (c_void_p, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageBuffer.restype = c_uint
        return MvCamCtrldll.MV_CC_GetImageBuffer(self.handle, byref(stFrame), nMsec)

    def MV_CC_FreeImageBuffer(self, stFrame):
        MvCamCtrldll.MV_CC_FreeImageBuffer.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FreeImageBuffer.restype = c_uint
        return MvCamCtrldll.MV_CC_FreeImageBuffer(self.handle, byref(stFrame))
