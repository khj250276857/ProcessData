import pickle
import matplotlib.pyplot as plt

with open(r'E:\实验数据\shift_10_10.pkl', 'rb') as f:
    ct_arrs = pickle.load(f)

print(type(ct_arrs))
resized_ct_arrs = ct_arrs[0]
shift_ct_arrs = ct_arrs[1]

plt.figure('before')
plt.imshow(resized_ct_arrs[100], cmap='gray')
plt.figure('after')
plt.imshow(shift_ct_arrs[100], cmap='gray')
plt.show()