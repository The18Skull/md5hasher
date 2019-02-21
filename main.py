from tkinter import *
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class app(Tk):
	class encoder(LabelFrame):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

			# Блок кнопок
			self.frame_buttons = Frame(self)
			self.frame_buttons.pack(side = TOP, expand = YES, fill = BOTH, pady = 5)
			# Кнопка "открыть файл"
			self.btn_open = Button(self.frame_buttons, text = "Из файла...", command = self.btn_open_action)
			self.btn_open.pack(side = LEFT, expand = YES, fill = BOTH)
			# Кнопка "получить хэш"
			self.btn_encode = Button(self.frame_buttons, text = "Получить хэш", command = self.btn_encode_action)
			self.btn_encode.pack(side = RIGHT, expand = YES, fill = BOTH)

			# Блок ввода
			self.frame_input = Frame(self)
			self.frame_input.pack(side = TOP, expand = YES, fill = BOTH, pady = 5)
			# Поле ввода
			self.txt_input = Text(self.frame_input, height = 10)
			self.txt_input.pack(side = LEFT, expand = YES, fill = BOTH)
			# Ползунок для просмотра всего поля
			self.scroll_input = Scrollbar(self.frame_input, command = self.txt_input.yview)
			self.txt_input.config(yscrollcommand = self.scroll_input.set)
			self.scroll_input.pack(side = RIGHT, fill = Y)

			# Поле вывода
			self.txt_output = Entry(self, width = 100, justify = CENTER, state = "readonly")
			self.txt_output.pack(side = TOP, expand = YES, fill = X)

		def set_input(self, text):
			# Изменить контент в поле ввода
			self.txt_input.delete("0.0", END)
			self.txt_input.insert("0.0", text)

		def set_output(self, text):
			# Изменить контент в поле вывода
			self.txt_output.config(state = "normal")
			self.txt_output.delete(0, END)
			self.txt_output.insert(0, text)
			self.txt_output.config(state = "readonly")

		def btn_open_action(self):
			# Открыть файл
			path = filedialog.askopenfilename()
			#print(path)
			if path:
				with open(path, "rb") as f:
					text = f.read()
					self.set_input("{0:s}".format(str(text))) # вывод прочитанной бинарки в поле ввода

		def btn_encode_action(self):
			# Начать хэшить по черному
			text = self.txt_input.get("0.0", END) # прочитать ввод в поле ввода
			print(text)
			# TODO: вызов хэш функции
			self.set_output("Вывод") # вывод результата в поле вывода хэша. принимает только str
			f = [[1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5]]
			self.master.master.frame_avalanche.set_plot(f) # если нужно както влиять на график снизу

	class avalanche(LabelFrame):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

			# Блок ввода инфы о изменении
			self.frame_change = Frame(self)
			self.frame_change.pack(side = TOP)
			# Приглашение ко вводу
			self.label_change = Label(self.frame_change, text = "Изменить бит номер:")
			self.label_change.pack(side = LEFT)
			# Поле ввода
			self.txt_change = Entry(self.frame_change, width = 10, justify = CENTER)
			self.txt_change.pack(side = LEFT, padx = 10)
			# Выполнить исследоваие
			self.btn_change = Button(self.frame_change, text = "Изменить", command = self.btn_change_action)
			self.btn_change.pack(side = LEFT)

			# Поле вывода промежуточного хэша
			self.txt_output = Entry(self, width = 100, justify = CENTER, state = "readonly")
			self.txt_output.pack(side = TOP, expand = YES, fill = X, pady = 5)

			# Блок графика
			self.frame_plot = Frame(self)
			self.frame_plot.pack(side = TOP, expand = YES, fill = BOTH)
			# Фигура
			self.fig = Figure(figsize = (5, 5), dpi = 100)
			self.fig.ax = self.fig.add_subplot(111)
			# Поле вывода графика
			self.canv_plot = FigureCanvasTkAgg(self.fig, self.frame_plot)
			# тулбар чет не работает:C
			# убрал это и заработало:D
			#self.canv_plot.draw()
			#self.canv_plot.get_tk_widget().pack(side = BOTTOM, expand = YES, fill = BOTH)
			self.toolbar_graph = NavigationToolbar2Tk(self.canv_plot, self.frame_plot)
			self.toolbar_graph.update()
			self.canv_plot._tkcanvas.pack(side = BOTTOM, expand = YES, fill = BOTH)

		def btn_change_action(self):
			text = self.master.master.frame_encoder.txt_output.get() # прочитать текущий зашифрованный хэш
			num = self.txt_change.get() # прочитать указанное колво бит
			print(text, num)
			# TODO: видимо какаета работа

		def set_output(self, text):
			# Изменить контент в поле вывода
			self.txt_output.config(state = "normal")
			self.txt_output.delete(0, END)
			self.txt_output.insert(0, text)
			self.txt_output.config(state = "readonly")

		def set_plot(self, plot):
			self.fig.ax.clear()
			self.fig.ax.plot(*plot)
			self.canv_plot.draw()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("Мегашифратор MD5")
		self.geometry("%dx%d" % (400, 600))

		self.frame_root = Frame(self)
		self.frame_root.pack(expand = YES, fill = BOTH)

		self.frame_encoder = self.encoder(self.frame_root, text = "MD5")
		self.frame_encoder.pack(expand = YES, fill = BOTH, padx = 5, ipadx = 5)

		self.frame_avalanche = self.avalanche(self.frame_root, text = "Лавинный эффект")
		self.frame_avalanche.pack(expand = YES, fill = BOTH, padx = 5, ipadx = 5)

if __name__ == "__main__":
	app().mainloop()