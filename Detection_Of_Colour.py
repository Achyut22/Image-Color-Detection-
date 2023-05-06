import cv2
import pandas as pd   #Panda Library is Used to read the dataset which is in the form of a CSV file

img_path = r'C:\Users\Achyut Tiwari\PycharmProjects\Image_Colour_Detection\test_image.jpg'  #Path of image is specified here
img = cv2.imread(img_path)   # Image is read from cv2.imread() an dis stored in img

clicked = False                      # Global variable used
r = g = b = x_pos = y_pos = 0        # Global variable used

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(r'C:\Users\Achyut Tiwari\PycharmProjects\Image_Colour_Detection\Colours_dataset.csv',encoding='latin1', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):   #To move through all row values in the dataset
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:      #By this we would get the closest match to the colour pointed by the pointer
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse single left click
def draw_function(input, x, y, flags, param):
    if input == cv2.EVENT_LBUTTONDOWN:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]  #In openCV language order of colour cahnnels is BGR
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (925, 60), (b, g, r), -1)    #-1 here allows whole rectangle to be filled with respective colour

        # Creating text string to display( Color name and RGB values )
        text = 'Color Name: ' + get_color_name(r, g, b) + ' , R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()