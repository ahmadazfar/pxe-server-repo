# VM PXE Server Infrastructure Setup

This repository documents the automation and configuration files used to spin up a fully functioning Network Boot (PXE) Server inside an Ubuntu Virtual Machine environment.

## 🚀 Infrastructure Topology

- **Host OS:** Windows 11 (Hypervisor Engine)
- **PXE Server VM:** Ubuntu Server 24.04 LTS
- **Network Interface:** Host-Only Adapter (`192.168.56.10`), NAT Adapter
- **Target Deployment:** Automated OS provisioning via HTTP/TFTP protocol matrix.

---

## 📂 Repository Layout

```text
├── dnsmasq.conf                # Unified DHCP & TFTP Engine configuration
├── autoinstall/                # Automated installation manifests
│   ├── user-data               # Cloud-init automated system configurations
│   ├── meta-data               # Instance tracking file (empty stub)
│   ├── vendor-data             # Vendor orchestration hooks
│   └── burnin.py               # Post-install system configuration testing script
└── packages/                   # Offline execution pre-cached dependencies
    ├── libaio1t64.deb          # Async I/O engine prerequisite
    └── stress-ng.deb           # System load and validation test-bed tool
```

---

## ⚙️ Service Configurations

### 1. Networking & Identity Management (`dnsmasq.conf`)
The central engine handling network addressing and bootfile handshakes. It binds to the host-only virtual network switch to safely isolate traffic from production routes.
- **DHCP Proxy Mode:** Listens to core discovery steps and injects option matrix values.
- **Root TFTP Assets Directory:** Active path targeted to serve initial system bootstrap footprints (`/src/`).

### 2. Auto-Provisioning Framework (`autoinstall/`)
Leverages cloud-init standards to pass installation choices programmatically to testing targets:
- **`user-data`**: Dictates root account details, block device partitions, network presets, and custom execution hooks to bypass standard visual menus.
- **`meta-data`**: Create empty file.
- **`vendor-data`**: Create empty file.
- **`packages/`**: Preserves isolated offline package binaries required on target environments immediately upon provisioning wrap-ups.

---

## 🛠️ Deployment Steps

To replicate this environment on a fresh Ubuntu virtual machine instance, execute the baseline sync routines:

```bash
# 1. Update systems and pull system prerequisites
sudo apt update && sudo apt install -y dnsmasq syslinux pxelinux apache2 openssh-server

# 2. Configure the DHCP & TFTP Server
# Edit dnsmasq config file:
sudo nano /etc/dnsmasq.conf
# Restart dnsmasq:
sudo systemctl restart  dnsmasq

# 3. Create TFTP Directory with Bootloaders
sudo mkdir -p /srv/tftp/pxelinux.cfg
sudo cp /usr/lib/PXELINUX/pxelinux.0 /srv/tftp/
sudo cp /usr/lib/syslinux/modules/bios/{ldlinux.c32,menu.c32,libutil.c32,libcom32.c32} /srv/tftp/
sudo nano /srv/tftp/pxelinux.cfg/default

# 4. Mount the ISO image and copy 'vmlinuz' and 'initrd' files
#Create the web directory and mount the CD-ROM drive properly
sudo mkdir -p /var/www/html/ubuntu_iso
sudo mount /dev/sr0 /var/www/html/ubuntu_iso

# Build the TFTP folder infrastructure and extract the network boot kernels
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
