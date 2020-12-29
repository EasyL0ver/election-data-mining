from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
import matplotlib.pyplot as plt


session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session, filter_empty=True)

counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))
vector_labels = data_counties[0].get_vector().labels(short=True)

m = np.corrcoef(counties_mat, rowvar=False)
candidates_mat = m[:7, 7:]
dem_mat = candidates_mat[:2, :]
rep_mat = candidates_mat[2:, :]

#plot
fig, (axdem, axrep) = plt.subplots(2,1)
axdem.matshow(dem_mat, cmap=plt.cm.Blues)
axrep.matshow(rep_mat, cmap=plt.cm.Reds)

for i in range(dem_mat.shape[1]):
    for j in range(dem_mat.shape[0]):
        c = dem_mat[j,i]
        val = f"{c:.2f}"
        axdem.text(i, j, val, va='center', ha='center', fontsize=6)

for i in range(rep_mat.shape[1]):
    for j in range(rep_mat.shape[0]):
        c = rep_mat[j,i]
        val = f"{c:.2f}"
        axrep.text(i, j, val, va='center', ha='center', fontsize=6)

democrat_candidate_names = vector_labels[:2]
republican_candidate_names = vector_labels[2:7]
attribute_names = vector_labels[7:]

axdem.set_yticks(np.arange(2))
axdem.set_yticklabels(democrat_candidate_names)
axrep.set_yticks(np.arange(5))
axrep.set_yticklabels(republican_candidate_names)

axdem.xaxis.set_ticks_position('top')
axdem.xaxis.set_tick_params(rotation=90, bottom=False, top=True)
axdem.set_xticks(np.arange(len(attribute_names)))
axdem.set_xticklabels(attribute_names, fontdict={'size': 7})

axrep.set_xticks([])
axdem.set_xticklabels(attribute_names)
plt.tight_layout(rect=[0,0,1,1])
plt.show()
pass