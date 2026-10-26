import numpy as np
from tap_macros import replay, rms, TapDetector

def test_double_and_triple():
    assert replay([[0,4000],[0.1,0],[0.3,4000],[0.4,0]]) == ['copy']
    assert replay([[0,4000],[0.1,0],[0.3,4000],[0.4,0],[0.6,4000]]) == ['paste']

def test_sustained_noise_and_idle_reset():
    assert replay([[0,4000],[0.1,4000],[0.2,4000]]) == []
    d = TapDetector()
    d.update(4000,0)
    d.update(0,0.1)
    d.update(4000,0.3)
    assert d.update(0,2) is None
    assert not d.taps
    assert rms(np.array([3000,-3000],dtype='<i2').tobytes()) == 3000
