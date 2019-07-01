import pandas as pd
import scipy.cluster
import numpy as np
from luigi import IntParameter, Parameter, ListParameter, LocalTarget, Task
import os
from collections import defaultdict
import csv
import itertools
import functools


def cluster(mat, dist):
    """Given a matrix and distance perform hierarchical clustering."""

    up_mat = np.triu(mat)  # convert the matrix to upper triangle matrix
    # Z = scipy.cluster.hierarchy.linkage(up_mat, method=dist)
    if dist == "single":
        Z = scipy.cluster.hierarchy.single(up_mat)
    elif dist == "complete":
        Z = scipy.cluster.hierarchy.complete(up_mat)
    elif dist == "average":
        Z = scipy.cluster.hierarchy.average(up_mat)
    elif dist == "weighted":
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
    out_dir = Parameter()
    # dist_algo = Parameter()

    def requires(self):
        dfile = os.path.join(self.out_dir, "mash_dist.txt")
        LocalTarget(dfile)

    def get_linkage(self):
        """A function that clusters."""
        # An empty data structure.
        name_to_id = defaultdict(functools.partial(next, itertools.count()))

        # open the file
        mash_dist_file = os.path.join(self.out_dir, "mash_dist.txt")
        with open(mash_dist_file) as f:
            reader = csv.reader(f, delimiter="\t")

    # do one pass over the file to get all the IDs so we know how 
    # large to make the matrix, then another to fill in the data.
    # this takes more time but uses less memory than loading everything
    # in in one pass, because we don't know how large the matrix is; you
    # can skip this if you do know the number of elements from elsewhere.
            for name_a, name_b, dist, p, share in reader:
                idx_a = name_to_id[name_a]
                idx_b = name_to_id[name_b]

    # make the (square) distances matrix
    # this should really be triangular, but the formula for 
    # indexing into that is escaping me at the moment
                n_elem = len(name_to_id)
                dists = np.zeros((n_elem, n_elem))

        # go back to the start of the file and read in the actual data
            f.seek(0)
            for name_a, name_b, dist, p, share in reader:
                idx_a = name_to_id[name_a]
                idx_b = name_to_id[name_b]
                dists[(idx_a, idx_b) if idx_a < idx_b else (idx_b, idx_a)] = dist

        np.savetxt(os.path.join(self.out_dir, "dist.txt"),
                   dists, delimiter=",")

        up_mat = np.triu(dists)
        linkage = scipy.cluster.hierarchy.single(up_mat)
        id_to_name = dict((id, name) for name, id in name_to_id.items())
        return linkage, id_to_name

    def parse_clusters(self, linkage, id_to_name):
        flat_clus = scipy.cluster.hierarchy.fcluster(linkage, 0.9)
        cluster_file = os.path.join(self.out_dir, "clusters.txt")
        md = defaultdict(list)
        for cl, a in enumerate(flat_clus):
            md[a].append(id_to_name[cl].split("/")[-1])
        print(md)
        with open(cluster_file, 'w') as cl_file:
            writer = csv.writer(cl_file)    
            for cl, mem in md.items():
                writer.writerow([cl, mem])

    def plot_linkage(self, linkage):
        plt.figure(figsize=(25, 10))
        plt.title('Hierarchical Clustering Dendrogram')
        plt.xlabel('sample index')
        plt.ylabel('distance')
        scipy.cluster.hierarchy.dendrogram(linkage,
                                           leaf_rotation=90.,  # rotates the x axis labels
                                           leaf_font_size=8.)  # font size for the x axis labels
        plt_file = os.path.join(self.out_dir, "cluster.png")
        plt.save()

    def run(self):
        """luigi run"""
        linkage, id_to_name = self.get_linkage()
        self.parse_clusters(linkage, id_to_name)
        # plot_linkage(linkage)

    def output(self):
        """output"""
        mash_dist_file = os.path.join(self.out_dir, "clusters.txt")
        return LocalTarget(mash_dist_file)
