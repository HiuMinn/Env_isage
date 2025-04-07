import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torch.nn.functional as F
import torchvision.utils as vutils
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.amp import GradScaler, autocast
import os
import random
import matplotlib.pyplot as plt
from PIL import Image
from tqdm.notebook import trange, tqdm
import time
from dataset_filtering import filtered_sets

root = "D:/Datasets/" # Path to the celebA directory

# Update the train, validation, and test datasets to include only filtered images without using Datasets.CelebA from Torchvision
class CustomCelebADataset(Dataset):
    def __init__(self, root, split, transform, filtered_images):
        self.root = root
        self.split = split
        self.transform = transform
        self.filtered_images = filtered_images
        self.image_dir = os.path.join(root, 'celeba', 'img_align_celeba')
        self.image_paths = [os.path.join(self.image_dir, img) for img in filtered_images]
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, index):
        img_path = self.image_paths[index]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image
    
def vae_loss(recon, x, mu, logvar):

    recon = recon.to(x.device)  # Ensure recon is on the same device as x
    mu = mu.to(x.device)  # Ensure mu is on the same device as x
    logvar = logvar.to(x.device)  # Ensure logvar is on the same device as x

    recon_loss = F.mse_loss(recon, x)
    
    # Here is our KL divergance loss implemented in code
    # We will use the mean across the dimensions instead of the sum (which is common and would require different scaling)
    kl_loss = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp()).mean()
    
    # We'll tune the "strength" of KL divergance loss to get a good result 
    loss = recon_loss + 0.1 * kl_loss
    return loss

# DownBlock for the Encoder
class DownBlock(nn.Module):
    def __init__(self, channels_in, channels_out):
        super(DownBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels_in, channels_out, 3, 2, 1)
        self.bn1 = nn.BatchNorm2d(channels_out)
        
        self.conv2 = nn.Conv2d(channels_out, channels_out, 3, 1, 1)
        self.bn2 = nn.BatchNorm2d(channels_out)
        
        self.conv3 = nn.Conv2d(channels_in, channels_out, 3, 2, 1)

    def forward(self, x):
        x_skip = self.conv3(x)
        
        x = F.elu(self.bn1(self.conv1(x)))
        x = self.conv2(x) + x_skip
        
        return F.elu(self.bn2(x))
    
