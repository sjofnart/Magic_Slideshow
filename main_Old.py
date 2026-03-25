import customtkinter as ctk
from PIL import Image, ImageEnhance
import os
import random
import gc

class TransitionManager:
    """Gère les effets visuels entre deux images."""
    @staticmethod
    def blend(img_old, img_new, alpha):
        """Mélange deux images selon un ratio alpha (0.0 à 1.0)."""
        # On s'assure que les deux images ont la même taille pour le mélange
        if img_old.size != img_new.size:
            img_old = img_old.resize(img_new.size, Image.Resampling.LANCZOS)
        return Image.blend(img_old, img_new, alpha)

class VisionneuseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Slideshow avec Transitions")
        self.geometry("1000x800")
        
        # État
        self.dossier_source = ""
        self.liste_images = []
        self.pile_images = []
        self.image_pil_precedente = None
        self.image_pil_actuelle = None
        self.is_slideshow_on = False
        self.intervalle_ms = 3000
        
        # Paramètres transition
        self.en_transition = False
        self.duree_transition_ms = 500  # Durée totale de l'effet
        self.pas_transition = 10         # Nombre d'étapes (plus c'est haut, plus c'est fluide)
        
        self._setup_ui()

    def _setup_ui(self):
        self.image_container = ctk.CTkFrame(self, fg_color="transparent")
        self.image_container.pack(expand=True, fill="both", padx=20, pady=20)

        self.label_image = ctk.CTkLabel(self.image_container, text="📁 Ouvrez un dossier", text_color="gray")
        self.label_image.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_ouvrir = ctk.CTkButton(self, text="📁 Dossier", command=self.action_choisir_dossier)
        self.btn_ouvrir.pack(side="left", padx=20, pady=20)

        self.btn_slideshow = ctk.CTkButton(self, text="▶ Démarrer", command=self.toggle_slideshow, state="disabled")
        self.btn_slideshow.pack(side="right", padx=20, pady=20)
        
        self.bind("<Configure>", self._on_resize)

    def action_choisir_dossier(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.dossier_source = path
            exts = ('.png', '.jpg', '.jpeg', '.webp')
            self.liste_images = [f for f in os.listdir(path) if f.lower().endswith(exts)]
            if self.liste_images:
                self.pile_images = []
                self.btn_slideshow.configure(state="normal")
                self.charger_nouvelle_image()

    def charger_nouvelle_image(self):
        """Prépare la nouvelle image et lance la transition."""
        if not self.liste_images or self.en_transition: return

        if not self.pile_images:
            self.pile_images = self.liste_images.copy()
            random.shuffle(self.pile_images)
        
        nom = self.pile_images.pop()
        
        # On garde l'ancienne pour la transition
        if self.image_pil_actuelle:
            self.image_pil_precedente = self.image_pil_actuelle.copy()

        try:
            with Image.open(os.path.join(self.dossier_source, nom)) as img:
                # On redimensionne tout de suite à la taille du conteneur pour optimiser le blend
                w, h = self._get_container_dims()
                self.image_pil_actuelle = self._resize_proportional(img, w, h)
            
            if self.image_pil_precedente:
                self.lancer_transition_fondu(0)
            else:
                self._afficher_image(self.image_pil_actuelle)
                
            gc.collect()
        except:
            self.charger_nouvelle_image()

    def lancer_transition_fondu(self, step):
        """Effet de fondu récursif."""
        self.en_transition = True
        alpha = step / self.pas_transition
        
        if alpha <= 1.0:
            # Création de l'image intermédiaire
            blended = TransitionManager.blend(self.image_pil_precedente, self.image_pil_actuelle, alpha)
            self._afficher_image(blended)
            
            # Calcul du prochain pas
            delay = self.duree_transition_ms // self.pas_transition
            self.after(delay, lambda: self.lancer_transition_fondu(step + 1))
        else:
            self.en_transition = False
            self._afficher_image(self.image_pil_actuelle)
            # On nettoie l'ancienne image
            if self.image_pil_precedente:
                self.image_pil_precedente.close()
                self.image_pil_precedente = None

    def _afficher_image(self, pil_img):
        img_ctk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
        self.label_image.configure(image=img_ctk, text="")

    def _get_container_dims(self):
        w = max(self.image_container.winfo_width() - 40, 100)
        h = max(self.image_container.winfo_height() - 40, 100)
        return w, h

    def _resize_proportional(self, img, max_w, max_h):
        img_w, img_h = img.size
        ratio = min(max_w/img_w, max_h/img_h)
        return img.resize((int(img_w*ratio), int(img_h*ratio)), Image.Resampling.LANCZOS)

    def toggle_slideshow(self):
        self.is_slideshow_on = not self.is_slideshow_on
        if self.is_slideshow_on:
            self.btn_slideshow.configure(text="Stop", fg_color="#ae3a3a")
            self.boucle_slideshow()
        else:
            self.btn_slideshow.configure(text="▶ Démarrer", fg_color="#2fa572")

    def boucle_slideshow(self):
        if self.is_slideshow_on:
            self.charger_nouvelle_image()
            # On attend l'intervalle + la durée de la transition pour ne pas chevaucher
            total_delay = self.intervalle_ms + self.duree_transition_ms
            self.after(total_delay, self.boucle_slideshow)

    def _on_resize(self, event):
        if event.widget == self and self.image_pil_actuelle and not self.en_transition:
            w, h = self._get_container_dims()
            self.image_pil_actuelle = self._resize_proportional(self.image_pil_actuelle, w, h)
            self._afficher_image(self.image_pil_actuelle)

if __name__ == "__main__":
    app = VisionneuseApp()
    app.mainloop()
