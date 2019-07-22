# scan indices:
    # 0-2 --> 2019_03
    # 3 --> 2017_12
# element indices:
    # 0 --> Cu
    # 1 --> Cd
    # will add others if needed

#import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.cluster import KMeans

  
cu_map = NBL3_3['XBIC_ele_maps'][0][0]

ax = sns.heatmap(cu_map, square = True)
ax.invert_yaxis()
