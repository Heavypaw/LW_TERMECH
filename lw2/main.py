import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import sympy as sp

# Параметры системы
R = 1.0  # Радиус колеса
m = 2.0  # Масса шарика
M = 1.0  # Масса колеса
c = 40.0  # Жесткость пружины
g = 9.81  # Ускорение свободного падения

# Временные параметры
t_max = 10  # Длительность анимации
fps = 30  # Частота кадров
t = np.linspace(0, t_max, t_max * fps)

# Функции для углов phi и psi
t_sym = sp.symbols('t')
phi_expr = sp.sin(2 * np.pi * t_sym / 5)  # Пример функции для phi
psi_expr = sp.cos(2 * np.pi * t_sym / 3)  # Пример функции для psi

phi_func = sp.lambdify(t_sym, phi_expr, 'numpy')
psi_func = sp.lambdify(t_sym, psi_expr, 'numpy')

phi_values = phi_func(t)  # Массив значений для phi
psi_values = psi_func(t)  # Массив значений для psi

# Инициализация фигуры
fig, ax = plt.subplots()
ax.set_xlim(-2 * R, 2 * R)
ax.set_ylim(-2 * R, 2 * R)
ax.set_aspect('equal')
ax.grid()

# Элементы системы
wheel = Circle((0, R), R, color='blue', fill=False)
ball, = ax.plot([], [], 'ro')
spring, = ax.plot([], [], 'k-')
ax.add_patch(wheel)


# Функция инициализации анимации
def init():
    ball.set_data([], [])
    spring.set_data([], [])
    return wheel, ball, spring


# Функция обновления анимации
def animate(i):
    phi = phi_values[i]
    psi = psi_values[i]

    # Положение центра колеса
    x_wheel = R * phi
    y_wheel = R

    # Положение шарика
    x_ball = x_wheel + R * np.sin(psi)
    y_ball = y_wheel - R * np.cos(psi)

    # Обновление положения элементов
    wheel.center = (x_wheel, y_wheel)

    # Передаем x_ball и y_ball как списки
    ball.set_data([x_ball], [y_ball])

    # Координаты пружины
    spring_x = [x_wheel, x_ball]
    spring_y = [y_wheel, y_ball]
    spring.set_data(spring_x, spring_y)

    return wheel, ball, spring


# Создание анимации
animation = FuncAnimation(fig, animate, frames=len(t), init_func=init, interval=1000 / fps, blit=True)

plt.show()
