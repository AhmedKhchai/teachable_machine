# Teachable Machine

## How to run the project
 ```python simple_calculation.py```
 ```python chained_calculation.py```

## How the code works:
The code uses the webcam to capture the frames and then it uses the model to predict the sign.
### simple_calculation.py
**How to use:**
First display the sign of the operator that you want to use then press S to start the recording of the frames.
Throught out a period of time we collect the class names (frames) that are not operators and take the one that is most common and with the highest confidence score then we use the operator that is read.
After Pressing S you need to display the sign of the number that you want to use, when the max number of frames is reached we take the most common class name and with the highest confidence score and we use it as a number 1. 
You can confirm the number by typing Y or R to restart the process or C to continue and read the second number.
### chained_calculation.py
**How to use:**
I took the same aproach as the simple_calculation.py but I replaced the the operator variable with a list of operators and i check the length of the operators and elements (numbers to be calculated).
(WIP)
## What happens when you run the project
Press S to start the recording of the frames 
Make the one of these signs + / * 