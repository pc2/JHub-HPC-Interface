# JupyterHub-Server Deployment mit Ansible

Folgende Installationen und Konfigurationen werden automatisiert vorgenommen:

- Installation von JupyterHub
- Installation des Batchspawners
- Installation benötigter Tools (Git etc.)
- Mapping der HPC-Knotennamen
- Kopieren der Konfigurationsdateien
- JupyterHub-Neustart

## Voraussetzungen

- Ansible auf dem Kontrollknoten installiert (siehe unten)
- Benutzer `ansiblebot` mit root-Rechten auf dem JupyterHub-Server vorhanden
- passwortloser SSH-Zugriff als `ansiblebot` auf den JupyterHub-Server möglich

## Installation von Ansible

Die [Installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) von Ansible auf dem Kontrollknoten erfolgt so:

```bash
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

Auf dem JupyterHub-Server selbst ist keine Ansible-Installation nötig.

## Durchführen der Konfiguration

Zuerst muss der JupyterHub-Server in `/etc/ansible/hosts` eingetragen werden, damit er von Ansible erreicht werden kann. Dort wird die IP und ggf. eine vom Standard abweichende SSH-Portnummer eingetragen:

```
# JupyterHub Server:
[jupyterhub_server]
1.2.3.4                   # IP
#1.2.3.4 ansible_port=123 # alternativ mit abweichendem SSH-Port
```

Dann wird das Ansible-Playbook ausgeführt:

```bash
ansible-playbook --ask-become-pass ./jupyterhub-deployment.yml
```

<!--
Test:
ssh -t ansiblebot@127.0.0.1 -p 2222 "$(< ./install_jupyterhub.sh)"
ssh -t ansiblebot@127.0.0.1 -p 2222 "$(< ./install_batchspawner.sh)"
ssh -t ansiblebot@127.0.0.1 -p 2222 "$(< ./hpc-nodenames-mapping.sh)"
-->
