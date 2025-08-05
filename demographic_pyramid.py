import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

df = pd.read_csv('filled_all_data.csv')

# извлекаем числа, приводим к числу
df['age'] = df['age'].astype(str).str.extract(r'(\d+)')
df['age'] = pd.to_numeric(df['age'], errors='coerce').astype('Int64')  # сохраняем тип с NaN

df = df[df['age'].notna()]

df = df[df['gender_new'].isin(['муж', 'жен'])]
df['status'] = df['status'].fillna('nan')

def simplify_status(s):
    if s == 'жив(а)':
        return 'жив'
    elif s == 'пропал(а)' or s == 'nan':
        return 'пропал/nan'
    elif s == 'погиб(ла)':
        return 'мертв'
    else:
        return 'пропал/nan'  # на всякий случай

df['status_simple'] = df['status'].apply(simplify_status)

# Группировка и подсчет

grouped = df.groupby(['age', 'gender_new', 'status_simple']).size().reset_index(name='count')

pivot = grouped.pivot_table(index='age', columns=['gender_new', 'status_simple'], values='count', fill_value=0)

ages = sorted(pivot.index)

colors_male = {
    'жив': mcolors.to_rgba('#5EB8E7', alpha=1),
    'пропал/nan': mcolors.to_rgba('#5EB8E7', alpha=0.6),
    'мертв': mcolors.to_rgba('#5EB8E7', alpha=0.3)
}
colors_female = {
    'жив': mcolors.to_rgba('#FAA4B0', alpha=1),
    'пропал/nan': mcolors.to_rgba('#FAA4B0', alpha=0.6),
    'мертв': mcolors.to_rgba('#FAA4B0', alpha=0.3)
}

fig, ax = plt.subplots(figsize=(12, 18))

widths_male = np.zeros(len(ages))
widths_female = np.zeros(len(ages))

female_labels = []
female_handles = []
male_labels = []
male_handles = []

for status in ['жив', 'пропал/nan', 'мертв']:
    male_vals = pivot.get(('муж', status), pd.Series([0]*len(ages), index=ages))
    female_vals = pivot.get(('жен', status), pd.Series([0]*len(ages), index=ages))

    h_m = ax.barh(ages, male_vals, left=widths_male, color=colors_male[status], label=f'{status}', align='center')
    widths_male += male_vals.values

    h_f = ax.barh(ages, -female_vals, left=-widths_female, color=colors_female[status], label=f'{status}', align='center')
    widths_female += female_vals.values

    def get_label(gender, status):
        if status == 'жив':
            return 'жив' if gender == 'муж' else 'жива'
        elif status == 'пропал/nan':
            return 'пропал' if gender == 'муж' else 'пропала'
        elif status == 'мертв':
            return 'мертв' if gender == 'муж' else 'мертва'
        else:
            return status

    male_handles.append(h_m[0])
    male_labels.append(get_label('муж', status))

    female_handles.append(h_f[0])
    female_labels.append(get_label('жен', status))

for age in ages:
    ax.axhline(y=age, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)

ax.set_yticks(ages)
ax.set_yticklabels([str(age) for age in ages])  # без -1, поэтому просто строка

ax.set_xlabel('Количество пропавших')
ax.set_ylabel('Возраст')
ax.set_title('Распределение по возрастам, статусу и полу')

max_count = max(widths_male.max(), widths_female.max())
step = 25

xticks_pos = list(range(0, int(max_count) + step, step))
xticks_full = [-x for x in xticks_pos[::-1]] + xticks_pos

ax.set_xticks(xticks_full)
ax.set_xticklabels([str(abs(x)) for x in xticks_full])

ax.axvline(0, color='black', linewidth=0.8)

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper right')

ax.grid(axis='x', linestyle='--', alpha=0.7)

leg_female = ax.legend(female_handles, female_labels, loc='upper left', title='Женщины')
leg_male = ax.legend(male_handles, male_labels, loc='upper right', title='Мужчины')
ax.add_artist(leg_female)

plt.tight_layout()
plt.show()