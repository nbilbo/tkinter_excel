import os
from tkinter import messagebox
from tkinter import filedialog
import typing

import pandas as pd
import numpy as np

from app.interface import Interface


class Controller:
    def __init__(self) -> None:
        self.interface = Interface()
        self.dataframe = None

        self.interface.add_button.config(command=self.add)
        self.interface.update_button.config(command=self.update)
        self.interface.delete_button.config(command=self.delete)
        self.interface.save_button.config(command=self.save)
        self.interface.load_button.config(command=self.load)

    
    def _convert_values(self, values: typing.List[str]) -> typing.List:
        """
        todo:
        the idea is convert each value to be correct inserted in the dataframe.
        """
        return values
    
    def start(self) -> None:
        self.interface.mainloop()
    
    def load(self) -> None:
        filename = self.interface.filename()
        
        if not os.path.exists(filename):
            messagebox.showerror('Error', f'{filename} not exists.')
        else:
            try:
                self.dataframe = pd.read_excel(filename, dtype='object', index_col=False)
                columns = list(self.dataframe.columns)
                rows = self.dataframe.to_numpy().tolist()
                self.interface.set_columns(columns)
                self.interface.set_rows(rows)
                self.interface.set_fields(columns)
            except Exception as error:
                messagebox.showerror('Error', str(error))

    def save(self) -> None:
        if self.dataframe is None:
            messagebox.showerror('Error', 'first load the file.')
        else:
            pathname = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[('xlsx files', '*.xlsx'), ('all files', '*')]
            ).strip().replace(' ', '_')
            if pathname:
                    try:
                        # filename, extension = os.path.splitext(pathname)
                        self.dataframe.to_excel(pathname, index=False)
                        messagebox.showinfo('Success', 'Saved.')
                    except Exception as error:
                        messagebox.showerror('Error', str(error))

    def add(self) -> None:
        if self.dataframe is None:
            messagebox.showerror('Error', 'first load the file.')
        else:
            values = self.interface.fields()
            self.dataframe.loc[len(self.dataframe)] = values
            rows = self.dataframe.to_numpy().tolist()
            self.interface.set_rows(rows)
            self.interface.clear_fields()
            messagebox.showinfo('Success', 'Row has been successfully added.')

    def update(self) -> None:
        values = self.interface.fields()
        index = self.interface.selection_index()

        if self.dataframe is None:
            messagebox.showerror('Error', 'first load the file.')
        elif index is None:
            messagebox.showerror('Error', 'Please, first select a row in the table.')
        else:
            self.dataframe.loc[index] = values
            rows = self.dataframe.to_numpy().tolist()
            self.interface.set_rows(rows)
            self.interface.clear_fields()
            messagebox.showinfo('Success', 'Row has been successfully updated.')

    def delete(self) -> None:
        index = self.interface.selection_index()

        if self.dataframe is None:
            messagebox.showerror('Error', 'first load the file.')
        elif index is None:
            messagebox.showerror('Error', 'Please, first select a row in the table.')
        else:
            columns = list(self.dataframe.columns)
            array = self.dataframe.to_numpy()
            array = np.delete(arr=array, obj=index, axis=0)
            self.dataframe = pd.DataFrame(data=array, columns=columns)
            rows = array.tolist()
            self.interface.set_rows(rows)
            self.interface.clear_fields()
            messagebox.showinfo('Success', 'Row has been successfully deleted.')