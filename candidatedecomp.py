from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
plt.close()

session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session, filter_empty=True)

counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))
vector_labels = data_counties[0].get_vector().labels(short=True)

m = np.corrcoef(counties_mat, rowvar=False)

candidates_mat = m[:7, 7:]
rep_mat = candidates_mat[2:, :]
republican_candidate_names = vector_labels[2:7]
attribute_names = vector_labels[7:]

pca = PCA(n_components=2)
decomposed = pca.fit_transform(rep_mat)
explained_percentage = np.cumsum(pca.explained_variance_ratio_)

attribute_d = dict()
for i, attribute_name in enumerate(attribute_names):
    test_vector = [0] * len(attribute_names)
    test_vector[i] = 1
    test_vector = np.array(test_vector)
    test_mat = test_vector.reshape(1, -1)
    attribute_d[attribute_name] = pca.transform(test_mat)

dict_items = list(attribute_d.items())
x_axis = list(sorted(dict_items, key=lambda x:x[1][0, 0], reverse=True))
y_axis = list(sorted(dict_items, key=lambda x:x[1][0, 1], reverse=True))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3,3)
axmap = fig.add_subplot(gs[1, 1])


axnegx = fig.add_subplot(gs[1, 0])
xneglabels = np.array(list(map(lambda x: x[0], x_axis[-5:]))).reshape(5, 1)
t = axnegx.table(cellText = xneglabels, loc='center', cellLoc='center', fontsize=30)
axnegx.axis('off')
t.auto_set_font_size(False)
t.set_fontsize(8)
#t.scale(1.5,2)

axposx = fig.add_subplot(gs[1, 2])
xposlabels = np.array(list(map(lambda x: x[0], x_axis[:5]))).reshape(5, 1)
t = axposx.table(cellText = xposlabels, loc='center', cellLoc='center', fontsize=8)
axposx.axis('off')
t.auto_set_font_size(False)
t.set_fontsize(8)
#t.scale(1.5,2)


axposy = fig.add_subplot(gs[0, 1])
yposlabels = np.array(list(map(lambda x: x[0], y_axis[:5]))).reshape(5, 1)
t = axposy.table(cellText = yposlabels, loc='center', cellLoc='center', fontsize=8)
axposy.axis('off')
t.auto_set_font_size(False)
t.set_fontsize(8)
#t.scale(2,2)

axnegy = fig.add_subplot(gs[2, 1])
yneglabels = np.array(list(map(lambda x: x[0], y_axis[-5:]))).reshape(5, 1)
t = axnegy.table(cellText = yneglabels, loc='center', cellLoc='center', fontsize=8)
axnegy.axis('off')
t.auto_set_font_size(False)
t.set_fontsize(8)
#t.scale(2,2)



# fig, (axmap, axbar) = plt.subplots(2,1)
x = [value[0] for value in decomposed]
y = [value[1] for value in decomposed]
axmap.scatter(x, y)
axmap.set_xlim(-0.7, 1.5)
axmap.set_ylim(-0.5, 0.8)
axmap.grid()
#axbar.bar(attribute_names, pca.mean_)
for i, name in enumerate(republican_candidate_names):
    axmap.annotate(name, (x[i], y[i]))

#plt.tight_layout()
plt.show()
pass

