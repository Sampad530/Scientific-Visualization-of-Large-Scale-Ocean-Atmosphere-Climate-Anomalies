
#######################################################

#Data Extraction for hovmoller plots

######################################################
import json
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import openvisuspy as ov
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from tqdm import tqdm  # ✅ Import tqdm


############################

variable='theta' # options are: u,v,w,salt,theta

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

###############################################

db=ov.LoadDataset(field)
print(f'Dimensions: {db.getLogicBox()[1][0]}*{db.getLogicBox()[1][1]}*{db.getLogicBox()[1][2]}')
print(f'Total Timesteps: {len(db.getTimesteps())}')
print(f'Field: {db.getField().name}')
print('Data Type: float32')

########################################
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tqdm import tqdm

# Initialize
rows = []
valid_times = []

tt = 10366
start_t = 0

# Loop and filter
for t in tqdm(range(start_t, tt)):

    data = db.db.read(time=t, quality=0, z=[27, 28], x=[3793, 7632], y=[3830, 4090]) # extract data for nino3.4 region

    avg_row = data.mean(axis=1).reshape(1, data.shape[2])
    rows.append(avg_row)
    valid_times.append(t)

# Concatenate valid rows
avg_image = np.concatenate(rows, axis=0)  # shape: (n_valid_times, 3839)

# Save the data
np.save("avg_sst.npy", avg_image)
np.save("times.npy", np.array(valid_times))