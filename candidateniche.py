from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
import matplotlib.pyplot as plt


def calc_niche(mat, candidate_names, attribute_names, factor = 1):
    pos = dict()
    neg = dict()
    for name in candidate_names:
        pos[name] = []
        neg[name] = []

    stddev = np.std(mat)
    tresh = factor * stddev

    for i in range(mat.shape[1]):
        for j in range(mat.shape[0]):
            val = mat[j,i]
            attribute = attribute_names[i]
            candidate = candidate_names[j]
            if val >= tresh:
                pos[candidate].append(attribute)
            elif val <= (-tresh):
                neg[candidate].append(attribute)


    return pos, neg


session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session, filter_empty=True)

counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))
vector_labels = data_counties[0].get_vector().labels(short=True)

m = np.corrcoef(counties_mat, rowvar=False)

candidates_mat = m[:7, 7:]
dem_mat = candidates_mat[:2, :]
rep_mat = candidates_mat[2:, :]

democrat_candidate_names = vector_labels[:2]
republican_candidate_names = vector_labels[2:7]
attribute_names = vector_labels[7:]

rep_pos, rep_neg = calc_niche(rep_mat, republican_candidate_names, attribute_names, factor=1.4)
dem_pos, dem_neg = calc_niche(dem_mat, democrat_candidate_names, attribute_names, factor=1.4)

pos = {**rep_pos, **dem_pos}
neg = {**rep_neg, **dem_neg}


candidate_names = vector_labels[:7]
fig, axes = plt.subplots(4,2)
fig.patch.set_visible(False)
fig.suptitle("Attribute correlation to candidate votes")
for i in range(axes.shape[0]):
    for k in range(axes.shape[1]):
        ax = axes[i,k]
        ax.axis('off')
        ax.axis('tight')

        cand_index = i + k * 4
        if (cand_index) > 6:
            break
        name = candidate_names[cand_index]
        positive_attributes = pos[name]
        negative_attributes = neg[name]
        table_size = max(len(positive_attributes), len(negative_attributes))
        positive_attributes += [None] * (table_size - len(positive_attributes))
        negative_attributes += [None] * (table_size - len(negative_attributes))
        table = [positive_attributes , negative_attributes]
        table = np.array(table).T
        ax.set_title(name)
        pos_colors = ['#9af274'] * len(positive_attributes)
        neg_colots = ['#f28974'] * len(positive_attributes)
        cell_colors = np.array([pos_colors, neg_colots]).T
        t = ax.table(cellText = table, colLabels=['Positive', 'Negative'], loc='center', cellLoc='center', fontsize=30, colColours=['green', 'red'], cellColours=cell_colors)
        t.auto_set_font_size(False)
        t.set_fontsize(7)
        t.scale(1.1, 0.5)

plt.show()
pass





