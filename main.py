import tkinter as tk
import tkinter.messagebox  # Импорт модуля для диалогового окна
import random

n = 20
speed = 0.7


class TMainForm:
    def __init__(self, root):
        self.imgmatrix = [[0] * n for _ in range(n)]
        self.weights = [[random.uniform(-0.3, 0.3) for _ in range(n)] for _ in range(n)]

        self.root = root
        self.canvas = tk.Canvas(root, width=n * 20, height=n * 20, bg="white")
        self.canvas.pack()

        self.BtnClear = tk.Button(root, text="Очистить", command=self.clear_image)
        self.BtnClear.pack()

        #self.BtnScale = tk.Button(root, text="Выровнять", command=self.scale_image)
        #self.BtnScale.pack()

        #self.BtnInitRandom = tk.Button(root, text="Случ. веса", command=self.init_random_weights)
        #self.BtnInitRandom.pack()

        self.BtnCheck = tk.Button(root, text="Проверить", command=self.check_image)
        self.BtnCheck.pack()

        self.BtnSaveWeights = tk.Button(root, text="Сохранить веса", command=self.save_weights)
        self.BtnSaveWeights.pack()

        self.BtnLoadWeights = tk.Button(root, text="Загрузить веса", command=self.load_weights)
        self.BtnLoadWeights.pack()

        self.canvas.bind("<Button-1>", self.draw)
        self.canvas.bind("<B1-Motion>", self.draw)

    def clear_image(self):
        self.canvas.delete("all")
        self.imgmatrix = [[0] * n for _ in range(n)]

    def scale_image(self):
        # Реализация масштабирования и выравнивания (локализации) изображения
        pass

    def init_random_weights(self):
        print("Нажата кнопка 'Случайные веса'")
        try:
            for i in range(n):
                for j in range(n):
                    self.weights[i][j] = random.uniform(-0.3, 0.3)
            self.SBStatus.set('')
        except Exception as e:
            print("Ошибка при установке случайных весов:", str(e))

    def draw(self, event):
        x = event.x // 20
        y = event.y // 20
        self.imgmatrix[y][x] = 1
        self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="black")

    def save_weights(self):
        filename = "weights.txt"
        if self.save_weights_to_file(filename):
            print("Веса сохранены в", filename)
        else:
            print("Ошибка сохранения весов")

    def load_weights(self):
        filename = "weights.txt"
        if self.load_weights_from_file(filename):
            print("Веса загружены из", filename)
        else:
            print("Ошибка загрузки весов")

    def save_weights_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                for i in range(n):
                    for j in range(n):
                        f.write(str(self.weights[i][j]) + '\n')
            return True
        except Exception as e:
            print("Ошибка при сохранении весов:", str(e))
            return False

    def load_weights_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                for i in range(n):
                    for j in range(n):
                        self.weights[i][j] = float(f.readline())
            return True
        except Exception as e:
            print("Ошибка при загрузке весов:", str(e))
            return False

    def check_image(self):
        sum = 0
        # Вычисляем сумму взвешенных значений
        for i in range(n):
            for j in range(n):
                sum += self.imgmatrix[i][j] * self.weights[i][j]

        if sum > 0:
            rety = 1  # Положительное изображение
        else:
            rety = 0  # Отрицательное изображение

        # Направление корректировки весов
        if rety == 1:
            question = "Точно такое же изображение. Правильно?"
        else:
            question = "Не такое же изображение. Правильно?"

        # Используем диалоговое окно для задания вопроса
        test = tk.messagebox.askyesno("Вопрос", question)

        if not test:
            if rety == 0:
                correction = 1
            else:
                correction = -1
            for i in range(n):
                for j in range(n):
                    self.weights[i][j] += speed * correction * self.imgmatrix[i][j]

            # Сохраняем измененные веса только если произошла коррекция
            self.save_weights()


if __name__ == "__main__":
    root = tk.Tk()
    app = TMainForm(root)
    root.mainloop()

