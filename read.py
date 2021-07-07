import data as data
import tables as tab
import numpy as np

def read_data():
    with tab.open_file("data/1294_1_a_talk_test_for_talk.h5", "r") as f:
        d = f.root.rawdata.read()[0][0]
        p = f.root.pedestal.read()[0][0]
        data.data[data.level['raw']] = d - p[:,None]
