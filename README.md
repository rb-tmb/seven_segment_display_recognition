# Analyzing Images to get Readings from Seven Segment Display

Using the method from [pyimagesearch](https://pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/) by Adrian Rosebrock using OpenCV techniques to recognize values from a 7 segment display, I have added a method for recognizing 1 also properly, after the recognition the values can be saved to a excel sheet and plotted for visualization.

Here the images are from a multimeter reading current drawn by a Quadrotor during operation.

The dictionary for recognizing the digits is based on this numbering system,



Also seven can appear like the images below depending on the display, hence 7 has 2 entries in the dictionary


