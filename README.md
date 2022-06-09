# FlatAnime
*Anime Image translation to Minimalist Theme* by Anirudh Rahul

The current image to image machine learning models such as style transfer models, seem to have promising applications in the arts. The goal of this project to apply traditional image to image learning methods on novel anime image dataset, to speicfically study the effectiveness of different image to image techniques for anime style images.


## Preliminary Results
| Input | Output | Ground |
| --- | --- | --- |
| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/luffy_real_A.png)| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/luffy_fake_B.png)|![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/luffy_real_B.png)|
| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/kakashi_side_look_real_A.png) | ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/kakashi_side_look_fake_B.png)| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/kakashi_side_look_real_B.png)|
| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/ll4_real_A.png) | ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/ll4_fake_B.png)| ![](https://github.com/AnirudhRahul/FlatAnime/blob/03cb4568b5a5f3a74bfae1b837e1ea15209437e2/results/unet+extended_b8_epoch_250/ll4_real_B.png)|



## Dataset Creation

In order to create a paired anime image dataset I had scrape the internet for exact pairs of anime and minimalist anime images, and then somehow align both these images.

To make finding exact image pairs easier, I decided to start searching for minimalist images on art forums such as Pixiv, and DeviantArt using tags such as minimalistflatdesign, and minimalistanime, since artists on these forums typically linked the source images for their minimalist drawings in their descriptions. 


In order to align the discovered pairs I used the alignment pipeline shown below

![pipeline-white](https://user-images.githubusercontent.com/14942461/172778512-35bfa988-ba85-4236-98fd-5aa021c76c71.png)
![boundingbox-white](https://user-images.githubusercontent.com/14942461/172778386-cb7ce8b6-acde-4f25-a0cf-b243f5cbbd5f.png)



## Development Notes
Put examples of paired data in the ```/keyed_data``` folder with the format ```basename.ext``` and ```basename_flat.ext```

Dependencies  needed include ```openCV, Pillow, torchvision```

Run ```process.py``` to properly mask and align the paired data (alignment simply tries to match up the bounding box of the flat image with the bounding box of the base image) and produce a standardized 512x512 output image in the ```/aligned``` dir

Then run ```format.py``` to extend the dataset via random image transformations such as affine transforms, padding, and hue jitters. 

Be sure to change the output directory for your test/training sets in the last to lines!

Also be sure to create the right subfolders, i.e :
```folderName/in``` and ```folderName/out```
