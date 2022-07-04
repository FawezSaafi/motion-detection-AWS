import time
import classifier
from classifier import detection, OpenCV

MODULE_PATH = r"C:\Users\21658\anaconda3\Lib\site-packages\cv2\__init__.py"
MODULE_NAME = "cv2"
OpenCV.import_layer(MODULE_PATH, MODULE_NAME)
import cv2
#convertir le video fullhd en hd
def resize(image,verif):
    # taille de l'image
    height = image.shape[0]
    width = image.shape[1]

    if(verif==True)and(width,height != 1280,720):
        return cv2.resize(image,(620,720), interpolation=cv2.INTER_AREA)

def analyseVideoClip(path, ClipPath, fileName, output_fileName, CSVPath, bigVideoOut, bMake_Output_fileName,
                         bMAke_bigVideoOut):
    print(ClipPath)

    # variable a remplir
    var_nbOccurenceFound = 0
    var_area_min = 0
    var_area_max = 0
    var_height_min = 0
    var_height_max = 0

    cap = cv2.VideoCapture(ClipPath)

    ret, frame1 = cap.read()
    frame1 = resize(frame1,ret)
    #print(ret)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # taille de l'image
    total_height = frame1.shape[0]
    total_width = frame1.shape[1]

    if bMake_Output_fileName == True:
        # Define the codec and create VideoWriter object
        out = cv2.VideoWriter(output_fileName, cv2.VideoWriter_fourcc(*"mp4v"), 8, (total_width, total_height), True)

    # elimination de la date avec une bande blanche
    x1 = int(50 / 720 * total_height)
    y1 = int(40 / 1280 * total_width)
    x2 = int(590 / 720 * total_height)
    y2 = int(80 / 1280 * total_width)
    cv2.rectangle(gray1, (x1, y1), (x2, y2), (255, 255, 255), -1)

    # flouter l'image
    gray1 = cv2.GaussianBlur(gray1, (31, 31), 0)
    ret, frame2 = cap.read()
    frame2 = resize(frame2,ret)
    start_time = time.time()
    while ret:

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        # elimination de la date
        cv2.rectangle(gray2, (x1, y1), (x2, y2), (255, 255, 255), -1)

        # flouter l'image
        gray2 = cv2.GaussianBlur(gray2, (31, 31), 0)
        frame2 = resize(frame2, ret)
        gray1=resize(gray1,ret)
        gray2=resize(gray2,ret)

        frame, detected = detection.frame_draw_detections(frame2, gray1, gray2)

        ##########################################################################
        ##  ecriture info sur l'image
        text = fileName + " [" + str(var_nbOccurenceFound) + "]"
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # fontScale
        font_scale = 1
        # Line thickness of 2 px
        thick_ness = 2
        # set the rectangle background to white
        rectangle_bgr = (255, 255, 255)
        # get the width and height of the text box
        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=thick_ness + 1)[0]
        # set the text start position
        text_offset_x = 50
        text_offset_y = 110
        # make the coords of the box with a small padding of two pixels
        box_coords = (
        (text_offset_x, text_offset_y + 8), (text_offset_x + text_width + 2, text_offset_y - text_height - 8))
        cv2.rectangle(frame, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)

        # Blue color in BGR
        color = (255, 0, 0)

        frame = cv2.putText(frame, text, (text_offset_x, text_offset_y), font, font_scale, color, thick_ness,
                            cv2.LINE_AA)
        ##########################################################################

        # cv2.imshow("Output4", frame)

        # write the modified frame
        if bMake_Output_fileName == True:
            out.write(frame)

        #if bMAke_bigVideoOut == True:
            #bigVideoOut.write(frame)

        if cv2.waitKey(1) == 27:  # exit on ESC
            break

        frame1 = frame2
        gray1 = gray2
        ret, frame2 = cap.read()
        #frame2=resize(frame2,ret)
        if detected == True:
            time.sleep(0.0)
            var_nbOccurenceFound = var_nbOccurenceFound + 1
        else:
            time.sleep(0.0)

    print('Classifier nbOccurenceFound result : ',var_nbOccurenceFound)
    # occ=
    # print("--- %s seconds ---" % (time.time() - start_time))
    cv2.destroyAllWindows()
    #fichier = open(CSVPath, "a")
    # fichier.write(fileName + ";" + str(var_nbOccurenceFound) + "\n")
    #fichier.close()

    if bMake_Output_fileName == True:
        out.release()

    return var_nbOccurenceFound