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

#plot
fig, ax = plt.subplots()
ax.matshow(candidates_mat, cmap=plt.cm.Blues)

for i in range(candidates_mat.shape[1]):
    for j in range(candidates_mat.shape[0]):
        c = candidates_mat[j,i]
        val = f"{c:.2f}"
        ax.text(i, j, val, va='center', ha='center', fontsize=6)

candidate_names = vector_labels[0:7]
attribute_names = vector_labels[7:]

ax.set_xticks(np.arange(len(attribute_names)))
ax.set_yticks(np.arange(len(candidate_names)))
ax.set_yticklabels(candidate_names)
ax.set_xticklabels(attribute_names)
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()
plt.show()
pass