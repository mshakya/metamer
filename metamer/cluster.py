import pandas as pd
import sklearn.cluster
import scipy

# from scipy.spatial.distance import squareform, pdist


# def conv_matrix(md):
# 	"""Converts the table that that has ref-query-dist-pvalue,shared to distance
# 	matrix """
# 	mdf = pd.read_csv(md, sep="\t", names=["m1", "m2", "dist", "pvalue", "shared"])
# 	mdf = mdf[mdf['dist'] < 1]
# 	mdf["m1"] = mdf["m1"].apply(lambda x: x.split("/")[-1])
# 	mdf["m2"] = mdf["m2"].apply(lambda x: x.split("/")[-1])
# 	dmc = mdf[['m1', 'm2', 'dist']]
# 	print(dmc)
# 	dm = dmc.pivot(index='m1', columns='m2', values='dist')
# 	dm = dm.values
# 	return dm

# mat = conv_matrix("tests/data/dists/test_table.txt")

# sklearn.cluster.AgglomerativeClustering(n_clusters=None, affinity="pre-computed", connectivity=None, compute_full_tree=True, linkage="average",
# 										distance_threshold=None)

# This is the one that works

def convert2matrix(dist_file):
    """A function that converts mash distance file to hierarchical clustering."""
    # read in the output file from mash
    mdf = pd.read_csv(dist_file, sep="\t", names=["m1", "m2", "dist",
                                                  "pvalue", "shared"])
    mdf["m1"] = mdf["m1"].apply(lambda x: x.split("/")[-1])
    mdf["m2"] = mdf["m2"].apply(lambda x: x.split("/")[-1])
    mdf = mdf.sort_values(by=["m1"])  # sort based on first column
    # pivot the df and then replace NA wit
    udf = mdf.pivot(index="m1", columns="m2", values="dist").fillna(0)
    # insert the missing column
    udf.insert(loc=0, column=udf.index[0], value=[0.0]*udf.shape[0],
               allow_duplicates=True)
    # insert the missing row
    udf.loc[udf.columns[-1]] = [0.0]*udf.shape[1]
    return udf.values


def cluster(mat, dist):
    """Given a matrix and distance perform hierarchical clustering."""

    up_mat = np.triu(mat)  # convert the matrix to upper triangle matrix
    # Z = scipy.cluster.hierarchy.linkage(up_mat, method=dist)
    if dist == "single":
        Z = scipy.cluster.hierarchy.single(up_mat)
    elif dist = "complete":
        Z = scipy.cluster.hierarchy.complete(up_mat)
    elif dist = "average":
        Z = scipy.cluster.hierarchy.average(up_mat)
    elif dist = "weighted":
        Z = scipy.cluster.hierarchy.weighted(up_mat)
    return Z


def plot_hclust(linkage):
    """Given linkage from scipy.hierarchy.single,etc. 
        produces a tree diagram of the clustering."""

    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    scipy.cluster.hierarchy.dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()


class ClusterSamples(Task):
    """luigi class for clustering mash distance."""
    dist_file = Parameter()
    dist_algo = Parameter()

    def requires(self):
        LocalTarget(self.dist_file)

    def cluster_dist(self):
        """calculate distance sketch"""


    def run(self):
        """luigi run"""
        dist_mat = convert2matrix(self.dist_file)
        linkage = cluster(dist_mat, self.dist_algo)

    def output(self):
        """output"""
        # return faqcs.RefFile(self.out_file)
        return LocalTarget(self.out_file)
