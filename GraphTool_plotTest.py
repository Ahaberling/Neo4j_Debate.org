import graph_tool.all as gt
import numpy as np
import math
import matplotlib.pyplot as plt

def sample_k(max):
     accept = False
     while not accept:
         k = np.random.randint(1,max+1)
         accept = np.random.random() < 1.0/k
     return k

g = gt.random_graph(10000, lambda: sample_k(40),
                     model="probabilistic-configuration",
                     edge_probs=lambda i, j: (math.sin(i / math.pi) * math.sin(j / math.pi) + 1) / 2,
                     directed=False, n_iter=100)

vprop_ab = g.new_vertex_property("int16_t")
g.vp.ab = vprop_ab

for i in g.vertices():
    if np.random.rand() <= 0.5:
        g.vp.ab[i] = "0"
    else:
        g.vp.ab[i] = "1"

#print(np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand())

print("graph generation - success")

h = gt.corr_hist(g, "out", "out")
plt.clf()
plt.xlabel("Source out-degree")
plt.ylabel("Target out-degree")
plt.imshow(h[0].T, interpolation="nearest", origin="lower")
plt.colorbar()
plt.savefig("corr_out.svg")


h = gt.corr_hist(g, g.vp.ab, g.vp.ab)
plt.clf()
plt.xlabel("Source out-degree")
plt.ylabel("Target out-degree")
plt.imshow(h[0].T, interpolation="nearest", origin="lower")
plt.colorbar()
plt.savefig("corr_ab.svg")