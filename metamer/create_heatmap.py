import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# sphinx_gallery_thumbnail_number = 2




def create_heatmap(dist, x, y, title, out_file):
	"""read in the dataframe and create heatmap."""

	print(dist)

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


def create_sns_heatmap(dist_file):
	mash_df = pd.read_csv(dist_file, sep="\t", header=None)
	print(mash_df)
	upper_dist_df = mash_df.pivot(0, 1, 2).fillna(0)
	print(upper_dist_df)
	lower_dist_df = mash_df.pivot(0, 1, 2).transpose().fillna(0)
	dist_df = upper_dist_df + lower_dist_df
	cl_map = sns.clustermap(dist_df)
	return cl_map