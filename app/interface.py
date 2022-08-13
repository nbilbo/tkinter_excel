import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import typing

import ttkbootstrap
from ttkbootstrap.scrolled import ScrolledFrame

from app import constants


class Interface(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('tkinter excel demo 0.0.1')
        self.geometry('1100x600+0+0')
        self.icon = tk.PhotoImage(file=constants.ICON_IMAGE)
        self.iconphoto(False, self.icon)

        paned = ttk.Panedwindow(self, orient='horizontal')
        paned.pack(side='top', fill='both', expand=True)

        left = ttk.Frame(paned)
        left.config(padding=15)
        left.pack_propagate(False)
        paned.add(left, weight=2)

        right = ttk.Frame(paned)
        right.config(padding=15)
        right.pack_propagate(False)
        paned.add(right, weight=1)

        self.ask_file_name = AskFileName(left)
        self.ask_file_name.pack(side='top', fill='x', pady=10)

        self.load_button = ttk.Button(left)
        self.load_button.config(text='Load')
        self.load_button.pack(side='top', fill='x')

        self.table = Table(left)
        self.table.pack(side='top', fill='both', expand=True, pady=10)

        self.save_button = ttk.Button(left)
        self.save_button.config(text='Save')
        self.save_button.pack(side='top', fill='x')

        self.form = Form(right)
        self.form.pack(side='top', fill='both', expand=True)

        self.table.treeview.bind(
            '<<TreeviewSelect>>', 
            lambda event: self._auto_fill_fields()
        )

        self._apply_style()

    def _apply_style(self) -> None:
        def travel(widget: tk.Misc, font: str) -> None:
            if isinstance(widget, ttk.Entry):
                widget.config(font=font)
            for children in widget.winfo_children():
                travel(children, font)

        default_font = 'Consolas 14 normal'
        entry_font = 'Arial 14 normal'
        button_font = 'Consolas 14 bold'

        bootstrap_style = ttkbootstrap.Style()
        bootstrap_style.theme_use('darkly')

        style = ttk.Style()
        style.configure('.', font=default_font)
        style.configure('TLabel', font=default_font)
        style.configure('TButton', font=button_font)
        style.configure('Treeview', rowheight=40)
        style.configure('Treeview', font=entry_font)
        style.configure('Treeview.Heading', font=default_font)

        self.add_button['bootstyle'] = 'success'
        self.update_button['bootstyle'] = 'warning'
        self.delete_button['bootstyle'] = 'danger'
        self.ask_file_name.button['bootstyle'] = 'outline-default'
        self.form.clear_button['bootstyle'] = 'outline-default'
        self.form.container.vscroll['bootstyle'] = 'info'
        self.table.ver_scrollbar['bootstyle'] = 'info'
        self.table.hor_scrollbar['bootstyle'] = 'info'
        travel(self, entry_font)

    def _auto_fill_fields(self) -> None:
        selection = self.table.selection()
        if selection:
            self.form.fill_fields(selection)

    def set_columns(self, columns: typing.Iterable[str]) -> None:
        self.table.set_columns(columns)
    
    def set_rows(self, rows: typing.Iterable[typing.Iterable[str]]) -> None:
        self.table.set_rows(rows)
    
    def filename(self) -> str:
        return self.ask_file_name.filename()
    
    def fields(self) -> typing.List[str]:
        return self.form.fields()
    
    def set_fields(self, fields: typing.Iterable[str]) -> None:
        self.form.set_fields(fields)
        self._apply_style()
    
    def clear_fields(self) -> None:
        self.form.clear_fields()
    
    def selection(self) -> typing.Optional[typing.Tuple[str, ...]]:
        return self.table.selection()
    
    def selection_index(self) -> typing.Optional[int]:
        return self.table.selection_index()

    @property
    def add_button(self) -> ttk.Button:
        return self.form.add_button

    @property
    def update_button(self) -> ttk.Button:
        return self.form.update_button

    @property
    def delete_button(self) -> ttk.Button:
        return self.form.delete_button
    

class AskFileName(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self)
        self.entry.config(textvariable=self.entry_var)
        self.entry.config(justify='center')
        self.entry.pack(side='left', fill='both', expand=True)

        self.folder_image = tk.PhotoImage(file=constants.FOLDER_IMAGE)
        self.button = ttk.Button(self)
        self.button.config(text='...')
        self.button.config(image=self.folder_image)
        self.button.config(command=self._ask)
        self.button.pack(side='left')

    def _ask(self) -> None:
        file = filedialog.askopenfilename()
        self.entry_var.set(file)
    
    def filename(self) -> str:
        return self.entry_var.get()


class Table(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pack_propagate(False)

        self.hor_scrollbar = ttk.Scrollbar(self, orient='horizontal')
        self.hor_scrollbar.pack(side='bottom', fill='x')

        self.treeview = ttk.Treeview(self)
        self.treeview.config(show='headings')
        self.treeview.pack(side='left', fill='both', expand=True)

        self.ver_scrollbar = ttk.Scrollbar(self, orient='vertical')
        self.ver_scrollbar.pack(side='left', fill='y')

        self.hor_scrollbar.config(command=self.treeview.xview)
        self.treeview.config(xscrollcommand=self.hor_scrollbar.set)

        self.ver_scrollbar.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.ver_scrollbar.set)
    
    def set_columns(self, columns: typing.Iterable[str]) -> None:
        self.treeview.config(columns=columns)
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=1)
            self.treeview.column(column, minwidth=1)
            self.treeview.column(column, stretch=True)
            self.treeview.column(column, anchor='center')

    def set_rows(self, rows: typing.Iterable[typing.Iterable[str]]) -> None:
        self.treeview.delete(*self.treeview.get_children())
        for row in rows:
            self.treeview.insert('', 'end', values=row)
    
    def selection(self) -> typing.Optional[typing.Tuple[str, ...]]:
        selections = self.treeview.selection()
        if selections:
            values = self.treeview.item(selections[0])['values']
            return tuple(str(value) for value in values)
        
        return None

    def selection_index(self) -> typing.Optional[int]:
        selections = self.treeview.selection()
        children = self.treeview.get_children()
        if selections:
            return children.index(selections[0])
        
        return None
    

