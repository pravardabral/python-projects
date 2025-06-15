#version 2.7
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesno, showerror
from tkinter.simpledialog import askinteger
from random import choice, randint
import pandas as pd
import matplotlib.pyplot as plot
import mysql.connector as sql

#global variables
options = {}
tables = []
question = ''
author = ''
sql_password = 'Pravar@123'

class pollApp:

    def __init__(self):

        #for clearing the placeholder text in question textbox
        def on_click_authbox(event):
            if self.auth_textbox.cget('fg') == 'grey':
                self.auth_textbox.delete(0, 'end') ; self.question_textbox.insert(0, '')
                self.auth_textbox.config(fg='black')

        #for clearing the placeholder text in question textbox
        def on_click_textbox(event):
            if self.question_textbox.cget('fg') == 'grey':
                self.question_textbox.delete(0, 'end') ; self.question_textbox.insert(0, '')
                self.question_textbox.config(fg='black')

        #for clearing the placeholder text in option textbox
        def on_click_optbox(event):
            if self.option_textbox.cget('fg') == 'grey':
                self.option_textbox.delete(0, 'end') ; self.option_textbox.insert(0, '')
                self.option_textbox.config(fg='black')

        #function for generating random poll data
        def rand_data():
                
            size = askinteger('Size', 'Enter the number of options:')
            low = askinteger('Lower limit', 'Enter the lower limit of random freqencies:')
            up = askinteger('Upper limit', 'Enter the upper limit of random frequencies:')

            if not size or not low or not up:
                pass
            else:
                global question, options
                question = 'Randomly generated poll'

                for i in range(size):
                    opt_color = ''
                    #for geneating names such as 'A', 'B', ... ,'Z', 'AA', 'BB',...
                    char = chr((i%26)+65)
                    opt_name = char * (i//26+1)

                    for _ in range(6): #generating a random 6-digit hexadecimal value for color
                        opt_color += choice(['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f'])
                        options[opt_name] = [randint(low, up), f"#{opt_color}"]
        
                self.setup_mainframe.pack_forget()
                self.resultStage() #calling the result app to show the results

        #used to add an option
        def add_option():
            global options, question, author #this is used to change the variables on the global scope
            opt_text = self.option_textbox.get() #getting whatever is in the option textbox

            self.option_textbox.delete(0, 'end') ; self.option_textbox.insert(0, '') #clearing the textbox after option has been added

            #updating the global variables
            options[opt_text] = [0, '#000000']
            question = self.question_textbox.get()
            author = self.auth_textbox.get()

            #creating and placing the radiobutton
            opt = Radiobutton(self.opt_frame, text=opt_text, variable=self.opt_var, value=self.opt_number, indicatoron=0, font=('Arial', 15))
            opt.grid(row=self.opt_row, column=3, padx=20, pady=5, columnspan=2)

            #creating and placing the label
            opt_label = Label(self.opt_frame, text=f'Option {self.opt_number+1}:', font=('Arial', 15))
            opt_label.grid(row=self.opt_row, column=0, padx=20, pady=5, columnspan=2)

            self.opt_list.append([opt, opt_label])
            self.opt_number += 1
            self.opt_row += 1

            current_table_name = author + question.removesuffix('?')
            sqlManager.add_table(current_table_name)
            sqlManager.insert_val(current_table_name, opt_text)

        #to associate a hex color value with the selected option
        def set_color():
            global options
            if self.opt_list: #if self.opt_list has any items
                color = askcolor()[1] #getting only the hex component
                opt_text = list(options)[self.opt_var.get()]

                self.opt_list[self.opt_var.get()][0].config(fg=color) #changing color of radiobutton
                self.opt_list[self.opt_var.get()][1].config(fg=color) #changing color of label

                options[opt_text][1] = color #updating the global options

                current_table_name = author + question.removesuffix('?')
                sqlManager.edit_val(current_table_name, opt_text, color=color)

            else: #if self.opt_list has no items
                showerror('No options!', 'There are no options!')       

        def display_past_results():
            row = 0
            if not tables:
                showerror('Error!', 'There are no results!')
            else:
                for (i, table_name) in enumerate(tables):
                    table_button = Radiobutton(self.table_frame, text=table_name, variable=self.table_var, value=i+1, indicatoron=0, font=('Arial', 15))
                    table_button.grid(row=i, column=0, columnspan=2)
                    row = i

                del_table_button = Button(self.table_frame, text='Delete result', command=hide_deleted_table, font=('Arial', 10))
                del_table_button.grid(row=row+1, column=0)

                show_result_button = Button(self.table_frame, text='Show result', command=show_table_result, font=('Arial', 10))
                show_result_button.grid(row=row+1, column=1)

        def hide_deleted_table():
            selected_opt = tables[self.table_var.get()-1]
            sqlManager.del_table(selected_opt)
            for i in self.table_frame.winfo_children():
                    i.grid_forget()
            display_past_results()
            
        def show_table_result():
            global question, options

            selected_opt = tables[self.table_var.get()-1]

            question = selected_opt
            for i in sqlManager.get_data(selected_opt):
                opt = i[0]
                freq = i[1]
                color = i[2]
                options[opt] = [freq, color]

            self.setup_mainframe.pack_forget()
            self.resultStage()

        #for removing the selected option    
        def remove():
            global options
            selected = self.opt_var.get() #index of the selected option
            if self.opt_list:
                del options[self.opt_list[selected][0].cget('text')] #delete selected option

                #remove selected option from the window
                for i in self.opt_list[selected]:
                    i.grid_forget()
                self.opt_list.pop(selected)

                #updating the numbering of the labels
                for (num, i) in enumerate(self.opt_list):
                    i[1].config(text=f'Option {num+1}:')
                    i[0].config(value=num)
                    self.opt_number = num+1
            else:
                showerror('No options!', 'There are no options!')

            #for removing all the options
        def delete():
            global options
            if askyesno('Confirm Removal', 'Do you want to remove all of the options?'):
                for i in self.opt_list: #removing options from window
                    for j in i:
                        j.grid_forget()

                #resetting the variables
                self.opt_number = 0
                self.opt_row = 0
                self.opt_list.clear()
                options.clear()

        def confirm():
            if not self.opt_list: #if self.opt_list is empty
                showerror('No Options', 'There are no options!')
            elif askyesno('Confirm', 'Do you want to proceed with the polling?'):
                self.setup_mainframe.pack_forget()
                self.pollingStage() #calling the pollingApp class

        self.window = Tk()
        self.h = self.window.winfo_screenheight()
        self.w = self.window.winfo_screenwidth()
        self.window.geometry(f'{self.w}x{self.h}')
        self.window.title('Poll Setup')

        self.setup_mainframe = Frame(self.window)
        self.setup_mainframe.pack(fill='y', side='top')
        
        #frame for storing the option randiobuttons and labels
        self.opt_frame = Frame(self.setup_mainframe)
        self.opt_frame.grid(row=3, column=0, columnspan=4)

        self.table_frame = Frame(self.setup_mainframe)
        self.table_frame.grid(row=6, column=0, columnspan=4)

        self.opt_var = IntVar()
        self.table_var = IntVar()
        self.opt_number = 0 #used for the "Option 2:", "Option 3:" etc. labels
        self.opt_row = 0 #used for placing options in the correct row
        self.opt_list = [] #local variable used for storing the option label, option radiobutton objects

        auth_label = Label(self.setup_mainframe, font=('Arial', 22), border=3, text='Author:')
        auth_label.grid(row=0, column=0)
        self.auth_textbox = Entry(self.setup_mainframe, font=('Arial', 22), border=5, fg='grey')
        self.auth_textbox.grid(row=0, column=1, padx=10, pady=5, sticky='NWES', columnspan=3)
        self.auth_textbox.insert(0, 'Enter name of Author')
        self.auth_textbox.bind('<FocusIn>', on_click_authbox)

        #question textbox
        self.question_textbox = Entry(self.setup_mainframe, font=('Arial', 25), border=5, fg='grey')
        self.question_textbox.grid(row=1, column=0, padx=10, pady=5, sticky='NWES', columnspan=4)
        self.question_textbox.insert(0, 'Enter a question here')
        self.question_textbox.bind('<FocusIn>', on_click_textbox)

        #option textbox
        self.option_textbox = Entry(self.setup_mainframe, font=('Arial', 20), border=2, fg='grey')
        self.option_textbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.option_textbox.insert(0, 'Enter an option here')
        self.option_textbox.bind('<FocusIn>', on_click_optbox)

        #add option button
        self.option_button = Button(self.setup_mainframe, text='Add option', command=add_option, font=('Arial', 15))
        self.option_button.grid(row=2, column=3, padx=10, pady=10, sticky='NWES')

        #remove the selected option
        self.remove_opt = Button(self.setup_mainframe, text='Remove', command=remove, font=('Arial', 15))
        self.remove_opt.grid(row=4, column=0, padx=5, pady=10, sticky='NWES')

        #removes all options
        self.remove_all = Button(self.setup_mainframe, text='Remove all', command=delete, font=('Arial', 15))
        self.remove_all.grid(row=4, column=1, padx=5, pady=10, sticky='NWES')

        #continue to pollingApp
        self.confirm_button = Button(self.setup_mainframe, text='Confirm', command=confirm, font=('Arial', 15))
        self.confirm_button.grid(row=4, column=2, padx=5, pady=10, sticky='NEWS')

        #change color of selected option
        self.change_color = Button(self.setup_mainframe, text='Change color', command=set_color, font=('Arial', 15))
        self.change_color.grid(row=4, column=3, padx=5, pady=10, sticky='NWES')

        self.rand_button = Button(self.setup_mainframe, text='Random Poll', command=rand_data, font=('Arial', 15))
        self.rand_button.grid(row=5, column=0, padx=5, pady=10, sticky='NWES', columnspan=2)

        self.past_results = Button(self.setup_mainframe, text='Past results', command=display_past_results, font=('Arial', 15))
        self.past_results.grid(row=5, column=2, padx=5, pady=10, sticky='NWES', columnspan=2)

        self.setup_mainframe.mainloop()

    def pollingStage(self):

        ''' app to take the poll '''

        #function for toggling submit confirmation
        def toggle():
            self.toggle_var = not self.toggle_var
            if not self.toggle_var:
                self.toggle_button.config(text='Submit confirmation: OFF')
            else:
                self.toggle_button.config(text='Submit confirmation: ON')

        #function for subbmitting the poll
        def submit():
            global options
            if self.opt_var.get() == 0:
                showerror('Invalid selection', 'Make a selection first')
            else:
                opt_text = list(options)[self.opt_var.get()-1]
                if not self.toggle_var or askyesno('Confirm submission', 'Do you want to submit? The next candidate will cast their poll after your submission.'):
                    self.candidate_number += 1
                    options[opt_text][0] += 1
                    self.candidate_label.config(text=f'Candidate {self.candidate_number}')

                    current_table_name = author + question.removesuffix('?')
                    sqlManager.edit_val(current_table_name, opt_text, True)

        #function for ending the poll and displaying the resutls
        def end():
            if askyesno('End Polling', 'Do you want to end the polling and proceed with the results?'):
                self.poll_mainframe.pack_forget()
                self.resultStage()

        self.window.title('Polling App')

        #mainframe containing all the widgets, packing it so it is centered in the window
        self.poll_mainframe = Frame(self.window)
        self.poll_mainframe.pack(fill='y')

        opt_frame = Frame(self.poll_mainframe)
        opt_frame.grid(row=2, column=0, columnspan=2)

        self.candidate_number = 1

        self.opt_var = IntVar()
        self.toggle_var = True

        #creating and displaying the candidate number and question labels
        self.candidate_label = Label(self.poll_mainframe, text=f'Candidate {self.candidate_number}', font=('Arial', 10))
        self.candidate_label.grid(row=0, column=0, columnspan=2, rowspan=1, pady=5, sticky='NWES')

        self.question_label = Label(self.poll_mainframe, text=f"Q: {question}", font=('Arial', 25))
        self.question_label.grid(row=1, column=0, columnspan=2, rowspan=1, pady=10)
    
        for (num, i) in enumerate(options): #for displaying the options
            self.opt = Radiobutton(opt_frame, text=f'{i}', variable=self.opt_var, value=num+1, indicatoron=0, fg=options[i][1], font=('Arial', 20), bd=5)
            self.opt.grid(row=num, column=0, columnspan=2, pady=10, sticky='NWES')

        #creating and displaying the end and submit buttons
        self.end_button = Button(self.poll_mainframe, text='End Poll', command=end, font=('Arial', 15))
        self.end_button.grid(row=3, column=1, pady=10)

        self.submit_button = Button(self.poll_mainframe, text='Submit', font=('Arial', 15), command=submit)
        self.submit_button.grid(row=3, column=0, pady=10)

        #button for toggling the submit confirmation
        self.toggle_button = Radiobutton(self.poll_mainframe, text='Submit confirmation: ON', indicatoron=0, command=toggle)
        self.toggle_button.grid(row=4, column=0, sticky='NWES', pady=10, columnspan=2)

    def resultStage(self):

        ''' displays the results '''

        #creating a dataframe from global options dictionary    
        poll_data = pd.DataFrame(options, index=['Freqency', 'Hex color']).T
        poll_data.index.name = 'Options'

        #extracting columns from the dataframe
        self.opt_names = poll_data.index
        self.freq = poll_data['Freqency']
        self.colors = poll_data['Hex color']

        #functions for displaying different charts
        def pie():
            plot.close()
            plot.axis('equal')
            plot.pie(self.freq, labels=self.opt_names, autopct='%1.1f%%', colors=self.colors)
            plot.show()
        
        def bar():
            plot.close()
            plot.bar(self.opt_names, self.freq, color=self.colors)
            plot.xlabel('Options') ; plot.ylabel('Number of people')
            plot.show()
        
        def line():
            plot.close()
            plot.plot(self.opt_names, self.freq, color='blue')
            plot.xlabel('Options') ; plot.ylabel('Number of people')
            plot.show()

        def scatter():
            plot.close()
            plot.scatter(self.opt_names, self.freq, color=self.colors)
            plot.xlabel('Options') ; plot.ylabel('Number of people')
            plot.show()

        self.window.title('Poll Results')

        result_mainframe = Frame(self.window)
        result_mainframe.pack(fill='y', side='top')        

        result_label = Label(result_mainframe, text='Poll Results', font=('Arial', 25))
        result_label.grid(row=0, column=0, columnspan=4, pady=5)

        question_label = Label(result_mainframe, text=f'Q: {question}', font=('Arial', 20))
        question_label.grid(row=1, column=0, columnspan=4, pady=10)

        #frame containing the options and freqency
        table = Frame(result_mainframe)
        table.grid(row=2, column=0, columnspan=4, pady=10)

        #creating and placing the column names inside table frame
        number_label = Label(table, text='S.No', font=('Arial', 15))
        number_label.grid(row=0, column=0, padx=25, pady=5)

        column_opt_label = Label(table, text='Options', font=('Arial', 15))
        column_opt_label.grid(row=0, column=1, padx=25, pady=5)

        column_freq_label = Label(table, text='Freqency', font=('Arial', 15))
        column_freq_label.grid(row=0, column=2, padx=25, pady=5)

        for (i, opt) in enumerate(options): #for displaying the options from the global variable

            opt_number = Label(table, text=f'{i+1}.', font=('Arial', 16))
            opt_number.grid(row=i+1, column=0)

            opt_label = Label(table, text=opt, fg=options[opt][1], font=('Arial', 16), border=5)
            opt_label.grid(row=i+1, column=1)

            freq_label = Label(table, text=options[opt][0], font=('Arial', 16))
            freq_label.grid(row=i+1, column=2)

        #creating and displaying the buttons for the different graphs
        bar_button = Button(result_mainframe, text='Bar graph', command=bar, font=('Arial', 10))
        bar_button.grid(row=3, column=0, padx=5, pady=5)

        pie_button = Button(result_mainframe, text='Pie graph', command=pie, font=('Arial', 10))
        pie_button.grid(row=3, column=1, padx=5, pady=5)

        line_button = Button(result_mainframe, text='Line graph', command=line, font=('Arial',10))
        line_button.grid(row=3, column=2, padx=5, pady=5)

        scatter_button = Button(result_mainframe, text='Scatter graph', command=scatter, font=('Arial', 10))
        scatter_button.grid(row=3, column=3, padx=5, pady=5)

class sqlManager:

    database = sql.connect(host='localhost', user='root', password=sql_password)
    db_cur = database.cursor()
    try:
        db_cur.execute('create database poll_data;')
    except sql.errors.DatabaseError:
        pass

    db_cur.execute('use poll_data;')
    
    def add_table(table_name : str):
        try:
            sqlManager.db_cur.execute(f'create table {table_name}(Opt varchar(40), Freq int, Color varchar(7));')
        except sql.errors.ProgrammingError:
            pass

    def del_table(table_name : str):
        global tables
        sqlManager.db_cur.execute(f'drop table {table_name}')
        tables.remove(table_name)

    def insert_val(table_name : str, opt : str, freq : int = 0, color : str = '#000000'):
        sqlManager.db_cur.execute(f'insert into {table_name} values ("{opt}", {freq}, "{color}");')

    def edit_val(table_name : str, opt : str, freq_bump : bool = False, color : str = '#000000'):
        if freq_bump:
            sqlManager.db_cur.execute(f'update {table_name} set Freq = Freq + 1, Color = "{color}" where Opt = "{opt}";')
        else:
            sqlManager.db_cur.execute(f'update {table_name} set Color = "{color}" where Opt = "{opt}";')

    def get_tables() -> list[str]:
        global tables
        sqlManager.db_cur.execute('show tables;')
        for i in sqlManager.db_cur.fetchall():
            tables.append(i[0])

        return tables
    
    def get_data(table_name : str):
        sqlManager.db_cur.execute(f'select * from {table_name};')

        return sqlManager.db_cur.fetchall()

tables = sqlManager.get_tables()
pollApp()
