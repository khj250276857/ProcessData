
# coding: utf-8

import numpy as np
# 加载需要的包
# import SimpleITK as sitk
import pydicom as dicom
# matplotlib.use('Agg')
import scipy.misc
import scipy.ndimage
import cv2

# 编码方式

#blob detection 相关包

# 初始化本地信息,数据放在移动硬盘上，case0为pet文件地址，case1为ct文件位置。在项目文件夹下的淋巴瘤子文件夹和淋巴瘤2017文件夹
# 中的结构有所不同
# 使用format表达式更加优雅
# name='唐丽霞'
# case_path0=r'H:\PET-CT淋巴瘤项目\淋巴瘤\唐丽霞\xpdata\pet'.format(name)
# case_path1=case_path0.replace('pet',"ct")

# 文件保存路径

# In[4]:

#重采样函数，以便于配准pet和ct
def resample(image, scan, new_spacing=(1, 1, 1)):
    # Determine current pixel spacing

    spacing = map(float, ([scan.PixelSpacing[0], scan.PixelSpacing[1], scan.SliceThickness]))

    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing

    new_real_shape = image.shape * resize_factor

    new_shape = np.round(new_real_shape)

    real_resize_factor = new_shape / image.shape

    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    return image, new_spacing


# ###	SUV	cannot	be	calculated	if	any	of	the	specified	DICOM	attributes	are	missing	or	empty	or	zero

# In[7]:

import os
import time
import datetime


# In[8]:

#定义一个从pet文件夹计算SUV(bw,lbm)的函数
# 定义一个从pet文件夹计算SUV(bw,lbm)的函数
def cal_suv(case_path0, lbm=False):
    '''arg0为pet图像所在文件夹，arg1为True则进行瘦体重的SUV计算,实验中实际计算的是bw'''
    # 读取路径下的pet图像,返回
    PathDicom = os.path.join(case_path0, 'PT')
    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            # if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName, filename))
    # Get ref file
    dic = {}
    for filepath in lstFilesDCM:
        RefDs = dicom.read_file(filepath)
        dic[RefDs.InstanceNumber] = filepath
    # slopes[RefDs.InstanceNumber] = RefDs.get('RescaleSlope')
    # intercept[RefDs.InstanceNumber] = RefDs.RescaleIntercept
    # 文件数目
    lenf = len(dic)
    # 文件维度
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
    ArrayDicom = np.zeros(ConstPixelDims, dtype=np.float32)
    maxv = []
    for i in range(lenf):
        ds = dicom.read_file(dic[(i + 1)], force=True)
        x = ds[0x0054, 0x0016].value
        # 核素半衰期，单位为秒
        halflife = x[0][0x0018, 0x1075].value
        # 获取时间和序列时间应该相同也就是，scanDate andTime=SeriesDate and Time
        SeriesDate = ds[0x0008, 0x0021]
        # ds[0x0008,0x0031]获取时间和序列时间的具体时间，时分秒
        AcquisitionDate = ds[0x0008, 0x0022]
        startTime = time.strptime(ds[0x0008, 0x0021].value + x[0][0x0018, 0x1072].value[0:6], '%Y%m%d%H%M%S')
        startTime = datetime.datetime(*startTime[:6])
        # decay	Time	=	scan	Time	– start Time	 //	seconds
        SeriesTime = time.strptime(ds[0x0008, 0x0022].value + ds[0x0008, 0x0031].value[0:6], '%Y%m%d%H%M%S')
        SeriesTime = datetime.datetime(*SeriesTime[:6])
        decayTime = SeriesTime - startTime
        decayTime.seconds

        injectedDose = x[0][0x0018, 0x1074].value
        # decayed	Dose	=	injected	Dose	*	pow (2,	-decay	Time	/	half	life)
        decayedDose = injectedDose * pow(2, -decayTime.seconds / halflife)
        # weight	=	Patient's	Weight	(0x0010,0x1030) //	in	kg
        weight = ds[0x0010, 0x1030].value
        # 如果使用瘦体重的话
        if lbm == True:
            sex = ds[0x0010, 0x0040].value
            height = ds[0x0010, 0x1020].value
            heightCm = height * 100
            if sex == 'F':
                weight = 1.07 * weight - 148 * (weight / heightCm) ** 2
            else:
                weight = 1.10 * weight - 120 * (weight / heightCm) ** 2
        # SUVbwScaleFactor	=	(weight	*	1000	/	decayed Dose)
        SUVbwScaleFactor = (float(weight) * 1000.0 / decayedDose)
        # 注意此处使用的是suvlbm或者SUVbw，详见前面的weight计算
        SUVbw = (ds.pixel_array * float(ds[0x0028, 0x1053].value) + float(ds[0x0028, 0x1052].value)) * SUVbwScaleFactor
        ArrayDicom[:, :, i] = SUVbw
    # ArrayDicom = normalize(ArrayDicom)
    ArrayDicom = np.clip(ArrayDicom, 0, 5)
    ArrayDicom = ArrayDicom.reshape(1, ArrayDicom.shape[0], ArrayDicom.shape[1], ArrayDicom.shape[2], 1)

    return ArrayDicom