class Form(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.clear_image = tk.PhotoImage(file=constants.CLEAR_IMAGE)
        self.clear_button = ttk.Button(self)
        self.clear_button.config(text='Clear')
        self.clear_button.config(image=self.clear_image)
        self.clear_button.config(command=self.clear_fields)
        self.clear_button.pack(side='top', anchor='e')

        self.container = ScrolledFrame(self) 
        self.container.pack(side='top', fill='both', expand=True)
        self.container.pack_propagate(False)

        self.delete_button = ttk.Button(self)
        self.delete_button.config(text='Delete')
        self.delete_button.pack(side='bottom', fill='x')

        self.update_button = ttk.Button(self)
        self.update_button.config(text='Update')
        self.update_button.pack(side='bottom', fill='x', pady=10)

        self.add_button = ttk.Button(self)
        self.add_button.config(text='Add')
        self.add_button.pack(side='bottom', fill='x')
    
    def set_fields(self, fields: typing.Iterable[str]) -> None:
        for children in self.container.winfo_children():
            children.destroy()
        
        for field in fields:
            text_field = TextField(self.container)
            text_field.label.config(text=field)
            text_field.pack(side='top', fill='x', pady=10)
    
    def fields(self) -> typing.List[str]:
        fields = []
        for field in self.container.winfo_children():
            fields.append(field.text())

        return fields

    def fill_fields(self, values: typing.Iterable[str]) -> None:
        fields = self.container.winfo_children()
        for index, field in enumerate(fields):
            field.set_text(values[index])
    
    def clear_fields(self) -> None:
        fields = self.container.winfo_children()
        for field in fields:
            field.set_text('')


class TextField(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = ttk.Label(self)
        self.label.config(anchor='center')
        self.label.pack(side='top', fill='x')

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self)
        self.entry.config(textvariable=self.entry_var)
        self.entry.config(justify='center')
        self.entry.pack(side='top', fill='x')

    def text(self) -> str:
        return self.entry_var.get()
    
    def set_text(self, text: str) -> None:
        self.entry_var.set(text)
