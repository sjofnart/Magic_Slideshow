import customtkinter as ctk

class PopupConfigTimer(ctk.CTkToplevel):
    def __init__(self, parent_app, val_initiale_ms):
        super().__init__(parent_app)
        
        self.app_principale = parent_app
        self.valeur_sec = int(val_initiale_ms / 1000)

        self.title("Timer")
        self.geometry("220x130") 
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTk"]["fg_color"])
        self.configure(fg_color=bg_color)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        btn_style = {"width": 35, "height": 35, "corner_radius": 8, "fg_color": "#3b3b3b"}
        
        self.btn_moins = ctk.CTkButton(self, text="<", command=self.action_diminuer, **btn_style)
        self.btn_moins.grid(row=0, column=0, padx=10, pady=10)

        self.entry_valeur = ctk.CTkEntry(self, width=60, height=35, font=("Arial", 18, "bold"), justify="center")
        self.entry_valeur.insert(0, str(self.valeur_sec))
        self.entry_valeur.grid(row=0, column=1)

        self.btn_plus = ctk.CTkButton(self, text=">", command=self.action_augmenter, **btn_style)
        self.btn_plus.grid(row=0, column=2, padx=10, pady=10)

        self.btn_ok = ctk.CTkButton(self, text="OK", command=self.destroy, fg_color="#2fa572", hover_color="#106a43")
        self.btn_ok.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 15), sticky="ew")

    def _mettre_a_jour(self):
        if self.valeur_sec < 1: self.valeur_sec = 1
        self.entry_valeur.delete(0, "end")
        self.entry_valeur.insert(0, str(self.valeur_sec))
        self.app_principale.action_changer_timer(self.valeur_sec * 1000)

    def action_augmenter(self):
        self.valeur_sec += 1
        self._mettre_a_jour()

    def action_diminuer(self):
        self.valeur_sec -= 1
        self._mettre_a_jour()
