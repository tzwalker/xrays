# rotating jpg images of NBL3 cross-sections
import numpy as np
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage.transform import rotate



#'Name' strings must correspond to the file name of the screenshot of the cross-seciton
#'Rot' determined from manually loading image file into python, then testing angles using rotate() from skimage
    #be sure to import all packages listed above if running soley from command line:
        #img = io.imread(path_to_image_file*)
        #io.imshow()
        #rotate(img, deg*)
        #'enter determined rotation into corresponding sample dictionary'
    
#'depth' are number of microns guessed from jpg
#'pixels' are exact; used third party screen shot software PicPick to capture presecise screenshots
#"ch_max" is the estmiated maximum value from the cross-section jpg
#"channels" contains the channels of interest; input must match that of the filename sytax, i.e. "Cd" or "Cd_L"
        #"channels" and 'ch_max' lengths should match!
        #adjust the inputs to "channels" if you only want to see certain plots
        
image_path = r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190406 GATAN x-sect imgs\jpgs'

save_path = r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190422 python cross section line plots'

sam1 = {'Name': 'NBL3_1', 'Rot': 0, 'depth': 12, 'depth_pixels': 175, 'channels': ['XBIC', 'Cd', 'Cu'], 'channel_maxes': [6, 1400, 350]}
sam2 = {'Name': 'NBL3_3', 'Rot': 5, 'depth': 17, 'depth_pixels': 200, 'channels': ['XBIC', 'Cd', 'Cu'], 'channel_maxes': [0.9, 1600, 1200]}
sam3 = {'Name': 'TS58A', 'Rot': 0.5, 'depth': 11, 'depth_pixels': 85, 'channels': ['XBIC', 'Cd', 'Cu'], 'channel_maxes': [0.5, 1300, 400]}

samples = [sam1, sam2, sam3]


def rotate_and_integrate_cross_section(samples):
    for sample in samples:
        fig = plt.figure()                                                                  #initialize figure object
        for channel, ch_max in zip(sample['channels'], sample['channel_maxes']):
            image_name = sample['Name'] + "_" + channel                                     #make sure this corresponds to the filename syntax being used
            #print(image_name)
            full_path = image_path + "\\" + image_name + ".jpg" 
            img = io.imread(full_path)
            gry_img = rgb2gray(img)
            rot_gry_img = rotate(gry_img, sample['Rot'])                                    #rotates the picture according to the rotation you determined manually
            column_sum = rot_gry_img.sum(axis=0)                                            #sums the columns of the rotated image matrix, equivalent to integrating
            
            #calibrates line plot x axis
            x = sample['depth']                                                             #get the thickness of the sample (read from original image)
            x_res = sample['depth_pixels']                                                  #get pixels in x of screenshot (read from Windows explorer)
            
            x_calib = np.linspace(0,x,x_res)                                                #generate an array of numbers from xmin to xmax that are spaced by the number of x-pixels in the image (will be used to plot Y against)
            lower_bound = min(x_calib)
            upper_bound = max(x_calib)
            
            #calibrate line plot y axis
            #by default the integration returns a sum of the pixels in a column that corresponds to an intensity 
            #the intensity is determined by rgb2gray() when converting to greyscale
            #the greyscale intensity will be converted to XRF intensity estimated from the ch_max of the cross-section image 
            y_max = max(column_sum)                                                         #gets the maximum intensity from the integration of the rotated image
            channel_calib_factor = ch_max / y_max                                           #get scaling factor that will convert greyscale intenistyto XRF intensity
            scaled_column_sum = column_sum * channel_calib_factor                           #convert             
            
            if channel == 'XBIC':
                units = 'nA'
            else:
                units = 'a.u.'
            
            plt.plot(x_calib, scaled_column_sum)                            
            plt.xlim([lower_bound, upper_bound])
            
            #line plot settings
            plt.title(image_name, fontsize = 18)
            plt.xlabel('X (um)', fontsize = 18)
            plt.xticks(rotation = 0)
            plt.ylabel(channel + ' ' + '(' + units + ')', fontsize = 18)
            plt.yticks(rotation = 0)
            plt.tick_params(axis="both", labelsize = 15)
            
            plt.grid()                      #places gridlines for prettification
            plt.show()                      #push this line to outer loop to make plots of all channels (rememebr to rename plt-titles); push line to inner loop to make individual plots for each channel
            #fig.get_figure()
            #fig.savefig(save_path + r"\{s}, {e}.jpg".format(s = sample["Name"], e = channel))
    return

rotate_and_integrate_cross_section(samples)

# =============================================================================
# #this was written to batch convert color images to greyscale to avoid having to do so manually in DigitialMicrograph (DM) software
# #it works, but the image canno tbe read by DM 
# #error: "sorry, cannot handle contiguous data with PhotometricInterpretation=1 and Samepixels=2"
# #however, the image was about to be opened in GIMP, so it may prove ot be useful at some point
#     
# #img_num generates a numeric indiactor matching the filename (which may change)
# color_imgs_path = r'C:\Users\Trumann\Desktop\solo_images_jpgs'
# gry_img_path = r'C:\Users\Trumann\Desktop\solo_images_jpgs\gray_images'
# 
# img_num = list(range(1,12))
# 
# for img in img_num:
#     #these if statements make sure the corect numeric indicator is used to contruct the filename string
#     if img < 10:
#         img_name = 'image00' + str(img) + '.jpg'                
#         
#     if img >= 10:
#         img_name = 'image0' + str(img) + '.jpg'
#         
#     full_path = color_imgs_path + '\\' + img_name           #find the image
#     img = io.imread(full_path)                              #import image
#     gry_img = rgb2gray(img)                                 #convert image to greyscale
#     sliced_str = img_name[:-4]                              #remove '.jpg' extension from filename (must match that of the file being imported)
#     gry_filename = sliced_str + '.tiff'                     #add '.tiff' extension (or any extension within io.imsave()'s ability)
#     gry_filepath = gry_img_path + '\\' + gry_filename       #go to new location for grey images
#     
#     io.imsave(gry_filepath, gry_img, plugin = 'tifffile') #save grey image
#     print(img_name +  ' saved')
# =============================================================================
    


