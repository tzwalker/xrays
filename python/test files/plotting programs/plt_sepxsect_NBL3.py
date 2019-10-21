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

save_path = r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190429 cross section line plots_py'

sam1 = {'Name': 'NBL3_1', 'Rot': 0, 'depth': 12, 'depth_pixels': 175, 'channels': ['XBIC', 'Cd', 'Te','Cu'], 'channel_maxes': [6, 1400, 1400, 350]}
sam2 = {'Name': 'NBL3_3', 'Rot': 5, 'depth': 17, 'depth_pixels': 200, 'channels': ['XBIC', 'Cd', 'Te', 'Cu'], 'channel_maxes': [0.9, 1600,1600, 1200]}
sam3 = {'Name': 'TS58A', 'Rot': 0.5, 'depth': 11, 'depth_pixels': 85, 'channels': ['XBIC', 'Cd', 'Te', 'Cu'], 'channel_maxes': [0.5, 1300,1300, 400]}

# quick-and-dirty export Cu and XBIC line profiles to CSVs for PVSC poster 
# =============================================================================
# sam1 = {'Name': 'NBL3_1', 'Rot': 0, 'depth': 12, 'depth_pixels': 175, 'channels': ['XBIC', 'Cu'], 'channel_maxes': [6, 350]}
# sam2 = {'Name': 'NBL3_3', 'Rot': 5, 'depth': 17, 'depth_pixels': 200, 'channels': ['XBIC', 'Cu'], 'channel_maxes': [0.9, 1200]}
# =============================================================================


samples = [sam1, sam2]#, sam3]


def rotate_and_integrate_cross_section(samples):
    master_list = []
    for sample in samples:
        channel_list = []
        for channel, ch_max in zip(sample['channels'], sample['channel_maxes']):
            image_name = sample['Name'] + "_" + channel                                     #make sure this corresponds to the filename syntax being used
            #print(image_name)
            full_path = image_path + "\\" + image_name + ".jpg" 
            img = io.imread(full_path)
            gry_img = rgb2gray(img)
            rot_gry_img = rotate(gry_img, sample['Rot'])                                    #rotates the picture according to the rotation you determined manually
            column_sum = rot_gry_img.sum(axis=0)                                            #sums the columns of the rotated image matrix, equivalent to integrating
            #calibrate line plot y axis
            #by default the integration returns a sum of the pixels in a column that corresponds to an intensity 
            #the intensity is determined by rgb2gray() when converting to greyscale
            #the greyscale intensity will be converted to XRF intensity estimated from the ch_max of the cross-section image 
            #the below lines are only necessary when manually reading values from colorscale of the jpg image
            y_max = max(column_sum)                                                         #gets the maximum intensity from the integration of the rotated image
            channel_calib_factor = ch_max / y_max                                           #get scaling factor that will convert greyscale intenisty to XRF intensity
            scaled_column_sum = column_sum * channel_calib_factor                           #convert 
            channel_list.append(scaled_column_sum)
        master_list.append(channel_list)
    return master_list

master_list = rotate_and_integrate_cross_section(samples)

def plot_save_combined_channels(samples, master_list):
    exes = []
    for sample, set_of_lines in zip(samples, master_list):
        #introduce x-axis calibration; convert pixel index to microns
        x = sample['depth']
        x_res = sample['depth_pixels']
        x_calib = np.linspace(0, x, x_res)
        exes.append(x_calib)
        
        lower_bound = min(x_calib)
        upper_bound = max(x_calib)
        
        #for line in set_of_lines: #not sure if this is necessary for the time being... just roll with below for now.
        fig, ax1 = plt.subplots()
        axis_title_size = 20
        tick_size = 16
        line_size = 5
        
        ax1.set_xlabel('Depth (um)', fontsize = axis_title_size)
        ax1.tick_params(axis='x', labelsize = tick_size)
        
        color = 'tab:red'
        lns1 = ax1.plot(x_calib, set_of_lines[0], color=color, label = 'XBIC', linewidth=line_size)      #XBIC line
        ax1.set_ylabel('XBIC (nA)', color=color, fontsize = axis_title_size)
        ax1.tick_params(axis='y', labelcolor=color, labelsize = tick_size)
        
        ax2 = ax1.twinx()
        color2 = 'tab:orange'
        ax2.set_ylabel('Cu XRF (a.u.)', fontsize = axis_title_size)
        ax2.tick_params(axis='y', labelcolor=color2, labelsize = tick_size)
        ax2.set_ylim(0,1300)
# =============================================================================
#         color = 'tab:blue'
#         lns2 = ax2.plot(x_calib, set_of_lines[1], color=color, linestyle = '--', label = 'Cd')  #Cd line
#         ax2.set_ylabel('a.u.', color=color, fontsize = 18)
#         ax2.tick_params(axis='y', labelcolor=color, labelsize = 14)
#         
#         #ax2 = ax1.twinx()
#         color = 'tab:gray'
#         lns3 = ax2.plot(x_calib, set_of_lines[2], color=color, linestyle = '--', label = 'Te')  #Cd line
# =============================================================================
        
        lns4 = ax2.plot(x_calib, set_of_lines[3], color=color2, linestyle = '--', label = 'Cu', linewidth=line_size)        #Cu line
            
        # from https://stackoverflow.com/questions/5484922/secondary-axis-with-twinx-how-to-add-to-legend
        lns = lns1 + lns4
        labs = [l.get_label() for l in lns]
        leg = ax1.legend(lns, labs, loc='lower center', fontsize = tick_size)
        
        for line in leg.get_lines():
            line.set_linewidth(4)
        
        fig.tight_layout()                          # otherwise the right y-label is slightly clipped
        plt.title(sample['Name'], fontsize = axis_title_size)
        plt.xlim([lower_bound, upper_bound])
        ax1.grid()
        plt.show()
    
# =============================================================================
#         fig.get_figure()
#         fig.savefig(save_path + r"\{s}, XBIC_Cu_Cd comb.jpg".format(s = sample["Name"]))
# =============================================================================
    return #exes (PVSC)

plot_save_combined_channels(samples, master_list)

### EXTRA CODE

# quick-and-dirty export Cu and XBIC line profiles to CSVs for PVSC poster
calib_xs = plot_save_combined_channels(samples, master_list)

arrays = []
for sample, x in zip(master_list, calib_xs):
    for channel in sample:
        a = [x, channel]
        a = np.asmatrix(a)
        a = np.transpose(a)
        arrays.append(a)
count = 0      
for array in arrays:
    np.savetxt(r'C:\Users\Trumann\Dropbox (ASU)\DefectLab\PVSC 46 -2019\foo' + str(count) + '.csv', array, delimiter = ',')
    count = count +1 

# batch convert color to greyscale without DigitialMicrograph (DM) software
# =============================================================================
# #cannot tbe read by DM 
# #error: "sorry, cannot handle contiguous data with PhotometricInterpretation=1 and Samepixels=2"
# #
# #the image was about to be opened in GIMP, so it may prove ot be useful at some point
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
    


