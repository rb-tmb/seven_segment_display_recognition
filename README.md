# Analyzing Images to get Readings from Seven Segment Display

Using the method from [pyimagesearch](https://pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/) by Adrian Rosebrock using OpenCV techniques to recognize values from a 7 segment display, I have added a method for recognizing 1 also properly, after the recognition the values can be saved to a excel sheet and plotted for visualization.

Here the images are from a multimeter reading current drawn by a Quadrotor during operation.

The dictionary for recognizing the digits is based on this numbering system,

![7-segment_numbered](https://user-images.githubusercontent.com/106291484/183712663-c7e4a0fd-fbbf-4817-9a3f-e8de26ffc9d5.png)

Also seven can appear like the images below depending on the display, hence 7 has 2 entries in the dictionary

![7-segment_7_1](https://user-images.githubusercontent.com/106291484/183712697-661de960-0612-46d0-9cfe-02287214cb3f.png)
![7-segment_7_2](https://user-images.githubusercontent.com/106291484/183712733-827032b9-be1e-49c4-80bf-b7840a830016.png)



