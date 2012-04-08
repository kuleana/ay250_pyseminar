README for AY250 Homework #3

Katherine de Kleer
2/21/12

>run classify

To train & test on the same directory & calculate metrics:
>classifier(test='path/50_categories')

To train and then test on validation set & output predicted categories:
>classifier(test='path/50_categories',target='path/validation',validate=True)

NOTE: This takes 30-45 minutes each time. If desired, you can set keyword 'quick=True' in the call to classifier, and this will cause it to train on only the first few files in each category and ignore the rest. Obviously it doesn't work very well in this mode...

PATHS NOTE: training path expects a directory with many subdirectories titled with category names. Validation path expects one directory with all validation images.

example output:
>Three Most Important Features:
>1. Aspect Ratio
>2. Total Number of Pixels
>3. Fraction of Edges in Vertical Orientation
>26% Good Predictions from Random Forest
>2% Good Predictions from Random Guessing

