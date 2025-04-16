
#####################################################################################
# This script extracts sea surface temperature data from a dataset for ENSO analysis.
#####################################################################################
# Import necessary libraries
import numpy as np
import openvisuspy as ov
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from tqdm import tqdm
#####################################################################################
#variable selection
# options are: u,v,w,salt,theta

variable='theta'

#####################################################################################
# DONOT TOUCH
base_url= "https://maritime.sealstorage.io/api/v0/s3/utah/nasa/dyamond/"
end_url="?access_key=any&secret_key=any&endpoint_url=https://maritime.sealstorage.io/api/v0/s3&cached=arco"
if variable=="theta" or variable=="w":
    base_dir=f"mit_output/llc2160_{variable}/llc2160_{variable}.idx"
elif variable=="u":
    base_dir= "mit_output/llc2160_arco/visus.idx"
else:
    base_dir=f"mit_output/llc2160_{variable}/{variable}_llc2160_x_y_depth.idx"
    
field= base_url+base_dir+end_url

#####################################################################################
# Load the dataset
db=ov.LoadDataset(field) 
print(f'Dimensions: {db.getLogicBox()[1][0]}*{db.getLogicBox()[1][1]}*{db.getLogicBox()[1][2]}') # Dimensions: 8640*6480*90
print(f'Total Timesteps: {len(db.getTimesteps())}')  # Total Timesteps: 10366
print(f'Field: {db.getField().name}') # Field: theta
print('Data Type: float32') # Data Type: float32

#####################################################################################

# We select indexs of x and y range with corresponding coordinates of nino regions here
# time steps are also fixed here
# for SST we kept z=[0, 1] to get the sea surface temperature

for t in tqdm(range(0, 10366), desc="Computing"):
    data1 = db.db.read(time=10365, z=[0, 1], x=[0, 8640], y=[0, 6480], quality=0)

    plt.figure(figsize=(10, 6))

    # vmin and vmax are set to highlight the sea surface temperature range
    img = plt.imshow(data1[0, :, :], origin='lower', vmin=-10, vmax=36, cmap='turbo', aspect='auto')

    # Add title
    plt.title('Global Sea Surface Temperature', fontsize=14, pad=20)

    # Hide axis
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    # Add vertical colorbar
    cbar = plt.colorbar(img, orientation='vertical', pad=0.05)
    cbar.set_label('SST (°C)')

    # Save the figure
    plt.savefig('01_image.png', bbox_inches='tight', dpi=300)
