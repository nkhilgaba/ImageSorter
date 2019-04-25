# ImageSorter
A Python script to find out people in a bunch of images and sort their potraits into respective directories

## Requirements
```
pip install face-recognition
```
## Working
Checks all the images present in the sub-directory **img** one by one, makes an index of the number of faces 
found in the respective image. After indexing all the image files, if any potraits are found, they are moved to 
new directories for each face recognized, displaying who's present in which image files and total number of different faces
found in all the images.

![](res/Sorter.gif)
