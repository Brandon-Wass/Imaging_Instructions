#!/bin/bash

### Script to resize Root partition and FileSystem ###

# Find the root partition (assuming it's ext4)
ROOT_PART=$(findmnt / -o source -n)
DISK=$(echo $ROOT_PART | sed -r 's/(.*)(p[0-9]+)/\1/')
PART_NUM=$(echo $ROOT_PART | sed -r 's/.*p([0-9]+)/\1/')

# Function to check if partition resize is successful
check_partition_resize() {
    PART_SIZE=$(sudo fdisk -l $DISK | grep "^$ROOT_PART" | awk '{print $3-$2+1}')
    DISK_SIZE=$(sudo fdisk -l $DISK | grep "^Disk $DISK" | awk '{print $3}' | cut -d'.' -f1) # Convert to integer

    # Check if partition size is close to disk size (accounting for minor differences in units)
    if [ $(echo "$DISK_SIZE - $PART_SIZE < 1024" | bc) -eq 1 ]; then
        echo "Partition resized successfully."
        return 0
    else
        echo "Partition resize failed."
        return 1
    fi
}

# Resize the partition
sudo growpart $DISK $PART_NUM

# Check if partition resize was successful
if check_partition_resize; then
    # Resize the filesystem
    sudo resize2fs $ROOT_PART
else
    echo "Error resizing partition. Exiting."
    exit 1
fi

# Disable and remove the systemd service
sudo systemctl disable resize_root.service
sudo rm /etc/systemd/system/resize_root.service

# Revoke passwordless sudo for the specific rule by deleting the line
sudo sed -i '/^osmc ALL=(ALL) NOPASSWD: \/sbin\/resize2fs, \/usr\/bin\/growpart, \/bin\/systemctl disable resize_root.service, \/bin\/rm \/etc\/systemd\/system\/resize_root.service, \/sbin\/reboot/d' /etc/sudoers

# Delete this script
rm -- "$0"

# Reboot the system
sudo reboot
