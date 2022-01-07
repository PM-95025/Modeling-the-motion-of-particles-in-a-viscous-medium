from numpy import pi, arange
from tkinter import Tk, Entry, Label, DoubleVar
import tkinter
import unittest


def create_UI() -> tuple[float, ...]:
	"""
	Creates an UI of `Settings` window.

	:return: tuple of values received from the user
	"""
	window: Tk = Tk()
	window.title("Settings")
	window.geometry('400x250')

	v0_ = DoubleVar(window, value=0.0)
	R_ = DoubleVar(window, value=0.0)
	ro_ = DoubleVar(window, value=0.0)
	ro_fluid_ = DoubleVar(window, value=0.0)
	mu_ = DoubleVar(window, value=0.0)
	tmax_ = DoubleVar(window, value=0.0)
	dt_ = DoubleVar(window, value=0.0)
	dv_ = DoubleVar(window, value=0.0)

	font = ('Courier', 12)
	height = 20
	entry_width = 40
	label_width = 60

	labels = ['vₒ:', 'R:', 'ρ:', 'ρ_f:', 'μ:', 'tmax:', 'Δt:', 'Δv:']
	varnames = ['v0_', 'R_', 'ro_', 'ro_fluid_', 'mu_', 'tmax_', 'dt_', 'dv_']
	units = ['m/s', 'm', 'kg/m³', 'kg/m³', '', 's', 's', 'm/s']
	values = 8

	def create_Labels():
		for i in range(values):
			Label(window, text=labels[i], justify=tkinter.RIGHT, anchor='e', width=label_width, font=font).place(x=10, y=5+25*i, width=label_width, height=height)
		for i in range(values):
			Label(window, text=units[i], justify=tkinter.LEFT, anchor='w', width=label_width, font=font).place(x=130, y=5+25*i, width=label_width, height=height)
		pass

	def create_Entries(R_, height, ro_, ro_fluid_, mu_, tmax_, dt_, dv_):
		v0_entry = tkinter.Entry(window, width=entry_width, textvariable=v0_)
		v0_entry.focus()
		v0_entry.place(x=80, y=5, width=entry_width, height=20)

		for i in range(1, values):
			exec(f'tkinter.Entry(window, width=entry_width, textvariable={varnames[i]}).place(x=80, y=30+25*(i-1), width=entry_width, height=height)')

	def save(root: Tk):
		"""
		Closes the `root` window.
		"""
		root.destroy()

	create_Labels()
	create_Entries(R_, height, ro_, ro_fluid_, mu_, tmax_, dt_, dv_)

	buttonOk = tkinter.Button(window, text='Save', command=lambda: save(window))
	buttonOk.place(x=195, y=5, width=100, height=200)

	window.mainloop()

	return tuple([i.get() for i in (v0_, R_, ro_, ro_fluid_, mu_, tmax_, dt_, dv_)])


def FStocks(R: float, v: float, mu: float) -> float:
	"""

	:param R: radius of sphere
	:param v: velocity of body
	:param mu: fluid dynamic viscosity
	:return: friction force
	"""
	return 6 * pi * R * v * mu


def FTotal(R: float, ro: float, ro_fluid: float, v: float, mu: float, g: float) -> float:
	"""
	:param R: radius of sphere
	:param ro: body density
	:param ro_fluid:fluid density
	:param v: velocity of body
	:param mu: fluid dynamic viscosity
	:param g: acceleration of gravity
	:return: total force
	"""

	V = 4 / 3 * pi * R ** 3
	m = V * ro

	return m * g - (FStocks(R, v, mu) + ro_fluid * g * V)


t0: float = 0
s0: float = 0
g: float = 9.80665
'''
v0: float = 1
R: float = 0.01
ro: float = 4000
ro_fluid: float = 3000
mu: float = 0.9
tmax: float = 1e5
dt: float = 1e-3
v_eps = 1e-9
'''

v0, R, ro, ro_fluid, mu, tmax, dt, v_eps = create_UI()

v: float = v0
s: float = s0
t: float = t0

m: float = ((4 / 3 * pi * R ** 3) * ro)
v_expected = 2 / 9 * R ** 2 * g * (ro - ro_fluid) / mu

with open('checker.py', 'rt') as f:
	exec(f.read())
'''
for t in arange(t0 - dt, tmax, dt):
	Fcurr: float = FTotal(R, ro, ro_fluid, v, mu, g)
	a = Fcurr / m
	v += dt * a / 2
	s += dt * v
	print(f'{round(s, 5)} meters          {round(v, 5)} m/s          {Fcurr} N          {round(t, 5)} s')
	pass

'''
while (abs(v_expected - v) > v_eps) and t < tmax:
	Fcurr: float = FTotal(R, ro, ro_fluid, v, mu, g)
	a = Fcurr / m
	v += dt * a / 2
	s += dt * v
	t += dt
	print(f'{round(s, 5)} meters          {round(v, 100)} m/s          {Fcurr} N          {round(t, 5)} s')
print(f'v_exp = {v_expected} m/s')
