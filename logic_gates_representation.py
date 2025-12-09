import tkinter as tk
from tkinter import ttk, font

class LogicGateSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecture Notes: Logic Gate Simulator (ANSI Standard)")
        self.root.geometry("900x650")
        
        self.line_width = 3
        self.gate_fill = "white"
        self.gate_outline = "black"
        self.bg_color = "white"
        
        self.input_a_var = tk.IntVar(value=0)
        self.input_b_var = tk.IntVar(value=0)
        self.current_gate = "AND"

        self.setup_sidebar()
        self.setup_main_area()
        
        self.select_gate("AND")

    def setup_sidebar(self):
        sidebar = tk.Frame(self.root, width=200, bg="#f0f0f0", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="Select Gate", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Updated list to include both laws
        gates = ["AND", "OR", "NOT", "XOR", "NAND", "NOR", "XNOR", "De Morgan 1", "De Morgan 2"]
        for gate in gates:
            btn = ttk.Button(sidebar, text=gate, command=lambda g=gate: self.select_gate(g))
            btn.pack(fill="x", pady=2)

    def setup_main_area(self):
        main = tk.Frame(self.root, padx=20, pady=20, bg=self.bg_color)
        main.pack(side="right", expand=True, fill="both")

        self.header_label = tk.Label(main, text="AND Gate", font=("Arial", 18, "bold"), bg=self.bg_color)
        self.header_label.pack(pady=(0, 5))
        
        self.desc_label = tk.Label(main, text="", font=("Arial", 11), bg=self.bg_color, wraplength=600, justify="left")
        self.desc_label.pack(pady=(0, 20))

        sim_frame = tk.Frame(main, bd=2, relief="groove", bg="#f9f9f9", padx=10, pady=10)
        sim_frame.pack(fill="both", expand=True)

        controls = tk.Frame(sim_frame, bg="#f9f9f9")
        controls.pack(pady=10)
        
        self.btn_a = tk.Button(controls, text="A=0", font=("Consolas", 12, "bold"), 
                               command=lambda: self.toggle_input("A"), width=6, bg="#ffcccc")
        self.btn_a.grid(row=0, column=0, padx=20)
        
        self.btn_b = tk.Button(controls, text="B=0", font=("Consolas", 12, "bold"), 
                               command=lambda: self.toggle_input("B"), width=6, bg="#ffcccc")
        self.btn_b.grid(row=0, column=1, padx=20)

        self.canvas = tk.Canvas(sim_frame, width=550, height=220, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.output_label = tk.Label(sim_frame, text="OUTPUT: 0", font=("Consolas", 16, "bold"), bg="#f9f9f9")
        self.output_label.pack(pady=10)

    def toggle_input(self, input_name):
        if input_name == "A":
            val = self.input_a_var.get()
            self.input_a_var.set(1 - val)
        else:
            val = self.input_b_var.get()
            self.input_b_var.set(1 - val)
        self.update_logic()

    def select_gate(self, gate):
        self.current_gate = gate
        self.header_label.config(text=f"{gate} Logic")
        
        self.input_a_var.set(0)
        self.input_b_var.set(0)
        
        descriptions = {
            "AND": "The AND gate outputs HIGH (1) only when both inputs are HIGH.",
            "OR": "The OR gate outputs HIGH (1) if at least one input is HIGH.",
            "NOT": "The NOT gate (Inverter) outputs the opposite of the input.",
            "XOR": "The XOR (Exclusive OR) outputs HIGH if inputs are different.",
            "NAND": "NAND is an AND gate followed by a NOT gate.",
            "NOR": "NOR is an OR gate followed by a NOT gate.",
            "XNOR": "XNOR is an XOR gate followed by a NOT gate.",
            "De Morgan 1": "First Law: (A . B)' = A' + B'\nLeft: NAND Gate | Right: OR Gate with Inverted Inputs (Negative-OR)",
            "De Morgan 2": "Second Law: (A + B)' = A' . B'\nLeft: NOR Gate | Right: AND Gate with Inverted Inputs (Negative-AND)"
        }
        self.desc_label.config(text=descriptions.get(gate, ""))
        
        if gate == "NOT":
            self.btn_b.grid_remove()
        else:
            self.btn_b.grid()
            
        self.update_logic()
        self.draw_gate()

    def update_logic(self):
        a = self.input_a_var.get()
        b = self.input_b_var.get()
        res = 0
        gate = self.current_gate
        
        # Standard Gates
        if gate == "AND": res = a and b
        elif gate == "OR": res = a or b
        elif gate == "NOT": res = not a
        elif gate == "XOR": res = a ^ b
        elif gate == "NAND": res = not (a and b)
        elif gate == "NOR": res = not (a or b)
        elif gate == "XNOR": res = not (a ^ b)
        
        # De Morgan 1: (AB)' = A' + B'
        elif gate == "De Morgan 1":
            left = not (a and b)
            right = (not a) or (not b)
            self.output_label.config(text=f"(AB)'={int(left)}  |  A'+B'={int(right)}", fg="blue")
            self._update_buttons(a, b)
            return

        # De Morgan 2: (A+B)' = A' . B'
        elif gate == "De Morgan 2":
            left = not (a or b)
            right = (not a) and (not b)
            self.output_label.config(text=f"(A+B)'={int(left)}  |  A'.B'={int(right)}", fg="blue")
            self._update_buttons(a, b)
            return

        # Finalize Standard Gate Output
        res = 1 if res else 0
        self.output_label.config(text=f"OUTPUT: {res}", fg="#009900" if res else "#cc0000")
        self._update_buttons(a, b)

    def _update_buttons(self, a, b):
        self.btn_a.config(text=f"A={a}", bg="#ccffcc" if a else "#ffcccc")
        self.btn_b.config(text=f"B={b}", bg="#ccffcc" if b else "#ffcccc")

    def draw_gate(self):
        self.canvas.delete("all")
        
        if self.current_gate == "De Morgan 1":
            self._draw_demorgan_law1_scene()
            return
        elif self.current_gate == "De Morgan 2":
            self._draw_demorgan_law2_scene()
            return

        cx, cy = 275, 110
        gate = self.current_gate
        
        # Inputs
        if gate == "NOT":
            self.canvas.create_line(100, cy, 190, cy, width=2)
            self.canvas.create_text(90, cy, text="A", font=("Arial", 12, "bold"))
        else:
            self.canvas.create_line(100, cy-30, 190, cy-30, width=2)
            self.canvas.create_line(100, cy+30, 190, cy+30, width=2)
            self.canvas.create_text(90, cy-30, text="A", font=("Arial", 12, "bold"))
            self.canvas.create_text(90, cy+30, text="B", font=("Arial", 12, "bold"))

        tip_offset = 0 
        
        # Gate Body Logic
        if "AND" in gate and "NAND" in gate: 
            self._draw_and_shape(cx, cy)
            tip_offset = 60 + 10 
        elif "AND" in gate: 
            self._draw_and_shape(cx, cy)
            tip_offset = 60
        elif "XNOR" in gate:
            self._draw_xor_shape(cx, cy)
            tip_offset = 60 + 10
        elif "XOR" in gate:
            self._draw_xor_shape(cx, cy)
            tip_offset = 60
        elif "NOR" in gate:
            self._draw_or_shape(cx, cy)
            tip_offset = 60 + 10
        elif "OR" in gate:
            self._draw_or_shape(cx, cy)
            tip_offset = 60
        elif gate == "NOT":
            pts = [cx-30, cy-30, cx-30, cy+30, cx+30, cy]
            self.canvas.create_polygon(pts, fill=self.gate_fill, outline=self.gate_outline, width=self.line_width)
            tip_offset = 30 + 10

        # Bubbles
        if gate in ["NAND", "NOR", "XNOR", "NOT"]:
            bx = cx + 30 if gate == "NOT" else cx + 60
            self.canvas.create_oval(bx, cy-5, bx+10, cy+5, fill="white", outline="black", width=2)

        # Output Line
        start_x = cx + tip_offset
        self.canvas.create_line(start_x, cy, 450, cy, width=2)
        self.canvas.create_text(460, cy, text="Q", font=("Arial", 12, "bold"))

    def _draw_demorgan_law1_scene(self):
        cx1, cy = 130, 110
        
        # --- Left: NAND ---
        self.canvas.create_text(cx1-100, cy-30, text="A", font=("Arial", 10, "bold"))
        self.canvas.create_text(cx1-100, cy+30, text="B", font=("Arial", 10, "bold"))
        self.canvas.create_line(cx1-90, cy-30, cx1-40, cy-30, width=2)
        self.canvas.create_line(cx1-90, cy+30, cx1-40, cy+30, width=2)
        
        self._draw_and_shape(cx1, cy)
        self.canvas.create_oval(cx1+60, cy-5, cx1+70, cy+5, fill="white", outline="black", width=2)
        self.canvas.create_line(cx1+70, cy, cx1+100, cy, width=2)
        self.canvas.create_text(cx1, cy+60, text="NAND\n(A.B)'", font=("Arial", 10, "italic"))

        self.canvas.create_text(260, cy, text="=", font=("Arial", 30, "bold"))

        # --- Right: Negative-OR ---
        cx2, cy = 400, 110
        
        self.canvas.create_text(cx2-120, cy-30, text="A", font=("Arial", 10, "bold"))
        self.canvas.create_text(cx2-120, cy+30, text="B", font=("Arial", 10, "bold"))
        self.canvas.create_line(cx2-110, cy-30, cx2-80, cy-30, width=2)
        self.canvas.create_line(cx2-110, cy+30, cx2-80, cy+30, width=2)
        
        # NOT Gates (Triangles)
        self._draw_triangle_inverter(cx2-80, cy-30)
        self._draw_triangle_inverter(cx2-80, cy+30)

        # Connect NOTs to OR
        self.canvas.create_line(cx2-54, cy-30, cx2-35, cy-30, width=2)
        self.canvas.create_line(cx2-54, cy+30, cx2-35, cy+30, width=2)

        self._draw_or_shape(cx2, cy)
        self.canvas.create_line(cx2+60, cy, cx2+90, cy, width=2)
        self.canvas.create_text(cx2, cy+60, text="Negative-OR\nA' + B'", font=("Arial", 10, "italic"))

    def _draw_demorgan_law2_scene(self):
        cx1, cy = 130, 110
        
        # --- Left: NOR ---
        self.canvas.create_text(cx1-100, cy-30, text="A", font=("Arial", 10, "bold"))
        self.canvas.create_text(cx1-100, cy+30, text="B", font=("Arial", 10, "bold"))
        self.canvas.create_line(cx1-90, cy-30, cx1-40, cy-30, width=2)
        self.canvas.create_line(cx1-90, cy+30, cx1-40, cy+30, width=2)
        
        self._draw_or_shape(cx1, cy)
        self.canvas.create_oval(cx1+60, cy-5, cx1+70, cy+5, fill="white", outline="black", width=2) # Bubble
        self.canvas.create_line(cx1+70, cy, cx1+100, cy, width=2)
        self.canvas.create_text(cx1, cy+60, text="NOR\n(A+B)'", font=("Arial", 10, "italic"))

        self.canvas.create_text(260, cy, text="=", font=("Arial", 30, "bold"))

        # --- Right: Negative-AND ---
        cx2, cy = 400, 110
        
        self.canvas.create_text(cx2-120, cy-30, text="A", font=("Arial", 10, "bold"))
        self.canvas.create_text(cx2-120, cy+30, text="B", font=("Arial", 10, "bold"))
        self.canvas.create_line(cx2-110, cy-30, cx2-80, cy-30, width=2)
        self.canvas.create_line(cx2-110, cy+30, cx2-80, cy+30, width=2)
        
        # NOT Gates (Triangles)
        self._draw_triangle_inverter(cx2-80, cy-30)
        self._draw_triangle_inverter(cx2-80, cy+30)

        # Connect NOTs to AND
        self.canvas.create_line(cx2-54, cy-30, cx2-40, cy-30, width=2)
        self.canvas.create_line(cx2-54, cy+30, cx2-40, cy+30, width=2)

        self._draw_and_shape(cx2, cy)
        self.canvas.create_line(cx2+60, cy, cx2+90, cy, width=2)
        self.canvas.create_text(cx2, cy+60, text="Negative-AND\nA' . B'", font=("Arial", 10, "italic"))

    def _draw_triangle_inverter(self, x, y):
        # Draws a small NOT gate (triangle + bubble) starting at x, centered vertically at y
        # Triangle
        self.canvas.create_polygon(x, y-10, x, y+10, x+20, y, 
                                   fill="white", outline="black", width=2)
        # Bubble
        self.canvas.create_oval(x+20, y-3, x+26, y+3, fill="white", outline="black", width=2)

    def _draw_and_shape(self, cx, cy):
        self.canvas.create_line(cx-40, cy-40, cx+10, cy-40, width=self.line_width)
        self.canvas.create_line(cx-40, cy+40, cx+10, cy+40, width=self.line_width)
        self.canvas.create_line(cx-40, cy-40, cx-40, cy+40, width=self.line_width)
        self.canvas.create_arc(cx-40, cy-40, cx+60, cy+40, start=-90, extent=180, 
                               style=tk.ARC, width=self.line_width, outline="black")

    def _draw_or_shape(self, cx, cy):
        points = [
            cx-40, cy-40,
            cx+10, cy-35,
            cx+60, cy,
            cx+10, cy+35,
            cx-40, cy+40,
            cx-20, cy
        ]
        self.canvas.create_polygon(points, smooth=True, fill=self.gate_fill, 
                                   outline=self.gate_outline, width=self.line_width, splinesteps=30)

    def _draw_xor_shape(self, cx, cy):
        back_arc_pts = [cx-55, cy-40, cx-35, cy, cx-55, cy+40]
        self.canvas.create_line(back_arc_pts, smooth=True, width=self.line_width)
        shift = 10
        points = [
            cx-40+shift, cy-40,  
            cx+10+shift, cy-35,  
            cx+60, cy,     
            cx+10+shift, cy+35,  
            cx-40+shift, cy+40,  
            cx-20+shift, cy      
        ]
        self.canvas.create_polygon(points, smooth=True, fill=self.gate_fill, 
                                   outline=self.gate_outline, width=self.line_width, splinesteps=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicGateSimulator(root)
    root.mainloop()