import numpy as np
def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def sharp_score(img):
    flattened = img+1
    flattened = flattened.astype(np.uint64)
    flattened = flattened[:,:,0] + 257*flattened[:,:,1] + 257*257*flattened[:,:,2]
    return len(np.unique(flattened))



import fid.fid_score as score
# Note fid code comes from:
# https://github.com/mseitzer/pytorch-fid
def run_fid(imgPathA, imgPathB):
    fid_score = score.calculate_fid_given_paths([imgPathA, imgPathB])
    return fid_score


run_fid("./flat_data")