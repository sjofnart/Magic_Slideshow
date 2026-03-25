import customtkinter as ctk
from PIL import Image
import os
import random

class VisionneuseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuration de la fenêtre ---
        self.title("Ma Visionneuse Aléatoire")
        self.geometry("950x750") # Fenêtre un peu plus grande
        ctk.set_appearance_mode("dark")

        # --- Variables d'état ---
        self.dossier_source = ""
        self.liste_images = []
        
        # Zone d'affichage maximale pour l'image (pour les calculs)
        self.ZONE_IMAGE_WIDTH = 900
        self.ZONE_IMAGE_HEIGHT = 600

        # --- Interface Graphique (UI) ---
        
        # Conteneur principal pour centrer l'image proprement
        self.image_container = ctk.CTkFrame(self, fg_color="transparent")
        self.image_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Label d'image (placé dans le conteneur)
        self.label_image = ctk.CTkLabel(self.image_container, text="📁 Choisissez un dossier pour commencer", text_color="gray")
        self.label_image.place(relx=0.5, rely=0.5, anchor="center") # Centrage parfait

        # Barre de contrôle (bas)
        self.frame_controle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controle.pack(pady=20)

        self.btn_ouvrir = ctk.CTkButton(self.frame_controle, text="📁 Dossier", 
                                       command=self.selectionner_dossier, corner_radius=20)
        self.btn_ouvrir.grid(row=0, column=0, padx=10)

        self.btn_suivant = ctk.CTkButton(self.frame_controle, text="🎲 Aléatoire", 
                                        command=self.afficher_image_aleatoire, state="disabled", corner_radius=20)
        self.btn_suivant.grid(row=0, column=1, padx=10)

    def selectionner_dossier(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.dossier_source = path
            extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
            self.liste_images = [f for f in os.listdir(path) if f.lower().endswith(extensions)]
            
            if self.liste_images:
                self.btn_suivant.configure(state="normal")
                self.afficher_image_aleatoire()
            else:
                self.label_image.configure(image=None, text="Aucune image trouvée ici.")

    # --- La fonction clé pour l'Aspect Ratio ---
    def calculer_taille_affichage(self, img_pil):
        """Calcule la taille optimale de l'image en respectant son aspect ratio."""
        orig_w, orig_h = img_pil.size
        
        # Calcul du ratio de l'image
        ratio = orig_w / orig_h
        
        # Tentative : ajuster à la largeur max
        new_w = self.ZONE_IMAGE_WIDTH
        new_h = int(new_w / ratio)
        
        # Si la hauteur dépasse la zone max, on ajuste à la hauteur max
        if new_h > self.ZONE_IMAGE_HEIGHT:
            new_h = self.ZONE_IMAGE_HEIGHT
            new_w = int(new_h * ratio)
            
        return (new_w, new_h)

    def afficher_image_aleatoire(self):
        if not self.liste_images:
            return

        image_nom = random.choice(self.liste_images)
        chemin_complet = os.path.join(self.dossier_source, image_nom)

        # 1. Ouvrir l'image originale avec PIL
        img_pil = Image.open(chemin_complet)
        
        # 2. Calculer la nouvelle taille respectant le ratio
        taille_affichage = self.calculer_taille_affichage(img_pil)
        
        # 3. Créer l'objet CTkImage avec la taille calculée
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=taille_affichage)
        
        # 4. Mise à jour de l'UI
        self.label_image.configure(image=img_ctk, text="")
        self.title(f"Visionneuse - {image_nom}")

if __name__ == "__main__":
    app = VisionneuseApp()
    app.mainloop()
