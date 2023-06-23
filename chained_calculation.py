from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)
operators = []
elements = []
frame_count = 0
increment_frames = False
max_frames = 50  # Number of frames to capture before making a decisio
prediction_dict = {}


def calculate(elements, operators):
    # The first element of the calculation should be the first number
    result = int(elements[0])

    # Now we go through each operator, applying it to the current result
    # and the next element in the elements list.
    for i in range(len(operators)):
        operator = operators[i]
        next_element = int(elements[i+1])

        if operator == "+":
            result += next_element
        elif operator == "-":
            result -= next_element
        elif operator == "*":
            result *= next_element
        elif operator == "/":
            if next_element != 0:
                result /= next_element
            else:
                print("Error: Division by zero.")
                return None
        else:
            print("Invalid operator:", operator)
            return None

    print("Result:", result)
    


while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index].split()[1]
    confidence_score = prediction[0][index]

    print("Class:", class_name)
    # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # Start incrementing frames when 's' is pressed
    if keyboard_input == ord("s"):
        increment_frames = True

    # Stop incrementing frames when 'e' is pressed
    if keyboard_input == ord("e"):
        increment_frames = False

    # print("increment_frames", increment_frames)
    if increment_frames:
        len_elements = len(elements)
        len_operators = len(operators)
        
        if class_name in ["+", "-", "*", "/"] and len_elements - len_operators == 1:
            operators.append(class_name)
            print("operators", operators)

        if class_name not in ["+", "-", "*", "/", "fond"] and len_elements - len_operators == 0:
            if class_name in prediction_dict:
                # Update the class name's score only if the new score is higher
                if confidence_score > prediction_dict[class_name]:
                    prediction_dict[class_name] = confidence_score
            else:
                prediction_dict[class_name] = confidence_score

        frame_count += 1
        if frame_count == max_frames:
            # Find the class name with the highest score
            most_confident_class = max(prediction_dict, key=prediction_dict.get)
            # Reset prediction_dict and frame_count for the next batch of frames
            prediction_dict = {}
            frame_count = 0
            print("most_confident_class", most_confident_class)

            user_input = input(
                "Confirm class (y/n), Retry (r), Continue (c)?: , or Done and calculate (d)"
            )
            if user_input.lower() == "y":
                elements.append(most_confident_class)
            elif user_input.lower() == "r":
                pass
            elif user_input.lower() == "c":
                continue
            elif user_input.lower() == "d":
                calculate(elements, operators)
                break
            else:
                print("Invalid input! Continuing to next class...")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
