import matplotlib.pyplot as plt
import numpy as np
import os

# === ЧТЕНИЕ ДАННЫХ ===
file_path = os.path.join(os.path.dirname(__file__), '1.csv')
numbers = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            try:
                number = float(line.replace(',', '.'))
                numbers.append(number)
            except ValueError:
                continue

if not numbers:
    raise ValueError("Файл 1.csv пуст или не содержит чисел!")

numbers.sort()
n = len(numbers)

# === ИНТЕРВАЛЬНЫЙ РЯД ===
counts = [11, 14, 8, 9, 5, 1, 2]
indexes = [1, 12, 26, 34, 43, 48, 49]
bin_edges = [numbers[i-1] for i in indexes]
relative_freq = [freq / n for freq in counts]

# === КУМУЛЯТИВНЫЕ ЗНАЧЕНИЯ ===
cumulative = np.cumsum([0] + relative_freq)  # [0, p1, p1+p2, ..., 1]
print(cumulative)

# === ОДИН ГРАФИК: ИДЕАЛЬНАЯ ЛЕСЕНКА ЭФР ===
plt.figure(figsize=(15, 8), dpi=150, facecolor='white')
ax = plt.gca()

# --- 1. СТРОИМ ЛЕСЕНКУ: ГОРИЗОНТАЛЬНЫЕ + ВЕРТИКАЛЬНЫЕ СЕГМЕНТЫ ---
x_points = [0.0] + bin_edges
y_points = [0.0] + list(cumulative[1:])  # F(x) после каждого скачка

# Рисуем сегменты: от (x_i, y_i) → (x_{i+1}, y_i) → (x_{i+1}, y_{i+1})
for i in range(len(x_points) - 1):
    x_left, x_right = x_points[i], x_points[i+1]
    y_level = y_points[i]  # F(x) на участке [x_left, x_right)

    # Горизонтальный сегмент
    ax.plot([x_left, x_right], [y_level, y_level],
            color='#2ca02c', linewidth=7, solid_capstyle='butt', zorder=4)

    # Вертикальный скачок в правой границе (кроме последнего)
    if i < len(x_points) - 2:
        y_next = y_points[i+1]
        ax.plot([x_right, x_right], [y_level, y_next],
                color='#aeaeae', linewidth=7, zorder=4)

# --- 2. ПОСЛЕДНЯЯ ГОРИЗОНТАЛЬ ДО +∞ ---
last_x = bin_edges[-1]
ax.plot([last_x, last_x + (last_x - 0.0) * 0.3], [1.0, 1.0],
        color='#2ca02c', linewidth=7, zorder=4)

# Выколотые точки в правых границах (на вершине скачка)
for i in range(len(relative_freq)):
    x_val = bin_edges[i]
    y_val = cumulative[i+1]  # F(x) после скачка
    ax.plot(x_val, y_val, 'o',
            markerfacecolor='white', markeredgecolor='#2ca02c',
            markeredgewidth=3, markersize=14, zorder=5)

# --- ОСИ ---
x_max = last_x + (last_x - 0.0) * 0.3
ax.set_xlim(0 * x_max, x_max)
ax.set_ylim(0, 1.10)

yticks = np.linspace(0, 1, 6)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{y:.2f}" for y in yticks], fontsize=13)

xticks = [0.0] + bin_edges
ax.set_xticks(xticks)
ax.set_xticklabels([f"{x:.2f}" for x in xticks], rotation=45, ha='right', fontsize=11)

plt.xlabel('Значения (x)', fontsize=14, labelpad=15)
plt.ylabel('F(x)', fontsize=14, labelpad=15)

ax.grid(True, axis='y', alpha=0.35, linestyle='--', linewidth=1, zorder=1)
ax.set_axisbelow(True)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_linewidth(1.8)
ax.tick_params(width=1.8, length=7)

plt.tight_layout()
plt.show()