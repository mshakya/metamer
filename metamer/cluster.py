import pandas as pd
from sklearn.cluster 

# from scipy.spatial.distance import squareform, pdist


def conv_matrix(md):
	"""Converts the table that that has ref-query-dist-pvalue,shared to distance
	matrix """
	mdf = pd.read_csv(md, sep="\t", names=["m1", "m2", "dist", "pvalue", "shared"])
	dmc = mdf[['m1','m2', 'dist']]
	dm = dmc.pivot(index='m1', columns='m2', values='dist')
	dm = dm.values
	# dm = pd.DataFrame( dmc.iloc['dist'], )
	return dm
