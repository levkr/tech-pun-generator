from scipy.io import wavfile
import numpy as np
import random

max_16 = 2 ** 16 - 1

def noise_wav(wav_file_path):
	sample_rate, data = wavfile.read(wav_file_path)
	data_list = data.tolist()
	new_data_list = []
	max = 0
	min = max_16
	for i in range(len(data_list)):
		#rand1
		rand1 = random.randint(1200, 1800)
		#new_data_list.append([(data_list[i][0] + rand1) % max_16, (data_list[i][1] + rand1) % max_16])
		
		#rand2
		rand2 = random.random() + 0.8
		#new_data_list.append([int(data_list[i][0] * rand2) % max_16, int(data_list[i][1] * rand2) % max_16])

		#rand3
		new_data_list.append([int(data_list[i][0] * rand2 + rand1) % max_16, int(data_list[i][1] * rand2 + rand1) % max_16])
		
		
	new_data = np.array(new_data_list)
	new_data = np.asarray(new_data, dtype=np.int16)
	wavfile.write(wav_file_path, sample_rate, new_data)

def guassian_noise(wav_file_path):
	sample_rate, data = wavfile.read(wav_file_path)
	data_list = data.tolist()
	new_data_list = []
	noise = np.random.normal(1200, 200, len(data_list))
	for i in range(len(data_list)):
		new_data_list.append([(data_list[i][0] + noise[i]) % max_16, (data_list[i][1] + noise[i]) % max_16])

	new_data = np.array(new_data_list)
	new_data = np.asarray(new_data, dtype=np.int16)
	wavfile.write(wav_file_path, sample_rate, new_data)	