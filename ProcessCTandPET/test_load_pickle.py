import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np

with open(r'E:\training data\3D volume suv0-5(resize_128+128)\ct volume\00005.pkl', 'rb') as f:
    ct_arrs = pkl.load(f)
ct_arrs = ct_arrs.reshape(128, 128, 64)
ct_arrs = ct_arrs.transpose([2, 0, 1])


plt.figure('ct_slice')
plt.imshow(ct_arrs[:, 64, :], cmap='gray')

plt.show()