import tkinter as tk
from idlelib.configdialog import font_sample_text
from tkinter import ttk
from tkinter import *

position = {"padx": 6, "pady": 6, "anchor": NW}
main_ch = ["Сумеречная Искорка",'Флаттершай', 'Рарити', 'Радуга Дэш', 'Пинки Пай', 'Эплджек']
evil_ch =['Кризалис', 'Король Сомбра', 'Коузи Глоу', 'Tирек', 'Дискорд', 'Лунная пони']
elements = ['Честность (Эпплджек)', 'Доброта (Флаттершай)', 'Смех (Пинки Пай)', 'Щедрость (Рарити)', 'Верность (Радуга Дэш)']
questions = ["1. Кто ваша любимая пони из главной шестёрки?","2. Почему именно она?","3. Самый потрясающий злодей?","4. За что вам нравится этот злодей?","5. Какой элемент гармонии вам ближе всего?"]
answers =[]

def one_of(spisok):
    window = Toplevel(hello)
    window.title(' вопрос')
    window.geometry('600x450+400+300')
    window.transient(hello)
    window.grab_set()
    if spisok ==main_ch:
        ttk.Label(window, text="1. Кто ваша любимая пони из главной шестёрки?").pack(side ='top')
    else:
        ttk.Label(window, text="3. Самый потрясающий злодей?").pack(side ='top')
    selected = StringVar()
    for i in spisok:
        lang_btn = ttk.Radiobutton(window, text= i, value= i,variable=selected)
        lang_btn.pack(**position)

    def next_q():
        user_ans = selected.get()
        answers.append(user_ans)
        window.destroy()
        why(user_ans)
    ttk.Button(window, text="Далее", command=next_q).pack(anchor = SE, side=BOTTOM, pady =10, padx = 10)

def why(user_ans):
    window = Toplevel(hello)
    window.title('1 вопрос')
    window.geometry('600x450+400+300')
    window.transient(hello)
    window.grab_set()

    def next_q():
        answers.append(entry.get())
        window.destroy()
        one_of(evil_ch)
    def last():
        answers.append(entry.get())
        window = Toplevel(hello)
        window.title(' вопрос')
        window.geometry('600x450+400+300')
        window.transient(hello)  # Связывает его с главным окном
        window.grab_set()
        def end():
            answers.append(selected_el.get())
            result_window = Toplevel(hello)
            result_window.title("конец")
            result_window.geometry("600x650+400+300")
            result_window.transient(hello)
            result_window.grab_set()

            last_image = PhotoImage(file='./end.png')
            title_label = ttk.Label(
                result_window, image=last_image,
                text="Спасибо за прохождение опроса! Вот ваши ответы:",
                font=("Arial", 14, "bold"),
                compound="top",
                justify="center"
            )
            title_label.pack(pady=15, side='top')
            title_label.image = last_image

            for i in range(5):
                q_frame = ttk.Frame(result_window)
                q_frame.pack(anchor="w", padx=20, pady=5, fill="x")

                q_label = ttk.Label(q_frame, text=f"{questions[i]}", font=("Arial", 10, "bold"))
                q_label.pack(anchor="w")

                a_label = ttk.Label(q_frame, text=answers[i], wraplength=550, justify="left")
                a_label.pack(anchor="w", padx=(10, 0))

            def finish_all():
                hello.destroy()

            finish_btn = ttk.Button(result_window, text="Завершить опрос", command=finish_all)
            finish_btn.pack(side="bottom", pady=20)

        elements_image = PhotoImage(file='./q2_elements.png')
        imtired = ttk.Label(window, image=elements_image, text="5. Какой элемент гармонии вам ближе всего?")
        imtired.image = elements_image
        imtired.pack(side='top')
        selected_el = StringVar()
        for i in elements:
            lang_btn = ttk.Radiobutton(window, text=i, value=i, variable=selected_el)
            lang_btn.pack(**position)
        ttk.Button(window, text="Закончить опрос", command= end).pack(anchor=SE, side=BOTTOM, pady=10, padx=10)

    if user_ans in main_ch:
        image_path = "./q2.png"
        ttk.Button(window, text="Далее", command= next_q).pack(anchor=SE, side=BOTTOM, pady=10, padx=10)
    else:
        image_path ="./q2_evil.png"
        ttk.Button(window, text="Далее", command= last).pack(anchor=SE, side=BOTTOM, pady=10, padx=10)

    q_image = PhotoImage(file= image_path)
    label2 = ttk.Label(window, image= q_image, text="Почему вам нравится этот герой?", compound="top")
    label2.pack()
    label2.image = q_image

    entry = ttk.Entry(window, width=100)
    entry.pack(padx=8, pady=8)

hello = Tk()
hello.title('My Little Pony: Friendship Is Magic опрос')
hello.geometry('600x450+400+300')
hello.resizable(False, False)
icon = PhotoImage(file="icon.png")
hello.iconphoto(True, icon)

h_i = PhotoImage(file="./hello_w.png")
label = ttk.Label(image=h_i, text="Привет, это короткий опрос по культовому шоу детства! Жми на кнопку, чтобы начать! :З", compound="top")
label.pack()

btn = ttk.Button(text="Начать", command=lambda: one_of(main_ch)) # создаем кнопку из пакета tkinter
btn.pack(anchor = SE, side=BOTTOM, pady =10, padx = 10)

hello.mainloop()