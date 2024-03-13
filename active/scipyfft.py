#from matplotlib import pyplot as plt
import numpy as np


#setting time intervals (will be time in between samples)
time_step = 0.05
#create numpy array from 0 to 10 with steps of 0.05
time_vec = np.arange(0, 10, time_step)
period = 5

#now creating a signal (sin wave), dividing by period creates more points for the cycle (100 points for 1 cycle now)
sig = (np.sin(2*np.pi*time_vec/period)) + 0.25*np.random.randn(time_vec.size)
#every 20 points, we complete one cycle (0.05 * 20 = 1)


#need code from here out
sig_fft = fftpack.fft(sig)

Amplitude = np.abs(sig_fft)
Power = Amplitude**2

#contains frequencies
sample_freq = fftpack.fftfreq(sig.size, d=time_step)

#find position of max amplitude
Amp_Freq = np.array([Amplitude, sample_freq])

#finding index of max value in amplitude array
Amp_Position = Amp_Freq[0,:].argmax()

peak_freq = Amp_Freq[1, Amp_Position]
print(peak_freq)