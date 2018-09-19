import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_number = 2




def create_heatmap(dist, x, y, title, out_file):
	"""read in the dataframe and create heatmap."""
	fig, ax = plt.subplots()
	im = ax.imshow(dist)

	# We want to show all ticks...
	ax.set_xticks(np.arange(len(x)))
	ax.set_yticks(np.arange(len(y)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(x)
	ax.set_yticklabels(y)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
		 rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	for i in range(len(x)):
		for j in range(len(y)):
			text = ax.text(j, i, dist[i, j],
					   ha="center", va="center", color="w")

	ax.set_title(title)
	fig.tight_layout()
	# plt.show()
	plt.savefig(out_file)


