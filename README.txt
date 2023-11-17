-#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#-
/\/\/\/\/\/\/\/\/\/\/\                      /\/\/\/\/\/\/\/\/\/\/\
\/\/\/\/\/\/\/\/\/\/\/ Imaging Instructions \/\/\/\/\/\/\/\/\/\/\/
/\/\/\/\/\/\/\/\/\/\/\                      /\/\/\/\/\/\/\/\/\/\/\
-#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#-

Instructions are annotated using hashes #
# = Standard Imaging Instructions (Fundamentals)
## = Custom Imaging Instructions (Optional)
### = Custom First-Boot Partition Resizer install (Optional)

-#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#-
!!!!!!                                                      !!!!!!
!!!!!!                      DISCLAIMER                      !!!!!!
!!!!!!                                                      !!!!!!
!!!!!! ALWAYS MAKE SURE YOU HAVE A BACKUP BEFORE PROCEEDING !!!!!!
!!!!!!   DATA CORRUPTION CAN HAPPEN BY ONE SIMPLE MISTAKE   !!!!!!
!!!!!!     I AM NOT LIABLE FOR CORRUPTION, DAMAGES, ETC     !!!!!!
!!!!!!               PROCEED AT YOUR OWN RISK               !!!!!!
!!!!!!                                                      !!!!!!
!!!!!!        ALL INSTRUCTIONS PROVIDED ARE EXAMPLES        !!!!!!
!!!!!!                                                      !!!!!!
!!!!!!        NOT ALL OS IMAGES ARE HANDLED THE SAME        !!!!!!
!!!!!!     THIS PROCESS WORKS FOR ME AND IS ONE OF MANY     !!!!!!
!!!!!!             WAYS IN WHICH IT CAN BE DONE             !!!!!!
!!!!!!                                                      !!!!!!
-#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#-

# Use GParted to shrink partitions (except shrink /boot/ or /part1/)
  - Take note of empty spaces before, between, and after partitions, their sizes, and partition formats
  - Keep in mind:
    - 1MB = 1,000,000 bytes
    - 1MiB = 1,048,576 bytes
    - bytes / 512 = sectors (1MiB = 2048 sectors)

# Create disc images of each partition (if=<input_partition>, of=<output_image>, bs=<block_size>)
  - `sudo dd if=/path/to/input/dev/sdx1 of=/path/to/output/partition1.img bs=4M status=progress`
  - `sudo dd if=/path/to/input/dev/sdx2 of=/path/to/output/partition2.img bs=4M status=progress`

# Create blank disc image file (count=<start_sector>, seek=<total_img_bytes>)
  - `sudo dd if=/dev/zero of=/path/to/empty/disc.img bs=1 count=0 seek=[Total Size in Bytes]`

# Use fdisk to write partitions to empty disc image
  - `fdisk /path/to/empty/disc.img`
    - `n` <new_partition>
    - `p` <primary_partition> /// l <logical_partition>
    - `1` <partition_number>
    - `8192` <first_sector> (4MiB empty)
    - `+647168` <last_sector> 

    - `n` <new_partition>
    - `p` <primary_partition> /// l <logical_partition>
    - `2` <partition_number>
    - `663552` <first_sector> (1st partition 4MiB empty + 1st partition last sector + 4MiB empty)
    - `+7340040` <last_sector>

    - `w` <write_changes>

# Attach target image file to Loop Device for setup
  - `sudo losetup -fP --show /path/to/empty/disc.img /dev/loop0`

# Use fdisk to properly format the partitions
  - `t` <change_partition_id>
  - `1` <partition_number>
  - `c` <partition_format> (W95 FAT32 LBA) /// b (W95 FAT32) /// 7 (HPFS/NTFS/exFAT) ///
        83 (Linux FileSystems) /// 82 (Linux Swap) /// l <full_list> (Lists Available Formats)
  - `w` <write_changes>

