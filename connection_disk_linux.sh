#connection à un disque distant 
#sur linux 
sudo apt update
sudo apt install cifs-utils
sudo mkdir /mount_point
sudo mount -t cifs //LAPTOP-89DAVKBV/celeba_filtered /mount_point -o guest
