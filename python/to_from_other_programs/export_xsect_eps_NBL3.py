"""
coding: utf-8

tzwalker
Mon May 18 09:32:08 2020
"""

# trying to plot XBIC and Cu cross sections
# with same dimensions as the Origin figure of
# integrate ddepth profiles

# note run 'main-NBLxsect home.py' before running this code
# [dfs[0].columns[:-45]] is to chop off columns of the map
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\vector graphics and figures'
FNAME = r'\NBL31scan8_full.eps'
PATH_OUT = PATH +FNAME 

fig, axs = plt.subplots(2,1, figsize=(cm2inch(3.5,3.5)))
plt.tight_layout(pad=-10)
XBIC = dfs[0]#[dfs[0].columns[:-45]]
axs[0].imshow(XBIC, cmap='inferno',extent=(0,300,0,100))
axs[0].axis('off')
Cu = dfs[1]#[dfs[1].columns[:-45]]
axs[1].imshow(Cu, cmap='Greys_r', extent=(0,300,0,100), vmax=3000)
axs[1].axis('off')
plt.savefig(PATH_OUT, format='eps', bbox_inches='tight')