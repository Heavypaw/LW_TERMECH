import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

# Параметры системы
m = 2.0  # Масса шарика
M = 1.0  # Масса колеса
R = 1.0  # Радиус колеса
c = 40.0  # Жесткость пружины
g = 9.81  # Ускорение свободного падения

# Начальные условия
phi0 = np.pi / 3  # Начальный угол phi
psi0 = 0.0  # Начальный угол psi
omega_phi0 = 0.0  # Начальная угловая скорость phi
omega_psi0 = 0.0  # Начальная угловая скорость psi

# Временные параметры
t_max = 10  # Длительность анимации
fps = 30  # Частота кадров
t_eval = np.linspace(0, t_max, t_max * fps)


# Система дифференциальных уравнений
def system(t, y):
    phi, psi, omega_phi, omega_psi = y
    alpha = (phi + psi) / 2

    # Уравнения для вторых производных
    dphi_dt = omega_phi
    dpsi_dt = omega_psi

    # Матрица коэффициентов
    A = np.array([[1, np.cos(phi)],
                  [np.cos(phi), 1 + 2 * M / m]])

    # Вектор правых частей
    b = np.array([-2 * c / m * (1 - np.cos(alpha)) * np.sin(alpha) - g / R * np.sin(phi),
                  -2 * c / m * (1 - np.cos(alpha)) * np.sin(alpha) - omega_phi ** 2 * np.sin(phi)])

    # Решение системы линейных уравнений
    domega_dt = np.linalg.solve(A, b)

    return [dphi_dt, dpsi_dt, domega_dt[0], domega_dt[1]]


# Решение системы дифференциальных уравнений
sol = solve_ivp(system, [0, t_max], [phi0, psi0, omega_phi0, omega_psi0], t_eval=t_eval)

# Результаты
phi_values = sol.y[0]
psi_values = sol.y[1]

# Анимация системы
fig, ax = plt.subplots()
ax.set_xlim(-2 * R, 2 * R)
ax.set_ylim(-2 * R, 2 * R)
ax.set_aspect('equal')
ax.grid()

wheel = plt.Circle((0, R), R, color='blue', fill=False)
ball, = ax.plot([], [], 'ro')
spring, = ax.plot([], [], 'k-')
ax.add_patch(wheel)


def init():
    ball.set_data([], [])
    spring.set_data([], [])
    return wheel, ball, spring


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
    ball.set_data([x_ball], [y_ball])

    # Координаты пружины
    spring_x = [x_wheel, x_ball]
    spring_y = [y_wheel, y_ball]
    spring.set_data(spring_x, spring_y)

    return wheel, ball, spring


animation = FuncAnimation(fig, animate, frames=len(t_eval), init_func=init, interval=1000 / fps, blit=True)

plt.show()
