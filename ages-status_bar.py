import pandas as pd
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Patch  # для ручной легенды

df = pd.read_csv('filled_all_data.csv')

def parse_age(age_str):
    '''для преобразования строки с возрастами в список чисел'''
    if pd.isna(age_str):
        return []
    try:
        ages = ast.literal_eval(age_str)
        if isinstance(ages, int):
            return [ages]
        elif isinstance(ages, list):
            return ages
        else:
            return []
    except:
        return []

df['age_list'] = df['age'].apply(parse_age)

# каждая строка с одним возрастом
df_expanded = df.explode('age_list')
df_expanded = df_expanded[df_expanded['age_list'].notna()]
df_expanded['age_list'] = df_expanded['age_list'].astype(int)

# количество по возрастам и статусам
counts = df_expanded.groupby(['age_list', 'status']).size().unstack(fill_value=0)

# проверяем что все нужные статусы есть
for col in ['пропал(а)', 'жив(а)', 'погиб(ла)']:
    if col not in counts.columns:
        counts[col] = 0

# Сортировка по возрасту
counts = counts.sort_index()

ages = counts.index.tolist()
dead = counts['погиб(ла)'].tolist()
missing = counts['пропал(а)'].tolist()
alive = counts['жив(а)'].tolist()

plt.figure(figsize=(18, 6))

plt.bar(ages, dead, label='Погиб(ла)', color='#EA3C2D')
plt.bar(ages, missing, bottom=dead, label='Пропал(а)', color='#F6C944')
plt.bar(ages, alive, bottom=[d + m for d, m in zip(dead, missing)], label='Жив(а)', color='#85BA38')

plt.xlabel('Возраст')
plt.ylabel('Количество пропавших')
plt.title('Распределение по возрастам и статусам')
plt.grid(True, axis='y', linestyle='--', alpha=0.4)

custom_legend = [
    Patch(color='#85BA38', label='Жив(а)'),
    Patch(color='#F6C944', label='Пропал(а)'),
    Patch(color='#EA3C2D', label='Погиб(ла)'),
]
plt.legend(handles=custom_legend, loc='upper right')

plt.xticks(ages, [str(age) for age in ages], rotation=80)

plt.tight_layout()
plt.show()
