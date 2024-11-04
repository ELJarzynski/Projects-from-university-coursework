from Lab04.Zadania.Ad1 import *
import numpy as np
import math
# cars['make-encoder'].hist(bins=10)
# np.sqrt(cars['make-encoder']).hist(bins=10)
# np.log(cars['make-encoder']).hist(bins=10)
plt.show()

# Length
np.sqrt(cars['length']).hist(bins=10)
# Width
np.log(cars['width']).hist(bins=10)
# Height
np.log(cars['height']).hist(bins=10)
# Curb weight
np.log(cars['curb-weight']).hist(bins=10)
# Engine size
np.log(cars['engine-size']).hist(bins=10)
# Compression ratio
np.log(cars[' compression-ratio']).hist(bins=10)
# City mpg
np.log(cars['city-mpg']).hist(bins=10)
# Highway mpg
np.log(cars['highway-mpg']).hist(bins=10)
