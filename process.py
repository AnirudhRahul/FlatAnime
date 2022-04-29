from turtle import bgcolor
import cv2
import numpy as np
import glob

data = glob.glob("./data/*")
data.sort()


for index in range(0, len(data),2):
    ground = cv2.imread(data[index],-1)
    if ground.shape[-1]==4:
        ground[ground[:,:,-1]==0,:]=0
        ground = cv2.cvtColor(ground, cv2.COLOR_BGRA2BGR)


    flat = cv2.imread(data[index+1])
    baseName = data[index].split('/')[-1].split('.')[0]
    print(baseName, data[index], data[index+1])

    groundHeight, groundWidth ,_ = ground.shape
    flatHeight, flatWidth ,_ = flat.shape


    desiredHeight = desiredWidth = 1024
    
    ground_resized = cv2.resize(ground, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)
    cv2.imwrite(f'formatted/view/{baseName}.png', ground_resized)
    ground = ground_resized

    if abs(flatHeight/flatWidth - groundHeight/groundWidth) < 0.01:
        flat_resized = cv2.resize(flat, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)
        cv2.imwrite(f'formatted/view/{baseName}_flat.png', flat_resized)
        continue

    print(flatHeight/flatWidth , groundHeight/groundWidth)

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

        thresh = cv2.Canny(img,0,255)
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

    def get_bg_color(rect, img):
        img = np.copy(img)
        (x,y,w,h) = rect
        img[y:y+h, x:x+w] = (255,255,255)
        # print(img.shape, rect)
        count = bincount_app(img)
        return count
    flat_bounding_rect = getBoundingRect(flat)
    _, _, fw, fh = flat_bounding_rect

    if fw == flatWidth and fh == flatHeight:
        flat_resized = cv2.resize(flat, (desiredWidth, desiredHeight), interpolation= cv2.INTER_LINEAR_EXACT)
        cv2.imwrite(f'formatted/view/{baseName}_flat.png', flat_resized)
        continue

    flat_bg_color = get_bg_color(flat_bounding_rect, flat)
    # flat_bg_color = (256, 256, 256)
    bg_pixels = np.all(flat[:,:]==np.array(flat_bg_color), axis=2)
    keyed_flat = np.copy(flat)
    keyed_flat[bg_pixels]=(255,255,255)
    flat_bounding_rect = getBoundingRect(keyed_flat)


    resized_flat = np.zeros((desiredHeight,desiredWidth,3), np.uint8)
    resized_flat[:,:] = flat_bg_color 

    (x,y,cropW,cropH) = flat_bounding_rect
    cropped = flat[y:y+cropH,x:x+cropW]



    ground_bounding_rect = getBoundingRect(ground)
    # drawBoundingRect(ground_bounding_rect, ground)


    (x,y,w,h) = ground_bounding_rect

    if groundWidth > groundHeight:
        desiredWidth = min(groundWidth, 1280)
        desiredHeight = round( (groundHeight / groundWidth) * desiredWidth)
    else:
        desiredHeight = min(groundHeight, 1280)
        desiredWidth = round( (groundWidth / groundHeight) * desiredHeight)


    crop_resized = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR_EXACT)

    resized_flat[y:y+h,x:x+w] = crop_resized

    cv2.imwrite(f'formatted/view/{baseName}_flat.png', resized_flat)



# cv2.waitKey(0)