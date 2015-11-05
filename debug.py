import os
import sys

sys.path.append(os.getcwd())

import recommendation

print recommendation.rmse('result')
