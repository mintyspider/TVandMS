import numpy as np
from scipy import stats
import os

file_path = os.path.join(os.path.dirname(__file__), '1.csv')

data = [] # Массив чисел
# Чтение данных из файла
with open(file_path, 'r', encoding='utf-8') as file:
   for line in file:
        if line.strip():  # Пропускаем пустые строки
            number = float(line.rstrip('\n').replace(',', '.'))
            data.append(number)

n = len(data)  # Размер выборки (50)
gamma = 0.95  # Уровень доверия
alpha = 1 - gamma
sigma = 3.0  # Известное стандартное отклонение

# 1. Выборочные характеристики
sample_mean = np.mean(data)
sample_std = np.std(data, ddof=1)  # Несмещённое стандартное отклонение
sample_var = sample_std ** 2
df = n - 1  # Степени свободы

# 2. Доверительный интервал для мат. ожидания (неизвестная дисперсия)
t_crit = stats.t.ppf(1 - alpha/2, df)
margin_error = t_crit * sample_std / np.sqrt(n)
ci_mean_unknown_var = (sample_mean - margin_error, sample_mean + margin_error)

print(f"1. Доверительный интервал для мат. ожидания (неизвестная дисперсия):")
print(f"   [{ci_mean_unknown_var[0]:.4f}, {ci_mean_unknown_var[1]:.4f}]")

# 3. Доверительный интервал для мат. ожидания (известная дисперсия = 9)
z_crit = stats.norm.ppf(1 - alpha/2)
margin_error_known_var = z_crit * sigma / np.sqrt(n)
ci_mean_known_var = (sample_mean - margin_error_known_var, sample_mean + margin_error_known_var)

print(f"2. Доверительный интервал для мат. ожидания (известная дисперсия = 9):")
print(f"   [{ci_mean_known_var[0]:.4f}, {ci_mean_known_var[1]:.4f}]")

# 4. Доверительный интервал для дисперсии
chi2_lower = stats.chi2.ppf(alpha/2, df)
chi2_upper = stats.chi2.ppf(1 - alpha/2, df)
ci_var_lower = (n - 1) * sample_var / chi2_upper
ci_var_upper = (n - 1) * sample_var / chi2_lower
ci_variance = (ci_var_lower, ci_var_upper)

print(f"3. Доверительный интервал для дисперсии:")
print(f"   [{ci_variance[0]:.4f}, {ci_variance[1]:.4f}]")