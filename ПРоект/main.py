import tkinter as tk
from tkinter import ttk
import sqlite3
#главный
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.db = db
        self.init_main() 
        self.view_records()
        

    #метод инициализации виджетов
    def init_main(self):
        #тулбар
        toolbar = tk.Frame(bg='#66CDAA', bd=10)    
        toolbar.pack(side=tk.TOP, fill=tk.X)

        #Кнопка добавления
        #PhotoImage - добавленное фото
        self.add_img = tk.PhotoImage(file='add.png')
        #фото-кнопка(image)
        #bg-фон
        #bd-граница
        btn_add = tk.Button(toolbar, text='Добавить', image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        #Кнопка редактирования
        self.redact_img = tk.PhotoImage(file='redact.png')
        btn_redact = tk.Button(toolbar, image=self.redact_img, command=self.open_update)
        btn_redact.pack(side=tk.LEFT, padx=10 )

        #Кнопка удаления
        self.del_img = tk.PhotoImage(file='delete.png')
        btn_del = tk.Button(toolbar, image=self.del_img, command=self.del_records)
        btn_del.pack(side=tk.LEFT )

         #Кнопка поиска
        self.search_img = tk.PhotoImage(file='see.png')
        btn_search = tk.Button(toolbar, image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT, padx=10)

        #Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)


        #таблица для вывода информации о контактах
        self.tree = ttk.Treeview(self, columns=('ID','name','phone','email','price'), show='headings', height=17)
        #настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=130, anchor=tk.CENTER)
        self.tree.column('email', width=130, anchor=tk.CENTER)
        self.tree.column('price', width=125, anchor=tk.CENTER)

        #названия для столбцов
        self.tree.heading('ID', text='Id')
        self.tree.heading('name',text='ФИО')
        self.tree.heading('phone',text='Номер телефона')
        self.tree.heading('email',text='Электронная почта')
        self.tree.heading('price',text='Зарплата')

        self.tree.pack()

    #метод  добавления в базу данных(посредник)
    def record(self, name, phone, email, price):
        self.db.insert_data(name, phone, email, price)
        self.view_records()

    #метод редактирования
    def upd_record(self, name, phone, email, price):
        id= self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name =?, phone= ?, email = ?, price = ?
            WHERE id = ?
                    ''',(name, phone, email, price, id))
        self.db.conn.commit()
        self.view_records()

    #метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id =?',
                                (self.tree.set(i,'#1'),))
        self.db.conn.commit()
        self.view_records()

    #метод поиска
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?',('%'+ name + '%',))
        r=self.db.cur.fetchall()
        for i in r:
            self.tree.insert('','end',values=i)

    
    #перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users')
        r= self.db.cur.fetchall()
        for i in r:
            self.tree.insert('','end',values=i)

    # Метод открытия окна добавления
    def open_child(self):
        Child()

    # Метод открытия окна редактирования
    def open_update(self):
        Update()

    # Метод открытия окна поиска
    def open_search(self):
        Search()


#класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    #метод создания виджетов дочернего окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        #перехват событий, происходящих в приложении
        self.grab_set()
        #перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text = 'ФИО')
        label_phone = tk.Label(self, text = 'Номер телефона')
        label_email = tk.Label(self, text = 'Электронная почта')
        label_price = tk.Label(self, text = 'Заработная плата')
        label_name.place(x=30, y=20)
        label_phone.place(x=30, y=55)
        label_email.place(x=30, y=90)
        label_price.place(x=30, y=125)


        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_price = tk.Entry(self)
        self.entry_name.place(x=198, y=20)
        self.entry_phone.place(x=198, y=55)
        self.entry_email.place(x=198, y=90)
        self.entry_price.place(x=198, y=125)

        #Закрыть команда
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=190, y=160)

        #Добавление команда
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(),
                                                              self.entry_phone.get(),
                                                              self.entry_email.get(),
                                                              self.entry_price.get()))
        self.btn_ok.place(x=290, y=160)


#класс редактирования 
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db=db
        self.default_date()

    def init_update(self):
        self.title('Изменение текущего сотрудника')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text='Сохранить')
        self.btn_upd.bind('<Button-1>', 
                          lambda ev: self.view.upd_record(self.entry_name.get(),
                                                          self.entry_phone.get(),
                                                          self.entry_email.get(),
                                                          self.entry_price.get()))
        self.btn_upd.bind('<Button-1>',lambda ev: self.destroy(),add='+')
        self.btn_upd.place(x=290, y=160)
    
    #метод автозаполнения формы
    def default_date(self):
        id =self.view.tree.set(self.view.tree.selection()[0],'#1')
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', id)
        row = self.db.cur.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_phone.insert(0,row[2])
        self.entry_email.insert(0,row[3])
        self.entry_price.insert(0,row[4])



#класс поиска окон
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    #метод создания виджетов дочернего окна
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        #перехват событий, происходящих в приложении
        self.grab_set()
        #перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x=10, y=25)
        

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=80, y=25)
        
      
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=200, y=70)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>',lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',lambda ev: self.destroy(),add='+')
        self.btn_ok.place(x=125, y=70)
    
     
#Класс БД
class Db:
    #cоздание соединения курсора и таблицы
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         price TEXT
            )''' )
        
    #метод добавления в базу данных
    def insert_data(self, name, phone, email, price ):
        self.cur.execute('''
                INSERT INTO users (name, phone, email, price)
                VALUES(?,?,?,?)
        ''',(name, phone, email, price))
        self.conn.commit()

if  __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(False, False)
    db=Db()
    app = Main(root)
    app.pack()

    root.mainloop()

