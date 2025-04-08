import matplotlib.pyplot as plt
import torch
import os
from torchvision import transforms
from PIL import Image

import autoencodeur.dataset_filtering as datase_filtering  # The dataset filtering code is in dataset_filtering.py
import autoencodeur.vae as vae  # The VAE model is defined in vae_model.py

# Transformation utilisée pour charger l'image
transform = transforms.Compose([
    transforms.Resize((218, 178)),  # Redimensionner à la taille utilisée lors de l'entraînement
    transforms.ToTensor(),         # Convertir en tenseur PyTorch
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalisation utilisée lors de l'entraînement
])

def encode(image_path, model=r"./src/autoencodeur/vae_final.pth"):
    """
    Encodes the input vector using the VAE model.

    :param vector: Input vector to be encoded.
    :param model: VAE model used for encoding.
    :return: Encoded vector.
    """

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vae_net = vae.VAE(channels=3).to(device)
    vae_net.load_state_dict(torch.load(model, map_location=device))
    vae_net.eval()

    # Charger une image de test
    image = Image.open(image_path).convert("RGB")  # Charger l'image et la convertir en RGB
    image = transform(image).unsqueeze(0).to(device)  # Appliquer les transformations et ajouter une dimension batch

    # Encoder l'image
    with torch.no_grad():
        z, _, _ = vae_net.encoder(image)  # Récupérez z, mu, et logvar
    return z

def decode(z, model=r"./src/autoencodeur/vae_final.pth"):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vae_net = vae.VAE(channels=3).to(device)
    vae_net.load_state_dict(torch.load(model, map_location=device))
    vae_net.eval()

    # Decoder l'image
    with torch.no_grad():
        z = vae_net.decoder(z)

    return z

if __name__ == "__main__":

    # Charger les ensembles d'images
    train_images, val_images, test_images = dataset_filtering.filtered_sets()

    # Chemin vers le dossier contenant les images CelebA
    celeba_folder = r"D:\Datasets\celeba\img_align_celeba"

    # Construire le chemin complet de l'image
    test_image_path = os.path.join(celeba_folder, test_images[0])

    # Charger le modèle VAE pré-entraîné
    vae_model_path = "vae_final.pth" # Chemin sur ma machine
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

    print ("test_image",test_image.shape)

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