import customtkinter as ctk
from PIL import Image
import os
import random
import gc

# Nos imports personnalisés (assure-toi que les fichiers existent)
from components import PopupConfigTimer
import image_utils 

class VisionneuseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Slideshow Fluide")
        self.geometry("1000x800")
        ctk.set_appearance_mode("dark")

        self.dossier_source = ""
        self.liste_images = []
        self.pile_images = []
        self.image_pil_actuelle = None
        self.image_ctk_affichage = None
        self.is_slideshow_on = False
        self.intervalle_ms = 3000
        self.timer_id = None       
        self.resize_timer_id = None
        self.popup_timer = None 

        self._setup_ui()
        self._bind_shortcuts()

    def _setup_ui(self):
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTk"]["fg_color"])

        # Container d'image
        self.image_container = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=0)
        self.image_container.pack(expand=True, fill="both")

        self.label_image = ctk.CTkLabel(self.image_container, text="📁 Ouvrez un dossier", text_color="gray")
        self.label_image.place(relx=0.5, rely=0.5, anchor="center")

        # Frame de contrôle
        self.frame_controle = ctk.CTkFrame(self, fg_color=bg_color, height=80, corner_radius=0)
        self.frame_controle.pack(fill="x", side="bottom", pady=10)

        self.btn_ouvrir = ctk.CTkButton(self.frame_controle, text="📁 Dossier", command=self.action_choisir_dossier)
        self.btn_ouvrir.pack(side="left", padx=20)

        self.btn_slideshow = ctk.CTkButton(
            self.frame_controle, text="▶ Démarrer Slideshow", command=self.toggle_slideshow,
            fg_color="#2fa572", state="disabled"
        )
        self.btn_slideshow.pack(side="right", padx=20)
        
        self.btn_slideshow.bind("<Button-3>", self.ouvrir_popup_config)

    def _bind_shortcuts(self):
        self.bind("<Configure>", self._on_resize)
        self.bind("<F11>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<space>", lambda e: self.toggle_slideshow() if self.liste_images else None)

    def action_choisir_dossier(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.dossier_source = path
            self.liste_images = image_utils.recuperer_liste_images(path)
            
            if self.liste_images:
                self.pile_images = []
                self.btn_slideshow.configure(state="normal")
                self.action_image_aleatoire()

    def action_image_aleatoire(self):
        if not self.liste_images: return

        if not self.pile_images:
            self.pile_images = self.liste_images.copy()
            random.shuffle(self.pile_images)
        
        nom = self.pile_images.pop()
        chemin = os.path.join(self.dossier_source, nom)

        img = image_utils.charger_image_pil(chemin)
        if img:
            self.image_pil_actuelle = img
            self._rafraichir_affichage()
            self.title(f"Slideshow - {nom} ({int(self.intervalle_ms/1000)}s)")
            gc.collect() 
        else:
            self.action_image_aleatoire()

    def toggle_slideshow(self):
        self.is_slideshow_on = not self.is_slideshow_on
        if self.is_slideshow_on:
            self.btn_slideshow.configure(text="Stop Slideshow", fg_color="#ae3a3a")
            self.boucle_slideshow()
        else:
            self.btn_slideshow.configure(text="▶ Démarrer Slideshow", fg_color="#2fa572")
            if self.timer_id: self.after_cancel(self.timer_id)

    def boucle_slideshow(self):
        if self.is_slideshow_on:
            self.action_image_aleatoire()
            self.timer_id = self.after(self.intervalle_ms, self.boucle_slideshow)

    def action_changer_timer(self, nouvelle_val_ms):
        self.intervalle_ms = nouvelle_val_ms
        if self.is_slideshow_on:
            if self.timer_id: self.after_cancel(self.timer_id)
            self.boucle_slideshow() 

    def ouvrir_popup_config(self, event):
        if self.popup_timer is None or not self.popup_timer.winfo_exists():
            self.popup_timer = PopupConfigTimer(self, self.intervalle_ms)
        else:
            self.popup_timer.focus()

    def _on_resize(self, event):
        if event.widget == self and self.image_pil_actuelle:
            if self.resize_timer_id:
                self.after_cancel(self.resize_timer_id)
            self.resize_timer_id = self.after(100, self._rafraichir_affichage)

    def _rafraichir_affichage(self):
        if not self.image_pil_actuelle: return
        
        taille = image_utils.calculer_dimensions_ratio(
            self.image_pil_actuelle.size, 
            (self.image_container.winfo_width(), self.image_container.winfo_height())
        )

        self.image_ctk_affichage = ctk.CTkImage(light_image=self.image_pil_actuelle, 
                                               dark_image=self.image_pil_actuelle, 
                                               size=taille)

        self.label_image.configure(image=self.image_ctk_affichage, text="")

# LE BLOC DE LANCEMENT (Crucial pour que ça démarre)
if __name__ == "__main__":
    app = VisionneuseApp()
    app.mainloop()
