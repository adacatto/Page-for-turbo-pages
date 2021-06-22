import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as fd
from tkinter.filedialog import asksaveasfilename
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests as requests
import io


class App(tk.Tk):
    def __init__(self):
        global textur
        global tex1
        global tex2
        global tex3
        global tex4

        super().__init__()
        self.title("Парсер турбо-страниц")

        tex1 = StringVar()
        tex2 = StringVar()
        tex3 = StringVar()
        tex4 = StringVar()

        btn_file = tk.Button(self, text="Выбрать карту сайта", command=self.choose_file)
        btn_gen = tk.Button(self, text="Генерация турбо-страниц", command=self.gen_file)
        btn_save = tk.Button(self, text="Сохранить файл", command=self.saving_file)

        lab1 = tk.Label(self, text='Тег для контента').grid(row=3, column=0)
        lab2 = tk.Label(self, text='Тег для картинки').grid(row=4, column=0)

        tex1_entry = tk.Entry(self, textvariable=tex1, bd=5).grid(row=3, column=1) 
        tex2_entry = tk.Entry(self, textvariable=tex2, bd=5).grid(row=4, column=1) 

        lab3 = tk.Label(self, text='Класс контента').grid(row=3, column=2)
        lab4 = tk.Label(self, text='Класс картинки').grid(row=4, column=2)

        tex3_entry = tk.Entry(self, textvariable=tex3, bd=5).grid(row=3, column=3) 
        tex4_entry = tk.Entry(self, textvariable=tex4, bd=5).grid(row=4, column=3) 
        textur = tk.Text(self, width=60, height=30)
        EventScrollBar = tk.Scrollbar(self, command=textur.yview, orient="vertical")

        textur.grid(column=0, row=6, columnspan=4)
        EventScrollBar.grid(column=4, row=6, sticky="ns")
        textur.configure(yscrollcommand=EventScrollBar.set)

        btn_file.grid(column=1, row=1, columnspan=2, sticky=NSEW)
        btn_gen.grid(column=1, row=5, columnspan=2, sticky=NSEW)
        btn_save.grid(column=2, row=10, columnspan=2, sticky=NSEW)

    def choose_file(self):
        global filename
        filetypes = (("Любой", "*"), ("Текстовые файлы", "*.txt"), ("HTML файлы", "*.html"), ("XML файл", "*.xml"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        if filename:
            labelfile = tk.Label(self, fg='green', text='Файл выбран!').grid(row=1, column=3)
            print(filename)

    def gen_file(self):
        tex1_value = tex1.get()
        tex2_value = tex2.get()
        tex3_value = tex3.get()
        tex4_value = tex4.get()

        opencarta = open(filename)
        soup = BeautifulSoup(opencarta, 'lxml')
        for vseurl in soup:
            vseurl = soup.find_all("loc")
            vseurl_text = [x.text for x in vseurl]
            print(vseurl_text)
            for tag in vseurl_text:
                resp = requests.get(tag)
                soup1 = BeautifulSoup(resp.text, 'lxml')
                content = soup1.find(tex1_value, class_=tex3_value)
                tit = soup1.title.text
                h = soup1.h1.text
                linkurl2 = resp.request.url  # найти url этой страницы
                linkurl1 = linkurl2[:linkurl2.find(".ru/")] + '.ru'  # найти url главной страницы
                if soup.find(tex2_value, class_=tex4_value) == None:  # если картинки в этом контейнере нет, 
                    imgscr = ''  # а она только в тексте, то вставлять пробел
                    turbo = '<?xml version="1.0" encoding="UTF-8"?>\n<rss xmlns:yandex="http://news.yandex.ru"\n ' \
                            'xmlns:media="http://search.yahoo.com/mrss/" \n xmlns:turbo="http://turbo.yandex.ru" \n ' \
                            'version="2.0"> <channel>\n <title>  (0) </title>\n <link> {0} </link>\n  ' \
                            '<description></description>\n <language>ru</language>\n <item turbo="true">\n <title> {' \
                            '1} </title> \n <link> {2} </link> \n <turbo:content><![CDATA[ \n <header> <figure> {3} ' \
                            '</figure> \n <h1> {4} </h1>  </header> \n  {5} \n ' \
                            ']]></turbo:content></item></channel></rss>'.format( 
                        linkurl1, tit, linkurl2, imgscr, h, content)
                    textur.insert(INSERT, turbo)
                else:
                    imgscr = soup.find(tex2_value, class_=tex4_value)  # иначе ссылку на фото
                    turbo = '<?xml version="1.0" encoding="UTF-8"?>\n<rss xmlns:yandex="http://news.yandex.ru"\n ' \
                            'xmlns:media="http://search.yahoo.com/mrss/" \n xmlns:turbo="http://turbo.yandex.ru" \n ' \
                            'version="2.0"> <channel>\n <title>  (0) </title>\n <link> {0} </link>\n  ' \
                            '<description></description>\n <language>ru</language>\n <item turbo="true">\n <title> {' \
                            '1} </title> \n <link> {2} </link> \n <turbo:content><![CDATA[ \n <header> <figure> {3} ' \
                            '</figure> \n <h1> {4} </h1>  </header> \n  {5} \n ' \
                            ']]></turbo:content></item></channel></rss>'.format(
                        linkurl1, tit, linkurl2, imgscr, h, content)
                    textur.insert(INSERT, turbo)

    def saving_file(self):
        save_text = asksaveasfilename(title="Сохранить файл", defaultextension="txt",
                                      filetypes=[("Любой", "*"), ("Текстовые файлы", "*.txt"), ("HTML файлы", "*.html"),
                                                 ("XML файл", "*.xml")])
        if not save_text:
            return
        with io.open(save_text, 'w+', encoding="UTF-8") as output_file:
            filetext = textur.get("1.0", tk.END)
            output_file.write(filetext)
            output_file.close()
            labelsave = tk.Label(self, fg='green', text='Файл сохранен!').grid(row=10, column=1)



if __name__ == "__main__":
    app = App()
    app.mainloop()
