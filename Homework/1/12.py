import matplotlib.pyplot as plt
import os
file_path = os.path.join(os.path.dirname(__file__), '1.csv')

numbers = [] # Массив чисел
# Чтение данных из файла
with open(file_path, 'r', encoding='utf-8') as file:
   for line in file:
        if line.strip():  # Пропускаем пустые строки
            number = float(line.rstrip('\n').replace(',', '.'))
            numbers.append(number)
numbers.sort() # Сортируем по возрастанию заранее

# Вычисления
average = sum(numbers) / len(numbers)
biased_variance = sum((x - average) ** 2 for x in numbers) / len(numbers)  # Смещённая дисперсия
unbiased_variance = sum((x - average) ** 2 for x in numbers) / (len(numbers) - 1) # Несмещённая дисперсия
biased_deviation = biased_variance ** 0.5  # Смещённое среднеквадратическое отклонение
unbiased_deviation = unbiased_variance ** 0.5  # Несмещённое среднеквадратическое отклонение

# Создание интервального вариационного ряда
n = len(numbers)
counts = [11, 14, 8, 9, 5, 1, 2]
indexes = [1, 12, 26, 34, 43, 48, 49, 50]
min_val, max_val = min(numbers), max(numbers)
bin_edges = [numbers[i-1] for i in indexes]
bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
relative_frequencies = [freq / n for freq in counts]

# Вывод интервалов, количества чисел и самих чисел
for i in range(len(bin_edges) - 1):
    left_edge = bin_edges[i]
    right_edge = bin_edges[i + 1]
    if i == len(bin_edges) - 2:
        interval_elements = [x for x in numbers if left_edge <= x <= right_edge]
    else:
        interval_elements = [x for x in numbers if left_edge <= x < right_edge]
    print(f"Интервал [{left_edge:.3f}, {right_edge:.3f}] содержит {len(interval_elements)} элементов: {interval_elements}")

# Вывод вычислений
print("\nВычисления:")
print(f"Среднее значение: {average:.5f}")
print(f"Смещённая дисперсия: {biased_variance:.5f}")
print(f"Несмещённая дисперсия: {unbiased_variance:.5f}")
print(f"Смещённое стандартное отклонение: {biased_deviation:.5f}")
print(f"Несмещённое стандартное отклонение: {unbiased_deviation:.5f}")
print(indexes)

# Создание графиков
plt.figure(figsize=(15, 5))

# 1. Полигон частот
plt.subplot(1, 2, 1)
plt.plot(bin_centers, counts, marker='o', linestyle='-', color='#1f77b4')
plt.title('Полигон частот')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.grid(True)
plt.xticks(bin_edges, [f"{x:.3f}" for x in bin_edges], rotation=45)

# 2. Гистограмма
plt.subplot(1, 2, 2)
plt.hist(numbers, bins=bin_edges, density=True, color='#ff7f0e', edgecolor='#d94801')
plt.title('Гистограмма')
plt.xlabel('Интервалы')
plt.ylabel('Относительная частота')
plt.grid(True)
plt.xticks(bin_edges, [f"{x:.3f}" for x in bin_edges], rotation=45)


plt.tight_layout()
plt.show()