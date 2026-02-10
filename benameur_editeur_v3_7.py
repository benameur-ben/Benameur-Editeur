import os
import sys
import tkinter as tk
import customtkinter as ctk
import re
import threading
import queue
import time
from datetime import datetime

# --- Portability & Distribution Optimization ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_system_requirements():
    """ Basic dependency check for distribution stability """
    if sys.version_info < (3, 7):
        return False, "تطلب النسخة بايثون 3.7 أو أحدث."
    return True, "تم التحقق من النظام."

# --- Professional Palette ---
CLR_BG = "#05060A"
CLR_SIDEBAR = "#0D0F16"
CLR_PANEL = "#111827"
CLR_ACCENT = "#00D1FF"
CLR_TEXT = "#F1F5F9"
CLR_KEYWORD = "#F87171"
CLR_TYPE = "#60A5FA"

ctk.set_appearance_mode("dark")

# --- Standardized Data ---
REFERENCE_KEYWORDS = [
    ("algorithme", "اسم الخوارزمية"),
    ("var", "قسم التعريفات"),
    ("début", "بداية العمليات"),
    ("fin", "نهاية البرنامج"),
    ("lire", "إدخال (قراءة)"),
    ("écrire", "إخراج (طباعة)"),
    ("si ... alors", "شرط (إذا)"),
    ("pour i <-- start a end", "تكرار إسنادي"),
    ("<--", "تعيين قيمة"),
]

REFERENCE_TYPES = [
    ("entier", "رقم صحيح"),
    ("réel", "رقم حقيقي"),
    ("caractère", "حرف واحد"),
    ("chaîne", "نص طويل"),
    ("booléen", "صح/خطأ"),
]

# --- Core Engine ---
class BenameurEliteV37:
    def __init__(self, term_cb, input_cb, prog_cb):
        self.term = term_cb
        self.input_ui = input_cb
        self.prog = prog_cb
        self.symbols = {}

    def parse_vars(self, code):
        m = re.search(r"var(.*?)\bdébut\b", code, re.S | re.I)
        if m:
            for line in m.group(1).split("\n"):
                line = line.strip()
                match = re.search(r"([\w,\s]+):([\w\séà]+)", line, re.I)
                if match:
                    names = [n.strip() for n in match.group(1).split(",")]
                    vtype = match.group(2).strip().lower()
                    for n in names: self.symbols[n] = {"type": vtype, "value": 0 if vtype in ["entier", "réel"] else ""}

    def preprocess(self, code):
        body = re.search(r"début(.*?)\bfin\b", code, re.S | re.I)
        if not body: raise Exception("début/fin missing")
        lines = body.group(1).split("\n")
        py_lines = ["import time", "st = time.time()"]
        for var in self.symbols: py_lines.append(f"{var} = {repr(self.symbols[var]['value'])}")
        
        indent = 0
        for line in lines:
            line = line.strip()
            if not line: continue
            l_low = line.lower()
            if l_low in ["sinon", "finsi", "finpour", "fintantque"]: indent = max(0, indent - 1)
            pref = "    " * indent
            
            if l_low.startswith("écrire"): line = re.sub(r"écrire\s*\((.*)\)", r"print_func(\1)", line, flags=re.I)
            elif l_low.startswith("lire"):
                m = re.search(r"lire\s*\((.*)\)", line, re.I)
                if m: line = f"{m.group(1).strip()} = read_func('{m.group(1).strip()}')"
            elif l_low.startswith("si "):
                line = re.sub(r"si\s+(.*)\s+alors", r"if \1:", line, flags=re.I)
                line = re.sub(r"(?<![<>!])=(?!=)", "==", line); py_lines.append(f"{pref}{line}"); indent += 1; continue
            elif l_low.startswith("pour "):
                m = re.search(r"pour\s+(\w+)\s*<--\s*(.*)\s+a\s+(.*)\s+faire", line, re.I)
                if m:
                    v, start, end = m.groups()
                    py_lines.append(f"{pref}for {v} in range(int({start}), int({end}) + 1):")
                    indent += 1; continue
            elif l_low == "sinon": py_lines.append(f"{pref}else:"); indent += 1; continue
            elif "<--" in line:
                line = line.replace("<--", "=")
                line = re.sub(r"\bDIV\b", "//", line, flags=re.I).replace("MOD", "%")
            
            if l_low not in ["finsi", "finpour", "fintantque"]: py_lines.append(f"{pref}{line}")
        return "\n".join(py_lines)

    def run(self, code):
        self.symbols = {}; self.prog(True)
        try:
            self.parse_vars(code)
            py_code = self.preprocess(code)
            def p(*args): self.term(" ".join(map(str, args)) + "\n")
            def r(v):
                q = queue.Queue(); self.input_ui(f"Saisie {v}", q)
                val = q.get(); vt = self.symbols[v]['type']
                return int(val) if vt == "entier" else float(val) if vt in ["réel", "reel"] else str(val)
            exec(py_code, {"print_func": p, "read_func": r, "time": time, "range": range, "int": int, "float": float}, {})
            self.term("\n[SUCCÈS] تم التنفيذ بنجاح.", is_success=True)
        except Exception as e: self.term(f"\n[خطأ] {str(e)}", is_error=True)
        finally: self.prog(False)

# --- Elite UI V3.7 Pro ---

class BenameurFinalPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Benameur Editeur V3.7 - Pro Signature")
        self.geometry("1400x950")
        self.configure(fg_color=CLR_BG)
        
        # --- Load Logo ---
        try:
            logo_img_path = resource_path(os.path.join("assets", "logo.png"))
            if os.path.exists(logo_img_path):
                from PIL import Image
                self.logo_img = tk.PhotoImage(file=logo_img_path)
                self.wm_iconphoto(True, self.logo_img)
        except Exception as e:
            print(f"Could not load logo: {e}")

        self.interpreter = BenameurEliteV37(self.write_term, self.input_mgr, self.toggle_prog)
        self.setup_ui()
        self.load_sample()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=CLR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="BENAMEUR", font=("Orbitron", 28, "bold"), text_color=CLR_ACCENT).pack(pady=(50, 30))
        self.run_btn = ctk.CTkButton(self.sidebar, text="▶ EXÉCUTER", font=("Segoe UI", 15, "bold"), 
                                     fg_color="#0EA5E9", command=self.execute, height=45)
        self.run_btn.pack(fill="x", padx=20, pady=10)
        
        self.prog_bar = ctk.CTkProgressBar(self.sidebar, mode="indeterminate", progress_color=CLR_ACCENT)
        ctk.CTkButton(self.sidebar, text="📖 Aide Mémoire", fg_color="transparent", border_width=1, 
                       border_color="#1E293B", command=self.toggle_guide).pack(fill="x", padx=20, pady=20)

        # 2. Workspace
        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=20, pady=(20, 0))
        self.workspace.grid_rowconfigure(0, weight=4)
        self.workspace.grid_rowconfigure(1, weight=1)
        self.workspace.grid_columnconfigure(0, weight=1)

        self.editor = ctk.CTkTextbox(self.workspace, font=("Consolas", 18), fg_color=CLR_PANEL, text_color=CLR_TEXT)
        self.editor.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        self.terminal = ctk.CTkTextbox(self.workspace, font=("Consolas", 14), fg_color="#010409", text_color=CLR_ACCENT)
        self.terminal.grid(row=1, column=0, sticky="nsew")
        self.terminal.configure(state="disabled")

        # 3. CORRECTED STATUS BAR (Fixed BiDi Flipping)
        self.footer = ctk.CTkFrame(self, height=40, fg_color=CLR_SIDEBAR, corner_radius=0)
        self.footer.grid(row=1, column=1, columnspan=2, sticky="ew")
        
        # Consolidation into a single label to prevent order flipping between widgets
        # Using specific order for Middle East / Arabic text flow
        credit_text = "ثانوية الأخوين الشهيدين بوجلال - عين السلطان  •  برعاية أستاذ المعلوماتية: بن عامر محمد"
        
        self.sig_lbl = ctk.CTkLabel(self.footer, text=credit_text, font=("Segoe UI", 11, "bold"), text_color="#94A3B8")
        self.sig_lbl.pack(expand=True)

        # 4. Guide
        self.guide_panel = ctk.CTkFrame(self, width=320, fg_color=CLR_SIDEBAR, border_width=1, border_color="#1E293B")
        self.guide_panel.grid(row=0, column=2, rowspan=2, sticky="nsew")
        
        scr = ctk.CTkScrollableFrame(self.guide_panel, fg_color="transparent")
        scr.pack(fill="both", expand=True, padx=10, pady=10)
        self.build_section(scr, "Mots-Clés", REFERENCE_KEYWORDS, CLR_KEYWORD)
        self.build_section(scr, "Types de Données", REFERENCE_TYPES, CLR_TYPE)

    def build_section(self, master, label, data, col):
        ctk.CTkLabel(master, text=f"─ {label} ─", font=("Segoe UI", 12, "bold"), text_color="#475569").pack(pady=10)
        for t, d in data:
            f = ctk.CTkFrame(master, fg_color="#131722", corner_radius=6)
            f.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(f, text=t, font=("Consolas", 13, "bold"), text_color=col).pack(pady=(6,0))
            ctk.CTkLabel(f, text=d, font=("Segoe UI", 10), text_color="#94A3B8").pack(pady=(0,6))

    def toggle_guide(self):
        if self.guide_panel.winfo_viewable(): self.guide_panel.grid_remove()
        else: self.guide_panel.grid()

    def input_mgr(self, p, q):
        def show(): q.put(ctk.CTkInputDialog(text=p, title="Input").get_input() or "")
        self.after(0, show)

    def write_term(self, t, is_error=False, is_success=False):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", t)
        self.terminal.see("end"); self.terminal.configure(state="disabled")

    def toggle_prog(self, s):
        if s: self.prog_bar.pack(fill="x", padx=30, pady=10); self.prog_bar.start(); self.run_btn.configure(state="disabled")
        else: self.prog_bar.stop(); self.prog_bar.pack_forget(); self.run_btn.configure(state="normal")

    def execute(self):
        threading.Thread(target=self.interpreter.run, args=(self.editor.get("1.0", "end"),), daemon=True).start()

    def load_sample(self):
        self.editor.insert("1.0", "algorithme Benameur_Pro\nvar\n  i, n, s : entier\ndébut\n  écrire(\"Bienvenue dans l'édition Pro\")\n  écrire(\"Entrez n :\")\n  lire(n)\n  s <-- 0\n  pour i <-- 1 a n faire\n      s <-- s + i\n  finpour\n  écrire(\"Résultat : \", s)\nfin")

if __name__ == "__main__":
    app = BenameurFinalPro()
    app.mainloop()
