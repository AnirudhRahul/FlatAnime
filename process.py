from turtle import bgcolor
import cv2
import numpy as np
import glob

data = glob.glob("./keyed_data/*")
data.sort()
print(data)

def mult_mask(img, mask):
    return img*mask[:,:,None]


def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersect(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return False # or (0,0,0,0) ?
    return (x, y, w, h)

def getBoundingRect(img):
    thresh = cv2.Canny(np.uint8(img),0,255)
    # cv2.imshow('edges', thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # drawn = np.copy(img)
    # cv2.drawContours(drawn, contours, -1, color=(200,0,0), thickness=2)
    # cv2.imshow('contours', drawn)

    rect_set=[]
    for contour in contours:
        rect = cv2.boundingRect(contour)
        if len(rect_set)==0:
            rect_set.append(rect)
        else:
            new_set = [rect]
            for seen_rect in rect_set:
                used = False
                for i, new_rect in enumerate(new_set):
                    if intersect(seen_rect, new_rect):
                        new_set[i] = union(seen_rect, new_rect)
                        used = True
                        break
                if not used:
                    new_set.append(seen_rect)
            rect_set = new_set
    # drawBoundingRects(rect_set, img)
    # cv2.imshow('rects', img)
    # cv2.waitKey(0)
    bounding_rect = max(rect_set, key= lambda x: x[-1] * x[-2])
    return bounding_rect

def drawBoundingRects(rects, img):
    if not type(rects)==list:
        rects = [rects]
    for (x,y,w,h) in rects:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)

def bincount_app(a):
    a2D = a.reshape(-1,a.shape[-1])
    a2D = a2D[np.any(a2D != 255, axis = 1), :]
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)

def get_bg_color(img, rect=(0,0,0,0)):
    img = np.copy(img)
    (x,y,w,h) = rect
    img[y:y+h, x:x+w] = (255,255,255)
    # print(img.shape, rect)
    count = bincount_app(img)
    return count

def show_rect(name, img, rect):
    (x,y,w,h) = rect
    cv2.imshow(name, cv2.rectangle(img, (x,y), (x+w, y+h),(255,0,0),5))
    cv2.waitKey(0)

for index in range(0, len(data),2):
    ground = cv2.imread(data[index],-1)
    flat = cv2.imread(data[index+1])
    baseName = data[index].split('/')[-1].split('.')[0]
    print(baseName, data[index], data[index+1])

    # Reformat ground img if it has alpha channel
    mask = None
    if ground.shape[-1]==4:
        mask = ground[:,:,-1]==0
        ground[mask,:] = 0
        mask = np.where(mask,0,1).astype(np.uint8)
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        ground = cv2.cvtColor(ground, cv2.COLOR_BGRA2BGR)
    groundHeight, groundWidth ,_ = ground.shape
    flatHeight, flatWidth ,_ = flat.shape

    if mask is None:
        mask = np.ones((groundHeight, groundWidth), dtype=np.uint8)


    # desiredHeight = desiredWidth = 1024
    # mask = cv2.resize(mask, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)

    # ground_resized = cv2.resize(ground, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)
    # ground_resized = mult_mask(ground_resized, mask)
    # cv2.imwrite(f'formatted/view/{baseName}.png', ground_resized)
    # masked_ground = mult_mask(ground, mask)

    
        
    
    # def remove_bg(img, color):
    #     color = np.array(list(color))
    #     # print(color)
    #     # print(img[:,:])
    #     img[np.all(img[:,:]==color, axis=2)] = (255,255,255)
    #     return img

    # if abs(flatHeight/flatWidth - groundHeight/groundWidth) < 0.01:
    #     flat_resized = cv2.resize(flat, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)
    #     flat_resized = mult_mask(flat_resized, mask)
    #     cv2.imwrite(f'formatted/view/{baseName}_flat.png', flat_resized)
    #     continue

    flat_rect = getBoundingRect(flat)
    ground_rect = getBoundingRect(ground)
    # _, _, fw, fh = flat_bounding_rect
    # show_rect("flat", flat, flat_rect)
    # show_rect("ground", ground, ground_rect)

    # flat_bg_color = get_bg_color(flat, rect=flat_rect)
    # flat_bg_color = (256, 256, 256)
    # bg_pixels = np.all(flat[:,:]==np.array(flat_bg_color), axis=2)
    # keyed_flat = np.copy(flat)
    # keyed_flat[bg_pixels]=(255,255,255)
    # flat_bounding_rect2 = getBoundingRect(keyed_flat)
    # show_rect("keyed_flat", keyed_flat, flat_bounding_rect2)



    
    resized_flat = np.zeros((groundHeight,groundWidth,3), np.uint8)
    resized_flat[:,:] = (0, 0, 0)

    (x,y,cropW,cropH) = flat_rect
    crop = flat[y:y+cropH,x:x+cropW]

    x, y, target_cropW, target_cropH = ground_rect
    resized_crop = cv2.resize(crop, (target_cropW, target_cropH), interpolation=cv2.INTER_LINEAR_EXACT)
    
    resized_flat[y:y+target_cropH,x:x+target_cropW] = resized_crop
    resized_flat = mult_mask(resized_flat, mask)
    ground = mult_mask(ground, mask)

    cv2.imwrite("aligned/{baseName}_flat.png", cv2.resize(resized_flat, (512, 512), interpolation=cv2.INTER_LINEAR_EXACT))
    cv2.imwrite("aligned/{baseName}.png", cv2.resize(ground, (512, 512), interpolation=cv2.INTER_LINEAR_EXACT))
