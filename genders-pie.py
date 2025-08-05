import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('filled_all_data.csv')

gender_counts = df['gender_new'].value_counts()
gender_counts = gender_counts.drop(labels=['неопр', None], errors='ignore')

labels_map = {
    'муж': 'Мужчины',
    'жен': 'Женщины',
    'мн': 'Несколько человек',
}
colors = {
    'муж': '#97CCE8',
    'жен': '#F4B9C1',
    'мн': '#9E9E9E',
}

labels = [labels_map.get(g, g) for g in gender_counts.index]
values = gender_counts.values
colors_used = [colors.get(g, '#CCCCCC') for g in gender_counts.index]

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    values,
    labels=None, 
    colors=colors_used,
    autopct='%1.1f%%',
    startangle=90,
    counterclock=False,
    textprops={'color': 'black', 'fontsize': 14},
    pctdistance=0.75
)

for i, wedge in enumerate(wedges):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.1 * np.cos(np.deg2rad(ang))
    y = 1.1 * np.sin(np.deg2rad(ang))
    ha = 'left' if x > 0 else 'right'
    plt.text(x, y, labels[i], ha=ha, va='center', fontsize=14)

plt.setp(autotexts, weight='normal') # не жирный

plt.axis('equal')
plt.title('Распределение по полу')
plt.tight_layout()
plt.show()
