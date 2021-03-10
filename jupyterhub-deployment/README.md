# JupyterHub Deployment with Ansible

The following installations and configurations are performed automatically:

- installation of [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/installation-guide-hard.html)
- installation of [BatchSpawner](https://github.com/jupyterhub/batchspawner)
- installation of [WrapSpawner](https://github.com/jupyterhub/wrapspawner)
- installation of required tools (Git etc.)
- copying the configuration file `jupyterhub_config.py` (you will most likely have to edit this file afterwards to make it fit your needs!)
- JupyterHub restart

(Testet on Ubuntu 18.04)

## Requirements

- clone this repo to your local machine
- Ansible installed on your **local** machine (see below)
- user `ansiblebot` with root privileges exists on the JupyterHub server
- **passwordless** SSH access as `ansiblebot` possible from your local machine to the JupyterHub server

Instead of `ansiblebot` you can use any other user that meets the above requirements. This user must be registered in `jupyterhub-deployment.yml`.

## Ansible installation

The [installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) of Ansible on your **local** machine is done as follows:

```bash
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

No Ansible installation is required on the JupyterHub server itself.

## Running the playbook

First, the JupyterHub server must be added to `/etc/ansible/hosts` on your local machine so that it can be reached by Ansible. The IP and, if necessary, a non-standard SSH port must be specified there:

```
# JupyterHub Server:
[jupyterhub_server]
1.2.3.4                   # JupyterHub server IP
#1.2.3.4 ansible_port=123 # alternatively with non-standard SSH port
```

Then the Ansible playbook is run from your local machine:

```bash
ansible-playbook --ask-become-pass ./jupyterhub-deployment.yml
```

A prompt will ask for a `BECOME password`. Enter `ansiblebot`s password there.
