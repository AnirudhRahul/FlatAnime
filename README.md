# FlatAnime
 
Put examples of paired data in the ```/keyed_data``` folder with the format ```basename.ext``` and ```basename_flat.ext```

Dependencies  needed include ```openCV, Pillow, torchvision```

Run ```process.py``` to properly mask and align the paired data (alignment simply tries to match up the bounding box of the flat image with the bounding box of the base image) and produce a standardized 512x512 output image in the ```/aligned``` dir

Then run ```format.py``` to extend the dataset via random image transformations such as affine transforms, padding, and hue jitters. 

Be sure to change the output directory for your test/training sets in the last to lines!

Also be sure to create the right subfolders, i.e :
```folderName/in``` and ```folderName/out```
