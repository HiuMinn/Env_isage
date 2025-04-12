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
from PIL import Image
import time
from autoencodeur.dataset_filtering import filtered_sets

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