import customtkinter as ctk
import gc
import os
import random

# Nos imports personnalisés
from components import PopupConfigTimer
import image_utils  # On importe nos outils

class VisionneuseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ... (Configuration initiale inchangée) ...
        self.title("Slideshow Fluide")
        self.geometry("1000x800")
        self.dossier_source = ""
        self.liste_images = []
        self.pile_images = []
        self.image_pil_actuelle = None
        self.is_slideshow_on = False
        self.intervalle_ms = 3000
        
        self._setup_ui()
        self._bind_shortcuts()

    # ... (_setup_ui et _bind_shortcuts restent identiques) ...

    def action_choisir_dossier(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.dossier_source = path
            # APPEL À UTILS
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
        
        # APPEL À UTILS
        img = image_utils.charger_image_pil(chemin)
        if img:
            self.image_pil_actuelle = img
            self._rafraichir_affichage()
            self.title(f"Slideshow - {nom} ({int(self.intervalle_ms/1000)}s)")
            gc.collect()
        else:
            self.action_image_aleatoire()

    def _rafraichir_affichage(self):
        if not self.image_pil_actuelle: return
        
        # APPEL À UTILS pour le calcul de taille
        taille = image_utils.calculer_dimensions_ratio(
            self.image_pil_actuelle.size, 
            (self.image_container.winfo_width(), self.image_container.winfo_height())
        )

        self.image_ctk_affichage = ctk.CTkImage(
            light_image=self.image_pil_actuelle, 
            dark_image=self.image_pil_actuelle, 
            size=taille
        )
        self.label_image.configure(image=self.image_ctk_affichage, text="")

    # ... (reste des méthodes : toggle_slideshow, etc.) ...
