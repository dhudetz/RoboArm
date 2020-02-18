"""
Created on 2/17/20
Marquette Robotics Club
Tyler Jones

Purpose: tkinter GUI for simulate.py
"""

import tkinter as tk


TK_TITLE = 'MU Robotics Arm Simulator Config'
TK_WINDOW_X = 550
TK_WINDOW_Y = 650
TK_BG_COLOR = 'black'
TK_PHOTO_MUR = 'mur_small.png'
TK_FONT_MAIN = ('Helvetica bold', 35)
TK_FONT_SECOND = ('Times', 20)
TK_FONT_THIRD = ('Times 20 underline')
TK_FONT_ENTRY = ('Helvetica', 16)
TK_FONT_BUTTON = ('Courier', 25)

response_active = False



a = 31.5
b = 31.5
c = 7
z_resolution = 0
a_resolution = 0


def isnum(a):
    try:
        _ = float(a)
        return True
    except ValueError:
        return False


class TkLauncher:
    def __init__(self):
        global response_active
        self.main = tk.Tk()
        self.main.title(TK_TITLE)
        self.main.geometry(str(TK_WINDOW_X) + 'x' + str(TK_WINDOW_Y))
        self.main.configure(bg=TK_BG_COLOR)


        self.mur_image = tk.PhotoImage(file=TK_PHOTO_MUR)
        self.im_label = tk.Label(image=self.mur_image, 
        borderwidth=0, highlightthickness=0, padx=100, pady=10,
        bg='black')
        self.im_label.grid(row=0, column=1)


        self.hzl = tk.Frame(height=2, width=TK_WINDOW_X - int(TK_WINDOW_X / 8), 
        bd=1, relief=tk.SUNKEN)
        self.hzl.grid(row=1, column=1, padx=5, pady=5)


        self.main_label = tk.Label(self.main, text='Generate Simulation Data', 
        font=TK_FONT_MAIN, bg='black', fg='white')
        self.main_label.grid(row=2, column=1)

        self.hzl = tk.Frame(height=2, width=TK_WINDOW_X - int(TK_WINDOW_X / 8), 
        bd=1, relief=tk.SUNKEN, bg='black', borderwidth=0)
        self.hzl.grid(row=3, column=1, padx=5, pady=15)


        self.sec_label_a = tk.Label(self.main, text='a - Shoulder to Elbow (cm)', 
        font=TK_FONT_SECOND, bg='black', fg='white')
        self.sec_label_a.grid(row=4, column=1, sticky='w', padx=10)

        self.sec_button_a = tk.Entry(self.main, fg='white',
        bg='black', font=TK_FONT_ENTRY)
        self.sec_button_a.grid(row=5, column=1, sticky='w', padx=10)

        self.sec_label_b = tk.Label(self.main, text='b - Elbow to Wrist (cm)', 
        font=TK_FONT_SECOND, bg='black', fg='white')
        self.sec_label_b.grid(row=6, column=1, sticky='w', padx=10)

        self.sec_button_b = tk.Entry(self.main, fg='white',
        bg='black', font=TK_FONT_ENTRY)
        self.sec_button_b.grid(row=7, column=1, sticky='w', padx=10)

        self.sec_label_c = tk.Label(self.main, text='c - Wrist to POI (cm)', 
        font=TK_FONT_SECOND, bg='black', fg='white')
        self.sec_label_c.grid(row=8, column=1, sticky='w', padx=10)

        self.sec_button_c = tk.Entry(self.main, fg='white',
        bg='black', font=TK_FONT_ENTRY)
        self.sec_button_c.grid(row=9, column=1, sticky='w', padx=10)

        self.sec_label_zr = tk.Label(self.main, text='zr - Height Resolution (cm/pixel)', 
        font=TK_FONT_SECOND, bg='black', fg='white')
        self.sec_label_zr.grid(row=10, column=1, sticky='w', padx=10)

        self.sec_button_zr = tk.Entry(self.main, fg='white',
        bg='black', font=TK_FONT_ENTRY)
        self.sec_button_zr.grid(row=11, column=1, sticky='w', padx=10)

        self.sec_label_ar = tk.Label(self.main, text='ar - Angle Resolution (cm/pixel)', 
        font=TK_FONT_SECOND, bg='black', fg='white')
        self.sec_label_ar.grid(row=12, column=1, sticky='w', padx=10)

        self.sec_button_ar = tk.Entry(self.main, fg='white',
        bg='black', font=TK_FONT_ENTRY)
        self.sec_button_ar.grid(row=13, column=1, sticky='w', padx=10)


        self.main_button_generate = tk.Button(self.main, text='Generate',
        font=TK_FONT_BUTTON, command=lambda : 
        self.generate(self.main_label_response))
        self.main_button_generate.grid(row=11, column=1, sticky='e', padx=50)

        self.sec_label_r = tk.Label(self.main, text='Status', 
        font=TK_FONT_THIRD, bg='black', fg='white')
        self.sec_label_r.grid(row=13, column=1, sticky='e', padx=100)

        self.main_label_response = tk.Label(self.main, text='Standby',
        font=TK_FONT_BUTTON, bg='black', fg='green')
        self.main_label_response.grid(row=14, column=1, sticky='e', padx=60)
    
    def generate(self, resp: tk.Label):
        global a, b, c, z_resolution, a_resolution, response_active
        if not response_active:
            response_active = True
            resp.config(text='Generating...', fg='yellow')

            # VARIABLES
            a = self.sec_button_a.get()
            b = self.sec_button_b.get()
            c = self.sec_button_c.get()
            z_resolution = self.sec_button_zr.get()
            a_resolution = self.sec_button_ar.get()

            if not isnum(a):
                resp.config(text='ERROR\n\'a\' is not\na number!', fg='red')
                resp.grid(padx=30)
            elif not isnum(b):
                resp.config(text='ERROR\n\'b\' is not\na number!', fg='red')
                resp.grid(padx=30)
            elif not isnum(c):
                resp.config(text='ERROR\n\'c\' is not\na number!', fg='red')
                resp.grid(padx=30)
            elif not isnum(z_resolution):
                resp.config(text='ERROR\n\'Height Resolution\' is \nnot a \nnumber!', fg='red')
                resp.grid(padx=30)
            elif not isnum(a_resolution):
                resp.config(text='ERROR\n\'Angle Resolution\' is \nnot a \nnumber!', fg='red')
                resp.grid(padx=30)
            else:
                a = float(a)
                b = float(b)
                c = float(c)
                z_resolution = float(z_resolution)
                a_resolution = float(a_resolution)

                # GENERATION CODE GOES HERE

                resp.config(text='Values \ngenerated!', fg='cyan')
                resp.grid(padx=20)
            response_active = False
        else:
            print('[WARNING] Already generating! Can\'t generate again')


app = TkLauncher()
app.main.mainloop()