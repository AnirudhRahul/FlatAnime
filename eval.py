import glob as np
import numpy as np
import os
import cv2

def PSNR(path):
    fake_files = sorted(glob.glob(os.path.join(path,"*fake*.png")))
    real_files = sorted(glob.glob(os.path.join(path,"*real_B*.png")))
    if len(fake_files) != len(real_files):
        raise "error"
    
    psnr_list = []
    for fake, real in zip(fake_files, real_files):
        original = cv2.imread(real)
        compressed = cv2.imread(fake)
        mse = np.mean((original - compressed) ** 2)
        if(mse == 0):  # MSE is zero means no noise is present in the signal .
                    # Therefore PSNR have no importance.
            return 100
        max_pixel = 255.0
        psnr_list.append(20 * np.log10(max_pixel / np.sqrt(mse)))
    
    psnr = np.average(np.array(psnr_list))
    print("Average PSNR: ", psnr)
    return psnr
def sharp_score(path):
    fake_files = sorted(glob.glob(os.path.join(path,"*fake*.png")))
    count = []
    for p in fake_files:
        img = cv2.imread(p)
        flattened = img+1
        flattened = flattened.astype(np.uint64)
        flattened = flattened[:,:,0] + 257*flattened[:,:,1] + 257*257*flattened[:,:,2]
        count.append(len(np.unique(flattened)))
    sharp_score = np.average(np.array(count))
    print("Average Sharp: ", sharp_score)
    return sharp_score


import fid.fid_score as score
import glob
# Note fid code comes from:
# https://github.com/mseitzer/pytorch-fid
def run_fid(imgPathA, imgPathB):
    fid_score = score.calculate_fid_given_paths([imgPathA, imgPathB])
    print("FID_score", fid_score)
    return fid_score


# run_fid("./flat_data")

all_results = glob.glob("./results/*")

print(all_results)


for path in all_results:
    name = path.split('/')[-1]
    print(name)
    fid = run_fid(path, './flat_data')
    average_PSNR = PSNR(path)
    average_sharp = sharp_score(path)
    
    res = os.path.join(path, '_results.txt')
    
    with open(res, 'w') as f:
        f.write(f'FID: {fid}\nAverage PSNR: {average_PSNR}\nAverage Sharp: {average_sharp}')