# Format FileSystems on partitions if necessary (mkfs.<filesystem-type> <options> /dev/<device>)
  - `sudo mkfs.vfat -F 32 /dev/loop0p1` (FAT32)
  - `sudo mkfs.ext4 /dev/loop0p2` (Ext4)
  - `sudo mkfs.ntfs /dev/loop0p3` (NTFS)
  - `sudo mkfs.exfat /dev/loop0p4` (exFAT)
  - `sudo mkswap /dev/loop0p5` (Linux Swap)
  - `sudo mkfs.btrfs /dev/loop0p6` (Btrfs)

# Copy partition images to Loop Device to combine them (Pay attention to the order and check formats after)
  - `sudo dd if=/path/to/partition1.img of=/dev/loop0p1 bs=4M status=progress`
  - `sudo dd if=/path/to/partition2.img of=/dev/loop0p2 bs=4M status=progress`

/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
##                                                                  ##
## The following instructions pertain to custom images and packages ##
##                                                                  ##
##         Skip to the final step to finish standard images         ##
##                                                                  ##
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

## Mount partitions to local system for editing
  - `sudo mkdir /mnt/part1/`
  - `sudo mkdir /mnt/part2/`
    - `sudo mount /dev/loop0p1 /mnt/part1`
    - `sudo mount /dev/loop0p2 /mnt/part2`

/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
###                                                                                                      ###
### The following instructions are for a Custom First-Boot Partition Resizer made for 2 partition setups ###
###   Resize.sh and its corresponding resize.service can be used without the resize_notification files   ###
###  Resize_notification files are added to provide a simple notification on OSMC custom image installs  ###
###  Check the repo for another version of resize_notification.py tailored for other custom OS installs  ###
###                                                                                                      ###
###          Instructions in this section can also be used for making changes to a custom image          ###
###                                                                                                      ###
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

### Make resize.sh and resize_notification.py executable
  - `sudo chmod +x ~/Imaging_Instructions/resize.sh`
  - `sudo cp ~/Imaging_instructions/resize_notification.py`

### Move resize.sh and resize_notification.py into part2 partition
  - `sudo cp ~/Imaging_Instructions/resize.sh /mnt/part2/home/<username>/`
  - `sudo cp ~/Imaging_Instructions/resize_notification.py /mnt/part2/home/<username>/`

### Move resize.service and resize_notification.service into part2 partition
  - `sudo cp ~/Imaging_instructions/resize.service /mnt/part2/etc/systemd/system/`
  - `sudo cp ~/Imaging_Instructions/resize_notification.service /mnt/part2/etc/systemd/system/`

### Mount system directories into the mounted part2 filesystem
  - `sudo mount --bind /dev /mnt/part2/dev`
  - `sudo mount --bind /dev/pts /mnt/part2/dev/pts`
  - `sudo mount -t proc /proc /mnt/part2/proc`
  - `sudo mount -t sysfs /sys /mnt/part2/sys`
  - `sudo mount -t tmpfs /run /mnt/part2/run`

### Chroot into the mounted image
  - `sudo chroot /mnt/part2`

### Add sudo powers for resize.sh script
  - `visudo`
    - "osmc ALL=(ALL) NOPASSWD: /sbin/resize2fs, /usr/bin/growpart, /bin/systemctl disable resize_root.service, /bin/rm /etc/systemd/system/resize_root.service, /sbin/reboot"

### Enable resize.service and resize_notification.service
  - `systemctl enable resize.service`
  - `systemctl enable resize_notification.service`

### Exit chroot
  - `exit`

### Unmount the system directories
  - `sudo umount /mnt/part2/run`
  - `sudo umount /mnt/part2/sys`
  - `sudo umount /mnt/part2/proc`
  - `sudo umount /mnt/part2/dev/pts`
  - `sudo umount /mnt/part2/dev`

/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
###                                                  ###
### End of Custom First-Boot Partition Resizer setup ###
###                                                  ###
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
    
## Unmount partitions
  - `sudo unmount /mnt/part1/`
  - `sudo unmount /mnt/part2/`

/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
##                                  ##
## End of custom image instructions ##
##                                  ##
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

# Unmount final disk image from Loop Device
  - `sudo losetup -d /dev/loop0`

# Write the final .img file
  - Use any capable imaging tool to write the final .img file to your desired device or location
    - There are many out there. The two tools I use most for this are Rufus (Windows) and GNOME Disks (Linux)

-#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#--#-#-#-#-#-
