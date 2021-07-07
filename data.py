import numpy as np


level = {"raw":0, "fft":1, "coh":2, "filt":3}
data = np.zeros((4, 320,10000), dtype=np.float32)
mask = np.ones(data[0].shape, dtype=bool)

hits_list = []
evt_hits_list = []
evt_trk2D_list = []
evt_trk3D_list = []
