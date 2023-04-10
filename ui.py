import customtkinter as tk
from tkinter import ttk
from logic import Logic

class User_manager(Logic):
    def __init__(self) -> None:
        super().__init__()
        tk.set_appearance_mode('dark')
        tk.set_default_color_theme('blue')
        self.root = tk.CTk()
        
        self.root.geometry("800x500")
        self.root.title('User manager')
        self.root.resizable(False, False)

        # treeview styling
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#242424", foreground="white", rowheight=25, fieldbackground="#242424", bordercolor="#ffffff", borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])
        self.style.configure("Treeview.Heading", background="#3b3b3b", foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#3484F0')])

        # main frame
        self.main_frame = tk.CTkFrame(self.root)
        self.main_frame.pack(pady=90, padx=150, fill='both', expand=True)
        self.show_main_menu()

        self.start_add_user_tracers()

        # label message
        self.label_message = tk.StringVar()

        # list of warnings
        self.messages = []

        # error messages
        self.name_error = 'Name cannot contain numbers or special characters'
        self.lastname_error = 'Last name cannot contain numbers or special characters'
        self.phone_error = 'Make sure it is a valid phone number'

        # start
        self.root.mainloop()

    def start_add_user_tracers(self):

        # user name tracer
        self.name_str_var = tk.StringVar(name='name')
        self.name_str_var.trace_add('write', callback=self.input_validation_pivot)

        # lastname tracer
        self.lastname_str_var = tk.StringVar(name='lastname')
        self.lastname_str_var.trace_add('write', callback=self.input_validation_pivot)

        # email tracer
        self.email_str_var = tk.StringVar(name='email')
        self.email_str_var.trace_add('write', callback=self.input_validation_pivot)

        # phone number tracer
        self.phone_str_var = tk.StringVar(name='phone')
        self.phone_str_var.trace_add('write', callback=self.input_validation_pivot)

        # name input
        self.add_user_name_input = tk.CTkEntry(self.main_frame, height=33, textvariable=self.name_str_var)

        # lastname input
        self.add_user_ln_input = tk.CTkEntry(self.main_frame, textvariable=self.lastname_str_var, height=33)

        # email input
        self.add_user_email = tk.CTkEntry(self.main_frame, placeholder_text="Email", height=30, textvariable=self.email_str_var)

        # phone input
        self.add_user_phone = tk.CTkEntry(self.main_frame, placeholder_text="Phone number", height=30, textvariable=self.phone_str_var)


    def show_main_menu(self):
        self.clear_frame()
        self.main_frame.pack_configure(pady=90, padx=150)

        # welcome messagemain.py
        self.welcome_label = tk.CTkLabel(self.main_frame, text="Welcome dear user.\nPlease choose an option", font=('Arial', 16, 'bold'))
        self.welcome_label.pack(pady=45)

        # add user btn
        self.add_user_btn = tk.CTkButton(self.main_frame, text="Add a new user", width=200, font=('Arial', 12, 'bold'), command=self.show_add_user_frame)
        self.add_user_btn.pack(pady=10)

        # list all users btn
        self.list_user_btn = tk.CTkButton(self.main_frame, text="List all users", width=200, font=('Arial', 12, 'bold'), command=self.list_all_users)
        self.list_user_btn.pack()

    def show_add_user_frame(self):
        self.clear_frame()
        self.main_frame.pack_configure(pady=50, padx=150)

        # columns configuration
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # list all users button
        self.list_user_btn = tk.CTkButton(self.main_frame, text='List all users',  command=self.list_all_users)
        self.list_user_btn.grid(row=0, column=0, sticky=tk.W+tk.E, padx=(100, 10), pady=(25, 30))

        # go to home button
        self.back_home_btn = tk.CTkButton(self.main_frame, text="Go back to home", command=self.show_main_menu)
        self.back_home_btn.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(10, 100), pady=(25, 30))

        # name label
        self.add_user_name = tk.CTkLabel(self.main_frame, text="Name", text_color="#9e9e9e")
        self.add_user_name.grid(row=2, column=0, sticky=tk.W, padx=(72, 0))

        # name input
        self.add_user_name_input.grid(row=3, column=0, sticky=tk.W+tk.E, padx=(70, 5))
 
        # lastname label
        self.add_user_ln = tk.CTkLabel(self.main_frame, text="Last name", text_color="#9e9e9e")
        self.add_user_ln.grid(row=2, column=1, sticky=tk.W, padx=(7, 0))

        # lastname input
        self.add_user_ln_input.grid(row=3, column=1, sticky=tk.W+tk.E, padx=(5, 70))

        # email label
        self.add_user_ln = tk.CTkLabel(self.main_frame, text="Email", text_color="#9e9e9e")
        self.add_user_ln.grid(row=4, column=0, sticky=tk.W, padx=(72, 0), pady=(8, 0))

        # email input
        self.add_user_email.grid(row=6, columnspan=2, sticky=tk.W+tk.E, padx=70)

        # phone number label
        self.add_user_ln = tk.CTkLabel(self.main_frame, text="Phone number", text_color="#9e9e9e")
        self.add_user_ln.grid(row=7, column=0, sticky=tk.W, padx=(72, 0), pady=(8, 0))

        # phone number input    
        self.add_user_phone.grid(row=8, columnspan=2, sticky=tk.W+tk.E, padx=70)

        #label messages
        self.label_validation = tk.CTkLabel(self.main_frame, textvariable=self.label_message, text_color="red",)
        self.label_validation.grid(row=10, column=0, sticky='ew', padx=70, pady=(10, 0), columnspan=2)

        # register user btn
        self.register_user_btn = tk.CTkButton(self.main_frame, text="Register User", command=self.handle_submit)
        self.register_user_btn.grid(row=12, columnspan=2, sticky=tk.W+tk.E, pady=30, padx=70)

    def list_all_users(self):
        self.clear_frame()
        self.main_frame.pack_configure(pady=55, padx=130)

        # column configuration
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # add user btn
        self.list_user_btn = tk.CTkButton(self.main_frame, text='Add a new user',  command=self.show_add_user_frame)
        self.list_user_btn.grid(row=0, column=0, sticky=tk.W+tk.E, padx=(100, 10), pady=(25, 30))

        # go to home button
        self.back_home_btn = tk.CTkButton(self.main_frame, text="Go back to home", command=self.show_main_menu)
        self.back_home_btn.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(10, 100), pady=(25, 30))
        
        # treeview configuration
        self.users_list = ttk.Treeview(self.main_frame, height=11, selectmode='browse', )
        self.users_list['columns'] = ('name', 'lastname', 'email', 'phone')

        self.users_list.heading('#0', text='#', anchor='center')
        self.users_list.heading('name', text='Name')
        self.users_list.heading('lastname', text='Last Name')
        self.users_list.heading('email', text='email')
        self.users_list.heading('phone', text='Phone number')

        self.users_list.column('#0', anchor='w', width=50)
        self.users_list.column('name', anchor='center', width=90)
        self.users_list.column('lastname', anchor='center', width=90)
        self.users_list.column('email', anchor='center', width=190)
        self.users_list.column('phone', anchor='center', width=110)

        self.users_list.place(relx=0.5, rely=0.60, anchor='center')

        self.get_users()
        
        # insert values in treeview
        for i, row in enumerate(self.rows):
            data = eval(row.strip())
            self.users_list.insert('', 0, text=(i + 1), values=[data['name'], data['lastname'], data['email'], data['phoneNumber']])

    def clear_frame(self):
        for child in self.main_frame.winfo_children():
            child.pack_forget()
            child.grid_forget()
            child.place_forget()
    