# In[9]:


#处理PET
# ArrayDicom_pet, ds_pet=cal_suv(case_path0)


# In[13]:


#定义一个从路径读取CT并进行重采样的函数
def cal_hu(case_path1):
    PathDicom = os.path.join(case_path1, 'CT')
    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            # if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName, filename))
# 使用pydicom
    dic = {}
    slopes = {}  
    intercept = {}
    for filepath in lstFilesDCM:
        RefDs = dicom.read_file(filepath)
        dic[RefDs.InstanceNumber] = filepath
        slopes[RefDs.InstanceNumber] = RefDs.get('RescaleSlope')
        intercept[RefDs.InstanceNumber] = RefDs.RescaleIntercept
    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
    ArrayDicom_ct= np.zeros(ConstPixelDims, dtype=np.float32)
    # loop through all the DICOM files
    for i in range(len(lstFilesDCM)):
    # read the file根据实际情况调整
        ds_ct = dicom.read_file(dic[i + 1], force=True)
    # store the raw image data
        ArrayDicom_ct[:, :, i] = slopes[i + 1]*ds_ct.pixel_array+intercept[i + 1]
    ArrayDicom_ct = np.clip(resize(ArrayDicom_ct), -90, 300)
    ArrayDicom_ct = ArrayDicom_ct.reshape(1, ArrayDicom_ct.shape[0], ArrayDicom_ct.shape[1], ArrayDicom_ct.shape[2], 1)

    return ArrayDicom_ct
# In[14]:

# ArrayDicom_ct,ds_ct = cal_hu(case_path1)
# In[15]:


