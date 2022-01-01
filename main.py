from numpy import pi, arange
from tkinter import Tk, Entry, Button, Label
import tkinter
import unittest


def create_UI() -> tuple:
	"""
	Creates an UI of `Settings` window.

	:return: tuple of values received from the user
	"""
	window: Tk = Tk()
	window.title("Settings")
	window.geometry('400x250')

	Label(window, text='vₒ:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=5,
																									 width=30,
																									 height=20)
	v0_ = tkinter.DoubleVar(window, value=0.0)
	v0_entry = tkinter.Entry(window, width=40, textvariable=v0_)
	v0_entry.focus()
	v0_entry.place(x=50, y=5, width=40, height=20)

	Label(window, text='R:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=30,
																									width=30, height=20)
	R_ = tkinter.DoubleVar(window, value=0.0)
	R_entry = tkinter.Entry(window, width=40, textvariable=R_)
	R_entry.place(x=50, y=30, width=40, height=20)

	Label(window, text='ρ:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=55,
																									width=30, height=20)
	ro_ = tkinter.DoubleVar(window, value=0.0)
	ro_entry = tkinter.Entry(window, width=40, textvariable=ro_)
	ro_entry.place(x=50, y=55, width=40, height=20)

	Label(window, text='ρ_f:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=80,
																									  width=30,
																									  height=20)
	ro_fluid_ = tkinter.DoubleVar(window, value=0.0)
	ro_fluid_entry = tkinter.Entry(window, width=40, textvariable=ro_fluid_)
	ro_fluid_entry.place(x=50, y=80, width=40, height=20)

	Label(window, text='μ:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=105,
																									width=30, height=20)
	mu_ = tkinter.DoubleVar(window, value=0.0)
	mu_entry = tkinter.Entry(window, width=40, textvariable=mu_)
	mu_entry.place(x=50, y=105, width=40, height=20)

	Label(window, text='tmax:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=130,
																									   width=30,
																									   height=20)
	tmax_ = tkinter.DoubleVar(window, value=0.0)
	tmax_entry = tkinter.Entry(window, width=40, textvariable=tmax_)
	tmax_entry.place(x=50, y=130, width=40, height=20)

	Label(window, text='Δt:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=155,
																									 width=30,
																									 height=20)
	dt_ = tkinter.DoubleVar(window, value=0.0)
	dt_entry = tkinter.Entry(window, width=40, textvariable=dt_)
	dt_entry.place(x=50, y=155, width=40, height=20)

	Label(window, text='Δv:', justify=tkinter.RIGHT, anchor='e', width=80, font=('Arial', 12)).place(x=10, y=180,
																									 width=30,
																									 height=20)
	dv_ = tkinter.DoubleVar(window, value=0.0)
	dv_entry = tkinter.Entry(window, width=40, textvariable=dv_)
	dv_entry.place(x=50, y=180, width=40, height=20)

	def save():
		window.destroy()

	buttonOk = tkinter.Button(window, text='Save', command=save)
	buttonOk.place(x=105, y=5, width=100, height=200)

	window.mainloop()

	return v0_.get(), R_.get(), ro_.get(), ro_fluid_.get(), mu_.get(), tmax_.get(), dt_.get(), dv_.get()


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
while abs(v_expected - v) > v_eps:
	Fcurr: float = FTotal(R, ro, ro_fluid, v, mu, g)
	a = Fcurr / m
	v += dt * a / 2
	s += dt * v
	t += dt
	print(f'{round(s, 5)} meters          {round(v, 100)} m/s          {Fcurr} N          {round(t, 5)} s')
print(f'v_exp = {v_expected} m/s')
