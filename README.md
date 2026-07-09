# VM PXE Server Infrastructure Setup

This repository documents the automation and configuration files used to spin up a fully functioning Network Boot (PXE) Server inside an Ubuntu Virtual Machine environment. 

There are two primary deployments in this repository:
1. **Linux OS Deployment**
2. **Custom RAM OS Deployment**

---

## Virtualbox
<img width="1918" height="1008" alt="image" src="https://github.com/user-attachments/assets/8e97084b-a83b-409d-aa0c-0ed5a8b4ec2b" />

---

## 🚀 Infrastructure Topology

- **Host OS:** Windows 11 (Hypervisor Engine)
- **PXE Server VM:** Ubuntu Server 24.04 LTS
- **Network Interface:** Host-Only Adapter (`192.168.56.10`), NAT Adapter
- **Target Deployment:** Automated OS provisioning via HTTP/TFTP protocol matrix.

---

# 1) Linux OS Deployment (Client VM)
Automates the network installation of a full Linux operating system (e.g., Ubuntu Server/Desktop) onto target client Virtual Machines over the local network using PXE.

Automated Installation: Utilizes automated response files (autoinstall / cloud-init) to eliminate manual user input during the OS installation process.

Network Components: Combines DHCP (assigns IP addresses and PXE boot filenames), TFTP (delivers the initial syslinux/grub bootloader and Linux kernel), and HTTP/NFS (hosts the full OS installation ISO/squashfs image).

Use Case: Provisioning bare-metal VMs, scaling client infrastructure, or resetting virtual machines with a standardized, production-ready OS image.

---

## ⚙️ Service Configurations

### 1. Networking & Identity Management (`dnsmasq.conf`)
The central engine handling network addressing and bootfile handshakes. It binds to the host-only virtual network switch to safely isolate traffic from production routes.

### 2. Boot Menu Configuration (`pxelinux.cfg/default`)
The roadmap file dictating the initial bootstrap phase for bare-metal and virtual machine target environments. It provides the terminal menu interface and delivers operational boot parameters over the network.

### 3. Auto-Provisioning Framework (`autoinstall/`)
Leverages cloud-init standards to pass installation choices programmatically to testing targets.

---

## 🛠️ Deployment Steps

To replicate this environment on a fresh Ubuntu virtual machine instance, execute the baseline sync routines:

```bash
# Update systems and pull system prerequisites
sudo apt update && sudo apt install -y dnsmasq syslinux pxelinux apache2 openssh-server

# Configure the DHCP & TFTP Server
# Edit dnsmasq config file:
sudo nano /etc/dnsmasq.conf
# Restart dnsmasq:
sudo systemctl restart  dnsmasq

# Create TFTP Directory with Bootloaders
sudo mkdir -p /srv/tftp/pxelinux.cfg
sudo cp /usr/lib/PXELINUX/pxelinux.0 /srv/tftp/
sudo cp /usr/lib/syslinux/modules/bios/{ldlinux.c32,menu.c32,libutil.c32,libcom32.c32} /srv/tftp/
sudo nano /srv/tftp/pxelinux.cfg/default

# Mount the ISO image and copy 'vmlinuz' and 'initrd' files
sudo mkdir -p /var/www/html/ubuntu_iso
sudo mount /dev/sr0 /var/www/html/ubuntu_iso
sudo mkdir -p /srv/tftp/ubuntu
sudo cp /var/www/html/ubuntu_iso/casper/{vmlinuz,initrd} /srv/tftp/ubuntu/

# Create the raw ISO file image that your autoinstall engine needs over HTTP
sudo dd if=/dev/sr0 of=/var/www/html/ubuntu-server.iso bs=4M status=progress
sudo chmod 644 /var/www/html/ubuntu-server.iso

# 5. Deploy infrastructure layout profiles
sudo mkdir -p /var/www/html/autoinstall
sudo touch /var/www/html/autoinstall/meta-data
sudo touch /var/www/html/autoinstall/vendor-data
sudo nano /var/www/html/autoinstall/user-data

```

<img width="727" height="400" alt="image" src="https://github.com/user-attachments/assets/6f4e5173-ddc5-4805-a258-c4365f400f41" />
<img width="722" height="406" alt="image" src="https://github.com/user-attachments/assets/149ac9c8-46af-4ed5-bb92-ec55f2ee5c20" />
<img width="726" height="67" alt="image" src="https://github.com/user-attachments/assets/c9f7348a-0dbc-4c8d-8287-de576a86ca8f" />

---

# 2) Custom PXE RAM-OS (Client VM)
A lightweight, diskless Linux distribution built using BusyBox, cpio, and custom scripts. Designed to boot over the network via PXE/iPXE directly into RAM to perform rapid PCI hardware discovery (lspci) without relying on host disks.

       ┌──────────────────────────────┐
       │     1. Prepare RootFS        │
       │  (BusyBox, lspci, pci.ids)   │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ 2. Fix Relative Symlinks     │
       │   (/bin/sh -> busybox)       │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ 3. Resolve Shared Libraries  │
       │ (Copy missing .so files)    │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ 4. Verify via Local Chroot   │
       │ (sudo chroot rootfs /bin/sh) │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ 5. Compress into Initramfs   │
       │   (find | cpio | gzip)       │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │ 6. Deploy to TFTP/PXE Folder │
       │  (/tftpboot/ram_os/boot/...) │
       └──────────────────────────────┘

<img width="747" height="397" alt="image" src="https://github.com/user-attachments/assets/605d7826-d9b3-4c38-893f-a23ca0a4d9a5" />
<img width="723" height="402" alt="image" src="https://github.com/user-attachments/assets/1d5df80b-7996-48c0-bb8d-4f69aecbebd0" />