#重采样函数，以便于配准pet和ct
def resample_ct(image, scan, scan_pet, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing

    spacing = map(float, ([scan.PixelSpacing[0], scan.PixelSpacing[1], scan_pet.SliceThickness]))

    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing

    new_real_shape = image.shape * resize_factor

    new_shape = np.round(new_real_shape)

    real_resize_factor = new_shape / image.shape

    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    return image, new_spacing

def cal_pt(path):
    pt_files = [os.path.join(path, _) for _ in os.listdir(path)]
    pt_array = np.array([dicom.read_file(pt_file).pixel_array for pt_file in pt_files], dtype='float32')
    pt_array = pt_array.transpose((1, 2, 0))

    return pt_array

def resize(input_array):
    output_array = []
    for i in range(input_array.shape[2]):
        output_array.append(cv2.resize(input_array[:, :, i], (128, 128), interpolation=cv2.INTER_CUBIC))
    output_array = np.array(output_array, dtype='float32')
    output_array = output_array.transpose((1, 2, 0))
    return output_array


def normalize(input_array):
    # input_array = (input_array - np.mean(input_array)) / np.std(input_array)
    input_array = (input_array - np.min(input_array)) / (np.max(input_array) - np.min(input_array))
    return input_array

# In[8]:


# #重采样SUV,[1,1, ds.SliceThickness],将ArrayDicom的数据类型设成浮点型会使得
# #重采样过程十分的困难
# pet_resampled, spacing = resample(ArrayDicom_pet, ds_pet)
#
#
# #进行zoom的好处是可以使用相应的CT数据特征了
# pet_resampled[pet_resampled<0]=0#此处的阈值是用3d slicer的liver suv uptake measurement来获取的
# pet_resampled[pet_resampled>=ArrayDicom_pet.max()]=ArrayDicom_pet.max()
#
# # 取设备成像中心区域，以便于和CT采样完成的数据相互对齐
# pet = pet_resampled[100:600, 100:600, :]
#
# #查看维度
# print(pet.shape)
#
# #查看片间距
# print(ds_pet[0x0018,0x0050].value)
#
# #保存下结果，一边以后使用
# if not os.path.isdir(name):
#     os.mkdir(name)
# np.save('{}/pet.npy'.format(name),pet)
#
#
# # In[16]:
#
#
# #重采样RefDs.SliceThickness,注意voxel spacing。
# pix_resampled, _ = resample_ct(ArrayDicom_ct, ds_ct, ds_pet,[1, 1,1])
#
#
# # In[17]:
#
#
# ct=pix_resampled
#
#
# # In[18]:
#
#
# np.save('{}/ct.npy'.format(name),ct)


# //	SUV	cannot	be	calculated	if	any	of	the	specified	DICOM	attributes	are	missing	or	empty	or	zero
# if	Corrected	Image	(0x0028,0x0051)	contains	ATTN	and	DECAY	and	Decay	Correction	(0x0054,0x1102)	is	START	{
# if	Units	(0x0054,0x1001)	are	BQML	{
# half	life	=	Radionuclide	Half	Life	(0x0018,0x1075)	in	Radiopharmaceutical	Information	Sequence	(0x0054,0x0016) //	seconds
# if	Series	Date	(0x0008,0x0021)	and	Time	(0x0008,0x0031) are	not	after	Acquisition	Date	(0x0008,0x0022)	and	Time	(0x0008,0x0032)		{
# scan	Date	and	Time	=	Series	Date	and	Time
# start	Time	=	Radiopharmaceutical	Start	Time	(0x0018,0x1072)	in	Radiopharmaceutical	Information	Sequence	(0x0054,0x0016)	
# //	start Date	is	not	explicit	…	assume	same	as	Series	Date;	but	consider	spanning	midnight
# decay	Time	=	scan	Time	– start Time	 //	seconds
# //	Radionuclide	Total	Dose is	NOT	corrected	for	residual	dose	in	syringe,	which	is	ignored	here	…
# injected	Dose	=	Radionuclide	Total	Dose	(0x0018,0x1074)	in	Radiopharmaceutical	Information	Sequence	(0x0054,0x0016) //	Bq
# decayed	Dose	=	injected	Dose	*	pow (2,	-decay	Time	/	half	life)
# weight	=	Patient's	Weight	(0x0010,0x1030) //	in	kg
# SUVbwScaleFactor	=	(weight	*	1000	/	decayed Dose)
# //	Rescale	Intercept	is	required	to	be	0	for	PET,	but	use	it	just	in	case
# //	Rescale	slope	may	vary	per	slice	(GE),	and	cannot	be	assumed	to	be	constant	for	the	entire	volume	
# SUVbw	=	(stored	pixel	value	in	Pixel	Data	(0x7FE0,0x0010)	*	Rescale	Slope	(0x0028,0x1053) +	Rescale	Intercept	(0x0028,0x1052)) *	SUVbwScaleFactor
# //	g/ml
