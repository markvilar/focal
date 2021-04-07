import csv

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Set up matplotlib style.
plt.style.use(['Scientific', 'high-vis'])

def position_feature_plotting(path: str):
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		data = {}
		for row in reader:
			for key, value in row.items():
				if not key in data:
					data[key] = []
				
				if key == 'index':
					data[key].append(int(value))
				else:
					data[key].append(float(value))

	for key, value in data.items():
		data[key] = np.array(value)
	
	y_limits = [0.0, 0.4]
	fig1, ax1 = plt.subplots()
	ax1.axline((0, 0.21), (2.5, 0.21), label='Measurement',
		color='#e6091c')
	ax1.scatter(data['z'], data['feature'], label='Reconstruction')
	ax1.set_xlabel(r'Depth, $\prescript{c}{}{z}$ [m]')
	ax1.set_ylabel('Geometric Feature [m]')
	ax1.set_ylim(y_limits)
	ax1.legend(loc='lower right')
	fig1.savefig('./figures/feature-depth.png', dpi=300)

	fig2, ax2 = plt.subplots(figsize=(3, 3))
	ax2.axline((-30, 0.21), (30, 0.21), label='Measurement',
		color='#e6091c')
	ax2.scatter(data['angle_x'] * 180 / np.pi, data['feature'],
		label='Reconstruction')
	ax2.set_xlabel(r'View direction angle, $\alpha_{x}$ [deg]')
	ax2.set_ylabel('Geometric Feature [m]')
	ax2.set_ylim(y_limits)
	ax2.legend(loc='lower right')
	fig2.savefig('./figures/feature-angle-x.png', dpi=300)

	fig3, ax3 = plt.subplots(figsize=(3, 3))
	ax3.axline((-30, 0.21), (30, 0.21), label='Measurement',
		color='#e6091c')
	ax3.scatter(data['angle_y'] * 180 / np.pi, data['feature'],
		label='Reconstruction')
	ax3.set_xlabel(r'View direction angle, $\alpha_{y}$ [deg]')
	ax3.set_ylabel('Geometric Feature [m]')
	ax3.set_ylim(y_limits)
	ax3.legend(loc='lower right')
	fig3.savefig('./figures/feature-angle-y.png', dpi=300)

	plt.show()

def feature_plotting(path: str):
	raise NotImplementedError

def main():
	path = './data/reconstruction/position-feature.csv'
	position_feature_plotting(path)

if __name__ == '__main__':
	main()
