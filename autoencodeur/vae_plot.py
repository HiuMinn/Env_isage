import matplotlib.pyplot as plt
import torch
import os
from torchvision import transforms
from PIL import Image

import dataset_filtering  # The dataset filtering code is in dataset_filtering.py
import vae  # The VAE model is defined in vae_model.py

# Charger les ensembles d'images
train_images, val_images, test_images = dataset_filtering.filtered_sets()

# Chemin vers le dossier contenant les images CelebA
celeba_folder = r"D:\Datasets\celeba\img_align_celeba"

# Construire le chemin complet de l'image
test_image_path = os.path.join(celeba_folder, test_images[0])

# Charger le modèle VAE pré-entraîné
vae_model_path = r"c:\Users\gauti\Documents\4A\S2\Projet4BIM\projet-4bim\autoencodeur\vae_model_epoch_30.pth" # Chemin sur ma machine
if not os.path.exists(vae_model_path):
    raise FileNotFoundError(f"Model file not found: {vae_model_path}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
vae = vae.VAE(channels=3).to(device)
vae.load_state_dict(torch.load(vae_model_path, map_location=device))
vae.eval()

# Transformation utilisée pour charger l'image
transform = transforms.Compose([
    transforms.Resize((218, 178)),  # Redimensionner à la taille utilisée lors de l'entraînement
    transforms.ToTensor(),         # Convertir en tenseur PyTorch
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalisation utilisée lors de l'entraînement
])

# Charger une image de test
test_image = Image.open(test_image_path).convert("RGB")  # Charger l'image et la convertir en RGB
test_image = transform(test_image).unsqueeze(0).to(device)  # Appliquer les transformations et ajouter une dimension batch

# Encoder et décoder l'image
with torch.no_grad():
    z, mu, logvar = vae.encoder(test_image)  # Récupérez z, mu, et logvar
    decoded = vae.decoder(z)  # Passez uniquement z au décodeur

# Afficher l'image originale et reconstruite
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].imshow(test_image.squeeze(0).permute(1, 2, 0).cpu().numpy() * 0.5 + 0.5)  # Dé-normaliser pour affichage
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(decoded.squeeze(0).permute(1, 2, 0).cpu().numpy() * 0.5 + 0.5)  # Dé-normaliser pour affichage
axes[1].set_title('Decoded Image')
axes[1].axis('off')

plt.tight_layout()
plt.show()