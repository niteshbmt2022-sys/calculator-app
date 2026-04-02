import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from sympy import *
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

class SymbolicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advance Calculator")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        self.expression = ""
        self.history = []
        self.is_scientific = False
        self.angle_mode = "Deg"
        
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<slash>", lambda e: self.on_slash_key())
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Top menu frame
        self.menu_frame = tk.Frame(self.root, bg="#2c3e50", height=28)
        self.menu_frame.pack(fill=tk.X)
        
        self.mode_btn = tk.Button(self.menu_frame, text="Scientific Calc", 
                                   command=self.toggle_mode, 
                                   bg="black", fg="white", 
                                   font=("Arial", 7, "bold"),
                                   padx=4, pady=1, relief=tk.FLAT)
        self.mode_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        info_label = tk.Label(self.menu_frame, 
                             text="ENTER=Calc | BK=Del", 
                             fg="#ecf0f1", bg="#2c3e50", font=("Arial", 6))
        info_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        menu_btn = tk.Button(self.menu_frame, text="Menu", 
                            command=self.show_menu, 
                            bg="black", fg="white", 
                            font=("Arial", 7, "bold"),
                            padx=4, pady=1, relief=tk.FLAT)
        menu_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Main container
        self.main_container = tk.Frame(self.root, bg="#ecf0f1")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Calculator frame
        self.calc_frame = tk.Frame(self.main_container, bg="#2c3e50")
        self.calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Display - Single only
        self.display = tk.Entry(self.calc_frame, 
                                font=("Arial", 18, "bold"), 
                                bg="#ecf0f1", fg="#2c3e50",
                                justify=tk.RIGHT, 
                                borderwidth=5)
        self.display.pack(fill=tk.X, padx=1, pady=2)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.calc_frame, bg="#2c3e50")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        self.create_basic_buttons()
        
        # History frame - REDUCED WIDTH
        self.history_frame = tk.Frame(self.main_container, bg="#34495e", width=100)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=2, pady=3)
        self.history_frame.pack_propagate(False)
        
        history_title = tk.Label(self.history_frame, text="H", 
                                 font=("Arial", 7, "bold"), 
                                 bg="#34495e", fg="white")
        history_title.pack(pady=1)
        
        self.history_listbox = tk.Listbox(self.history_frame, 
                                          bg="#2c3e50", fg="white",
                                          font=("Arial", 7),
                                          borderwidth=0,
                                          width=15)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Bind click event to history listbox
        self.history_listbox.bind("<Double-Button-1>", self.on_history_click)
        
        scrollbar = tk.Scrollbar(self.history_frame, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
    def create_basic_buttons(self):
        """Create basic calculator buttons"""
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        buttons = [
            ["AC", "(", ")", "%", "⌫"],
            ["7", "8", "9", "÷", "√"],
            ["4", "5", "6", "×", "^"],
            ["1", "2", "3", "-", "="],
            ["0", ".", "a", "b", "x"]
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                is_equal = btn_text == "="
                font_size = 30 if btn_text in ["-", "+", "=", "×", "÷", "%", "^", "!", "√", "∛"] else 28
                
                btn = tk.Button(self.buttons_frame, text=btn_text,
                               font=("Arial", 15, "bold"),
                               bg="blue" if is_equal else "black",
                               fg="white",
                               padx=2, pady=4,
                               relief=tk.FLAT,
                               command=lambda text=btn_text: self.on_button_click(text))
                
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
        
        for i in range(5):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
    
    def create_scientific_buttons(self):
        """Create scientific calculator buttons"""
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        buttons = [
            ["AC", "π", "e", "%", "⌫"],
            ["sin", "cos", "tan", "log", "ln"],
            ["√", "∛", "^", "!", "÷"],
            ["7", "8", "9", "(", "×"],
            ["4", "5", "6", ")", "-"],
            ["1", "2", "3", "a", "+"],
            ["0", ".", "b", "x", "="]
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                is_equal = btn_text == "="
                font_size = 30 if btn_text in ["-", "+", "=", "×", "÷", "%", "^", "!", "√", "∛", "(", ")"] else 28
                
                btn = tk.Button(self.buttons_frame, text=btn_text,
                               font=("Arial", 15, "bold"),
                               bg="blue" if is_equal else "black",
                               fg="white",
                               padx=1, pady=3,
                               relief=tk.FLAT,
                               command=lambda text=btn_text: self.on_button_click(text))
                
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
        
        for i in range(5):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
    
    def on_slash_key(self):
        """Handle / key from keyboard"""
        self.expression += "÷"
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        return "break"
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        char = event.char
        keysym = event.keysym
        
        # Handle / key
        if keysym == "slash" or char == "/":
            self.expression += "÷"
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
            return "break"
        
        if char.isdigit() or char in "+-×÷*.()abxπe^!%":
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif char == " ":
            return "break"
    
    def on_button_click(self, char):
        """Handle button clicks"""
        if char == "AC":
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif char == "=":
            self.calculate()
        elif char == "%":
            self.expression += "%"
            self.update_display()
        elif char == "√":
            self.expression += "sqrt("
            self.update_display()
        elif char == "∛":
            self.expression += "cbrt("
            self.update_display()
        elif char == "π":
            self.expression += "pi"
            self.update_display()
        elif char == "e":
            self.expression += "e"
            self.update_display()
        elif char == "sin":
            self.expression += "sin("
            self.update_display()
        elif char == "cos":
            self.expression += "cos("
            self.update_display()
        elif char == "tan":
            self.expression += "tan("
            self.update_display()
        elif char == "log":
            self.expression += "log("
            self.update_display()
        elif char == "ln":
            self.expression += "ln("
            self.update_display()
        elif char == "^":
            self.expression += "**"
            self.update_display()
        elif char == "!":
            self.expression += "!"
            self.update_display()
        elif char in ["a", "b", "x"]:
            self.expression += char
            self.update_display()
        else:
            self.expression += char
            self.update_display()
    
    def update_display(self):
        """Update display"""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
    
    def backspace(self):
        """Backspace function"""
        self.expression = self.expression[:-1]
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        return "break"
    
    def format_result(self, result_str):
        """Format result"""
        try:
            result_float = float(result_str)
            if result_float == int(result_float):
                return str(int(result_float))
            else:
                return f"{result_float:.10g}"
        except:
            return result_str
    
    def calculate(self):
        """Calculate symbolic expression"""
        try:
            expr_str = self.expression
            
            # Handle percentage: a%b = a/100*b (like 220%10 = 2.2 of 10 = 22)
            # Pattern: number%number
            expr_str = re.sub(r'(\d+\.?\d*)%(\d+\.?\d*)', r'(\1/100)*\2', expr_str)
            
            expr_str = expr_str.replace("÷", "/")
            expr_str = expr_str.replace("×", "*")
            expr_str = expr_str.replace("sqrt(", "sqrt(")
            expr_str = expr_str.replace("cbrt(", "cbrt(")
            expr_str = expr_str.replace("sin(", "sin(")
            expr_str = expr_str.replace("cos(", "cos(")
            expr_str = expr_str.replace("tan(", "tan(")
            expr_str = expr_str.replace("log(", "log(")
            expr_str = expr_str.replace("ln(", "ln(")
            expr_str = expr_str.replace("pi", "pi")
            expr_str = expr_str.replace("e", "E")
            
            expr_str = re.sub(r'(\d+)!', r'factorial(\1)', expr_str)
            
            transformations = standard_transformations + (implicit_multiplication_application,)
            parsed_expr = parse_expr(expr_str, transformations=transformations)
            
            variables = parsed_expr.free_symbols
            
            if variables:
                result = simplify(parsed_expr)
                result_str = str(result)
            else:
                result = parsed_expr.evalf()
                result_str = str(result)
                result_str = self.format_result(result_str)
            
            self.add_to_history(f"{self.expression}={result_str}")
            
            self.display.delete(0, tk.END)
            self.display.insert(0, result_str)
            self.expression = result_str
            
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
    
    def add_to_history(self, item):
        """Add to history"""
        timestamp = datetime.now().strftime("%H:%M")
        history_item = f"[{timestamp}] {item}"
        self.history.append(history_item)
        self.history_listbox.insert(0, history_item)
    
    def on_history_click(self, event):
        """Handle history item click - load into display for editing"""
        selection = self.history_listbox.curselection()
        if selection:
            selected_item = self.history_listbox.get(selection[0])
            # Extract the expression part (without timestamp)
            # Format: "[HH:MM] expression=result"
            if "=" in selected_item:
                expr_part = selected_item.split("=")[0]  # Get "expression" part
                expr_part = expr_part.split("] ")[1] if "] " in expr_part else expr_part
                self.expression = expr_part
                self.display.delete(0, tk.END)
                self.display.insert(0, expr_part)
    
    def toggle_mode(self):
        """Toggle mode"""
        self.is_scientific = not self.is_scientific
        
        if self.is_scientific:
            self.mode_btn.config(text="Basic")
            self.create_scientific_buttons()
        else:
            self.mode_btn.config(text="Scientific")
            self.create_basic_buttons()
    
    def show_menu(self):
        """Show menu"""
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu")
        menu_window.geometry("140x100")
        menu_window.resizable(False, False)
        
        clear_btn = tk.Button(menu_window, text="Clear",
                             command=self.clear_history,
                             bg="black", fg="white",
                             font=("Arial", 7, "bold"),
                             padx=6, pady=3, relief=tk.FLAT)
        clear_btn.pack(pady=2, fill=tk.X, padx=5)
        
        help_btn = tk.Button(menu_window, text="Help",
                            command=self.show_help,
                            bg="black", fg="white",
                            font=("Arial", 7, "bold"),
                            padx=6, pady=3, relief=tk.FLAT)
        help_btn.pack(pady=2, fill=tk.X, padx=5)
        
        close_btn = tk.Button(menu_window, text="Close",
                             command=menu_window.destroy,
                             bg="black", fg="white",
                             font=("Arial", 7, "bold"),
                             padx=6, pady=3, relief=tk.FLAT)
        close_btn.pack(pady=2, fill=tk.X, padx=5)
    
    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno("Clear", "Clear all?"):
            self.history.clear()
            self.history_listbox.delete(0, tk.END)
    
    def show_help(self):
        """Show help"""
        help_text = """Type: 5*6=30
Vars: a+a=2a
220%10=22
ENTER=Calc
Double-click history to edit"""
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SymbolicCalculator(root)
    root.mainloop()