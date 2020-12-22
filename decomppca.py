from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plot

session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session, filter_empty=True)
counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))


data_states = load_states(session)
states_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_states)))

# print(data_states)

pca = PCA(n_components=2)
decomposed = pca.fit_transform(states_mat)

# y_pos = np.arange(len(pca.explained_variance_ratio_))
# #plot.bar([str(i) for i in range(40)], pca.explained_variance_ratio_, width=0.5)
# plot.scatter([i for i in range(39)], pca.explained_variance_ratio_)
# print(pca.explained_variance_ratio_)
# plot.savefig('decomposition_bar_plot.png')

data_counties = load_counties(session, filter_empty=True)
vector_labels = data_counties[0].get_vector().labels(short=True)
attribute_names = vector_labels[7:]
print(attribute_names)

x = [value[0] for value in decomposed]
y = [value[1] for value in decomposed]
plot.scatter(x, y)
for i, state in enumerate(data_states):
    plot.annotate(state, (x[i], y[i]))
#plot.savefig('decomposition_n_2.png')
plot.show()