# UpBlock for the Decoder
class UpBlock(nn.Module):
    def __init__(self, channels_in, channels_out):
        super(UpBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(channels_in)

        self.conv1 = nn.Conv2d(channels_in, channels_in, 3, 1, 1)
        self.bn2 = nn.BatchNorm2d(channels_in)

        self.conv2 = nn.Conv2d(channels_in, channels_out, 3, 1, 1)
        
        self.conv3 = nn.Conv2d(channels_in, channels_out, 3, 1, 1)
        self.up_nn = nn.Upsample(scale_factor=2, mode="nearest")

    def forward(self, x_in):
        x = F.elu(self.bn2(x_in))
        
        x_skip = self.up_nn(self.conv3(x))
        
        x = self.up_nn(F.elu(self.bn2(self.conv1(x))))
        return self.conv2(x) + x_skip

# Encoder
class Encoder(nn.Module):
    def __init__(self, channels, ch=32, z=256):
        super(Encoder, self).__init__()
        self.conv_1 = nn.Conv2d(channels, ch, 3, 1, 1)

        self.conv_block1 = DownBlock(ch, ch)
        self.conv_block2 = DownBlock(ch, ch * 2)
        self.conv_block3 = DownBlock(ch * 2, ch * 4)

        self.conv_mu = nn.Conv2d(4 * ch, z, 4, 1)
        self.conv_logvar = nn.Conv2d(4 * ch, z, 4, 1)

    def sample(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def forward(self, x):
        x = F.elu(self.conv_1(x))
        
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)

        mu = self.conv_mu(x)
        logvar = self.conv_logvar(x)
        x = self.sample(mu, logvar)
        
        return x, mu, logvar

# Decoder
class Decoder(nn.Module):
    def __init__(self, channels, ch=32, z=256):
        super(Decoder, self).__init__()
        
        self.conv1 = nn.ConvTranspose2d(z, 4 * ch, 4, 1)
        
        self.conv_block1 = UpBlock(4 * ch, 2 * ch)
        self.conv_block2 = UpBlock(2 * ch, ch)
        self.conv_block3 = UpBlock(ch, ch)
        self.conv_out = nn.Conv2d(ch, channels, 3, 1, 1)
        self.upsample = nn.Upsample(size=(218, 178), mode='bilinear', align_corners=True)

    def forward(self, x):
        x = self.conv1(x)
        
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = F.elu(self.conv_block3(x))
        
        x = self.conv_out(x)
        x = self.upsample(x)  # Adjust the size to match the input dimensions

        return torch.tanh(x)

# VAE combining Encoder and Decoder
class VAE(nn.Module):
    def __init__(self, channels, ch=32, z=256):
        super(VAE, self).__init__()
        self.encoder = Encoder(channels, ch, z)
        self.decoder = Decoder(channels, ch, z)

    def forward(self, x):
        # Encode
        z, mu, logvar = self.encoder(x)
        
        # Decode
        x_recon = self.decoder(z)
        
        return x_recon, mu, logvar

if __name__ == "__main__":

    load_checkpoint = False # Load checkpoint if it exists

    batch_size = 64 # Batch size for training
    lr = 1e-4  # Learning rate
    nepoch = 500 # Number of Training epochs
    latent_size = 128 # The size of the Latent Vector

    # Define the transform to convert images to tensors and normalize them
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    use_cuda = torch.cuda.is_available()
    gpu_indx  = 0
    device = torch.device(gpu_indx if use_cuda else "cpu")

    train_images, val_images, test_images = filtered_sets(subset_size=1000) # For testing purposes, we can use a smaller subset of the dataset

    # Check the number of images in each set
    print(f"Number of training images: {len(train_images)}")
    print(f"Number of validation images: {len(val_images)}")
    print(f"Number of testing images: {len(test_images)}")

    # Create our network
    vae_net = VAE(channels=3, z=latent_size).to(device)

    # Setup optimizer
    optimizer = optim.Adam(vae_net.parameters(), lr=lr, betas=(0.5, 0.999))

    # Create loss logger
    loss_log = []
    train_loss = 0

    scaler = GradScaler('cuda')

    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)

    best_loss = float('inf')
    patience = 10  # Number of epochs with no improvement after which training will be stopped
    patience_counter = 0

    print("Using GPU" if use_cuda else "Using CPU")
    # Set the random seed for reproducibility
    random.seed(42)
    torch.manual_seed(42)
    if use_cuda:
        torch.cuda.manual_seed_all(42)

    train_set = CustomCelebADataset(root=root, split='train', transform=transform, filtered_images=train_images)
    val_set = CustomCelebADataset(root=root, split='val', transform=test_transform, filtered_images=val_images)
    test_set = CustomCelebADataset(root=root, split='test', transform=test_transform, filtered_images=test_images)

    # Update the data loaders
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

    # Get a test image
    dataiter = iter(test_loader)
    test_images = next(dataiter)[0]

    # View the shape
    print("Test images shape: ", test_images.shape)
    
    # Instantiate and test the VAE
    channels = 3  # Assuming the input images have 3 channels (RGB)
    vae_net = VAE(channels).to(device)

    # Add a batch dimension to the test image
    test_images_batch = test_images.unsqueeze(0)

    recon_data, mu, logvar = vae_net(test_images_batch.to(device))
    print(f"Input shape: {test_images_batch.shape}")
    print(f"Reconstructed shape: {recon_data.shape}")

    # Pass through a test image to make sure everything is working
    recon_data, mu, logvar = vae_net(test_images_batch.to(device))

    # View the Latent vector shape
    print("Latent vector shape: ", mu.shape)

    # Load checkpoint if it exists
    checkpoint_path = r".\vae_checkpoint.pth"
    start_epoch = 0
    if os.path.exists(checkpoint_path) and load_checkpoint:
        checkpoint = torch.load(checkpoint_path)
        vae_net.load_state_dict(checkpoint["model_state"])
        optimizer.load_state_dict(checkpoint["optimizer_state"])
        scaler.load_state_dict(checkpoint["scaler_state"])
        scheduler.load_state_dict(checkpoint["scheduler_state"])
        loss_log = checkpoint["loss_log"]
        best_loss = checkpoint["best_loss"]
        patience_counter = checkpoint["patience_counter"]
        start_epoch = checkpoint["epoch"] + 1
        print(f"Checkpoint loaded. Resuming training from epoch {start_epoch}.")
    else:
        if load_checkpoint:
            print("Checkpoint not used. Starting training from scratch.")
        else :
            print("No checkpoint found. Starting training from scratch.")

    # Network training

    print("Training VAE...")
    total_start_time = time.time()  
    vae_net.train()
    train_loss = 0
    for epoch in range(start_epoch, nepoch):
        last_save_time = time.time()
        epoch_start_time = time.time()
        train_loss = 0
        for i, data in enumerate(train_loader):
            batch_start_time = time.time()

            image = data.to(device, non_blocking=True)

            # Forward pass with mixed precision
            with autocast(device_type="cuda"):  # Spécifiez le type de périphérique
                recon_data, mu, logvar = vae_net(image)
                loss = vae_loss(recon_data, image, mu, logvar)

            if not torch.isfinite(loss):
                print("Loss is NaN or Inf!")
            
            # Log the loss
            loss_log.append(loss.item())
            train_loss += loss.item()

            # Take a training step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


            """
            # Scale Gradients
            scaler.scale(loss).backward()
            
            # Update Optimizer
            scaler.step(optimizer)
            scaler.update()
            """

            # Mesurer la durée du batch
            batch_duration = time.time() - batch_start_time
            print(f"Batch {i + 1}/{len(train_loader)} duration: {batch_duration:.2f} seconds")
        
        # Sauvegarder tous les 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"Saving models at epoch {epoch + 1}...")
            torch.save(vae_net.encoder.state_dict(), f"encoder_epoch_{epoch + 1}.pth")
            torch.save(vae_net.decoder.state_dict(), f"decoder_epoch_{epoch + 1}.pth")
            torch.save(vae_net.state_dict(), f"vae_model_epoch_{epoch + 1}.pth")
            print(f"Models saved for epoch {epoch + 1}.")

        print("Saving checkpoint...")
        checkpoint = {
            "epoch": epoch,
            "model_state": vae_net.state_dict(),
            "optimizer_state": optimizer.state_dict(),
            "scaler_state": scaler.state_dict(),
            "scheduler_state": scheduler.state_dict(),
            "loss_log": loss_log,
            "best_loss": best_loss,
            "patience_counter": patience_counter,
            "hyperparams": {
                "batch_size": batch_size,
                "lr": lr,
                "latent_size": latent_size
            },
            "train_images": train_images,
            "val_images": val_images,
            "test_images": test_images
        }
        
        # Sauvegarde du modèle
        torch.save(checkpoint, "vae_checkpoint.pth")
        print("Checkpoint saved.")

        # Mesurer la durée de l'époque
        epoch_duration = time.time() - epoch_start_time
        print(f"Epoch {epoch + 1} duration: {epoch_duration:.2f} seconds")

        # Step the scheduler
        scheduler.step(train_loss / len(train_loader))
        print(f"Epoch {epoch + 1}, Loss: {train_loss / len(train_loader):.4f}")

        if train_loss < best_loss:
            best_loss = train_loss
            patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= patience:
            print("Early stopping triggered!")
            break
    
    total_duration = time.time() - total_start_time
    print(f"Total training duration: {total_duration:.2f} seconds")

    print(f"Final Loss: {train_loss/len(train_loader)}")
    print("Training complete!")

    vae_net.eval()
    val_loss = 0
    with torch.no_grad():
        for i, data in enumerate(val_loader):
            recon_data, mu, logvar = vae_net(data.to(device))
            val_loss += vae_loss(recon_data, data, mu, logvar).item()
    print(f"Validation Loss: {val_loss / len(val_loader)}")

    test_images_batch = test_images.unsqueeze(0)  # Add a batch dimension
    recon_data, mu, logvar = vae_net(test_images_batch.to(device))

    # Sauvegarder l'encodeur
    torch.save(vae_net.encoder.state_dict(), "encoder.pth")

    # Sauvegarder le décodeur
    torch.save(vae_net.decoder.state_dict(), "decoder.pth")

    # Sauvegarder le modèle complet
    torch.save(vae_net.state_dict(), "vae_model.pth")

