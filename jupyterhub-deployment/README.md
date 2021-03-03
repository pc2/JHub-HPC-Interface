# JupyterHub Deployment with Ansible

The following installations and configurations are performed automatically:

- installation of [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/installation-guide-hard.html)
- installation of [BatchSpawner](https://github.com/jupyterhub/batchspawner)
- installation of required tools (Git etc.)
- copying the configuration files
- JupyterHub restart

## Requirements

- Ansible installed on the control node (see below).
- user `ansiblebot` with root privileges exists on the JupyterHub server
- passwordless SSH access as `ansiblebot` to the JupyterHub server granted

## Ansible installation

The [installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) of Ansible on the control node is done as follows:

```bash
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

No Ansible installation is required on the JupyterHub server itself.

## Carrying out the deployment

First, the JupyterHub server must be added to `/etc/ansible/hosts` so that it can be reached by Ansible. The IP and, if necessary, a non-standard SSH port are specified there:

```
# JupyterHub Server:
[jupyterhub_server]
1.2.3.4                   # IP
#1.2.3.4 ansible_port=123 # alternatively with different SSH port
```

Then the Ansible playbook is run:

```bash
ansible-playbook --ask-become-pass ./jupyterhub-deployment.yml
```
