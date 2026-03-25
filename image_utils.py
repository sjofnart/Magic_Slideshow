import os
import random
from PIL import Image

def recuperer_liste_images(dossier):
    """Retourne la liste des noms de fichiers images valides."""
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
    if not os.path.exists(dossier):
        return []
    return [f for f in os.listdir(dossier) if f.lower().endswith(exts)]

def charger_image_pil(chemin):
    """Charge une image et la prépare pour le slideshow."""
    try:
        with Image.open(chemin) as img:
            img_ready = img.convert("RGB")
            img_ready.load()
            return img_ready
    except Exception as e:
        print(f"Erreur lors du chargement de {chemin}: {e}")
        return None

def calculer_dimensions_ratio(img_size, container_size):
    """Calcule la nouvelle taille de l'image en respectant le ratio."""
    img_w, img_h = img_size
    cont_w, cont_h = max(container_size[0], 100), max(container_size[1], 100)
    
    ratio = min(cont_w / img_w, cont_h / img_h)
    return (int(img_w * ratio), int(img_h * ratio))
