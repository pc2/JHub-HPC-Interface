# JupyterHub + High-Performance Computing

*High performance Jupyter Notebooks*

The aim of this project is to connect JupyterHub to a high-performance computer (HPC). By automatically outsourcing the computations to the HPC system, even complex calculations are possible. While JupyterHub is deployed on a regular server, the notebooks themselves are spawned and run on the remote HPC system.

**Motivation**

The technical core of this project is the transparent integration of digital worksheets (Jupyter notebooks), in which learning content and programs can be displayed, edited and executed on the students' own laptops, with current cloud and high-performance computing (HPC) technologies. This provides the conditions for innovative, digital teaching that encourages independent and interactive development of, for example, data science applications, without imposing the complexity of using a high-performance computer system on the students. Instead, particularly computationally and data-intensive calculations are automatically offloaded to a high-performance computer, enabling even sophisticated analyses to be performed that would otherwise not be feasible on students' laptops.

---

## Table of Contents
- [JupyterHub + High-Performance Computing](#jupyterhub--high-performance-computing)
  - [Table of Contents](#table-of-contents)
  - [Installation JupyterHub Server](#installation-jupyterhub-server)
    - [Requirements](#requirements)
    - [Node mapping](#node-mapping)
  - [Installation HPC System](#installation-hpc-system)
    - [Requirements](#requirements-1)
    - [Clone Repository](#clone-repository)
    - [Singularity Container](#singularity-container)
      - [Build Singularity Container](#build-singularity-container)
    - [Configuration Wizard for Slurm](#configuration-wizard-for-slurm)
      - [Start the configuration wizard](#start-the-configuration-wizard)
    - [Configuration file (jh_config)](#configuration-file-jh_config)
  - [How It Works](#how-it-works)
    - [1. JupyterHub Login](#1-jupyterhub-login)
    - [2. The Spawner Class](#2-the-spawner-class)
    - [3. Wrapper Scripts](#3-wrapper-scripts)
    - [4. Procedure](#4-procedure)
  - [Examples](#examples)
  - [Shibboleth Integration](#shibboleth-integration)
  - [nbgrader Integration](#nbgrader-integration)
    - [Installation](#installation)
    - [Changing the Student ID to the JupyterHub logged in user name](#changing-the-student-id-to-the-jupyterhub-logged-in-user-name)
    - [Create nbgrader_config.py](#create-nbgrader_configpy)
  - [Using WebDAV](#using-webdav)
  - [Security Precautions](#security-precautions)
    - [Singularity Host Filesystems](#singularity-host-filesystems)
    - [JupyterHub API (https or SSH tunnel)](#jupyterhub-api-https-or-ssh-tunnel)
      - [https](#https)
      - [SSH Tunnel](#ssh-tunnel)
    - [tunnelbot User](#tunnelbot-user)
  - [Troubleshooting](#troubleshooting)

---

## TODO

* User Accounting Information on HPC-Side
* JupyterHub: Shibboleth Integration

## Installation JupyterHub Server

### Requirements

* JupyterHub
* batchspawner (https://github.com/jupyterhub/batchspawner)
* A user (called tunnelbot or whatever)
  * This user is responsible two start a SSH tunnel between the compute node and the JupyterHub server
  * A SSH Key Pair

1. See _examples/jupyterhub_config.py_ for more information

### Node mapping

The JupyterHub extracts the execution host name of the HPC system (e.g. cnode-003).
When a notebook server is started, an SSH tunnel is established using the notebook port. 

In order for JupyterHub to resolve the compute nodes hostname, the _/etc/hosts_ file must be edited.
An example entry might look like the following:

* `cnode-014 127.0.0.1`

---

## Installation HPC System

### Requirements

* __Singularity (> v.3.7.0)__
* An user who is allowed to allocate resources on the HPC system
  * A group with a directory (The user should be a member of this group)
  * This user should also have entered the public key of the tunnelbot user in the file _~/.ssh/authorized_keys_
* e2fsprogs with following option:
  * https://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git/commit/?id=217c0bdf17899c0f79b73f76feeadd6d55863180
* A directory to create a valid overlay for singularity

### Clone Repository

The best way is to copy the repository into the scratch directory of the user who is allowed to perform calculations.

```bash
git clone https://github.com/pc2/JHub-HPC-Interface.git
```

### Singularity Container

Singularity recipe examples are in the directory SINGULARITY/.

> INFO: If you do not want to use Singularity, just set `$use_singularity` in _jh_config_ to `false`.

#### Build Singularity Container

The following commands replace USER_ID in the recipes to the output of `id -u`, creates a new hidden file, and builds the singularity container with the new created file.
 
##### Compute

```bash
USER_ID=$(id -u) && sed "s/USER_ID/$USER_ID/" < SINGULARITY/Singularity > SINGULARITY/.recipefile_compute && singularity build --remote SINGULARITY/compute_jupyter.sif SINGULARITY/.recipefile_compute
```

##### GPU (Tensorflow)

```bash
USER_ID=$(id -u) && sed "s/USER_ID/$USER_ID/" < SINGULARITY/Singularity_Tensorflow > SINGULARITY/.recipefile_gpu && singularity build --remote SINGULARITY/gpu_jupyter.sif SINGULARITY/.recipefile_gpu
```

_singularity build help section_:
> __-r, --remote__            build image remotely (does not require root)

Please refer to the offical docs how to use the remote build featue: https://sylabs.io/docs/

### Configuration Wizard for Slurm

The configuration wizard is an interactive script to configure the HPC environment with JupyterHub.
The script creates a temporary configuration file at the end, which can be copied with a simple `cp`.

#### Start the configuration wizard

Just type following in your terminal:
```bash
./jh_slurm_wizard
```

If you are using another workload manager, you can configure _jh_config_ manually.

### Configuration file (jh_config)

|          Option           |                                                                Description                                                                |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `is_cluster_in_maintenance` | If true, the notebook servers will stop with an error message. |
| `scratch_dir` | Scratch directory were all wrapper scripts located | 
| `external_hub_url` | JupyterHub API URL - Default: __http://127.0.0.1:8083/hub/api__ |
| `cmd_run_job` | How to run a job with the Workload-Manager |
| `cmd_run_job_debug` | How to run a job in debug mode |
| `cmd_kill_job` | How to kill a job  with the Workload-Manager |
| `cmd_job_owner` | Extract the job **name** from a given Job ID (The name of a job will be set to the JH login name) |
| `cmd_job_batchfile` | Path of the executed batchfile |
| `cmd_job_state` | Job state of a running/planned/stopped job |
| `cmd_job_get_mapped_node` | Get the execution node from a given Job ID |
| `cluster_job_is_running/stopped/planned` | These values should be exact the same values from the `$cmd_job_state` output |
| `use_accounting` | WORK IN PROGRESS: Collect accounting information per user. If enabled, the scripts collects data about used resources to `$sqlite_database_file` |
| `sqlite_database_file` | WORK IN PROGRESS: The database file to use, if accounting (`use_accounting`) is enabled. |
| `ssh_tunnel_api` | If set to true, the API will be available localhost on the compute node on port `$ssh_tunnel_api_port` |
| `ssh_tunnel_api_port` | The port where the API will listen. - Default: 8083 | 
| `ssh_tunnel_user` | This user will be used to establish a SSH tunnel from the compute node to the JupyterHub server (and reverse) |
| `ssh_jh_ip` | The IP address of the JupyterHub server to establish the SSH tunnel |
| `ssh_priv_key` | The private key to use to create a SSH tunnel. The public part of course should be written into ~`$ssh_tunnel_user`_/.ssh/authorized_keys_ |
| `creating_user_homes` | If set to true, home directories in `$home_dir/` for users will be created. If false, no home directories will be created and all changes from users are temporary - Default: true |
| `home_dir` | Where all home directories should be placed? (Default: `$scratch_dir`_/HOME_DIRECTORIES/_) |
| `user_home_dir` | Will be expanded to: `$home_dir`_/$JUPYTERHUB_USER/_ |
| `user_log_directory` | Will be expanded to: `$user_home_dir`_/JupyterHub-Log/_ (This directory will be mount by singularity to _/notebooks/_, if used) |
| `use_singularity` | If set to true, `$cmd_load_singularity` will be executed and the notebook server will start in a container |
| `singularity_bind_fix` | fix binds at start time - e.g. for `jh_batchspawner_singleuser_replace` and `jh_starttunnel` |
| `singularity_bind_extra` | optional binds at start time - e.g. for an exchange directory to use nbgrader |
| `singularity_bind` | Merge `$singularity_bind_fix` and `$singularity_bind_extra` |
| `overlay_size` | Overlay size (MiB) to create a persistent storage for every user |
| `overlay_location` | Where should all created overlay be stored? Default: `$user_home_dir`_/overlay.img_ |
| `create_overlay_cmd` | Command to create an overlay. Default: `dd if=/dev/zero of=$overlay_location bs=1M count=$overlay_size` |
| `create_ext3_overlay_cmd` | Command to make the overlay as ext3 filesystem. |
| `container_to_start_compute` | Path of the container which should be started on a regular compute node |
| `container_to_start_gpu` | Path of the container which should be started on a GPU node | 
| `singularity_no_mount` | Comma-seperated list of which singularity should not mount when calling singularity (--no-mount) |
| `singularity_home_dir` |  $HOME-Directory inside the singularity container. (--home) |
| `singularity_extra_args` | Extra arguments that will be passed to the singularity call |
| `enable_debug_mode` | enable `$cmd_run_job_debug` and prints DEBUG logs in `$log_dir` | 
| `enable_logging` | If true, all wrapper scripts creates log information in regular files named `$logging_save_date_fmt` |
| `log_dir` | Path of the log directory - Default: `$scratch_dir`_/log/_ |
| `cmd_load_singularity` | How to load singularity? So that the `singularity` command is available |
| `enable_webdav` | If enabled,  _jh_start_singularity_environment_ mounts WebDAV on the host filesystem using `$webdav_command` and `$webdav_mount_dir` and extends the variable $SINGULARITY_BIND with `$webdav_mount_dir_container` |
| `webdav_command` | Command how to mount files/directories with the WebDAV Protocol |
| `webdav_mount_dir` | Destination mountpoint outside of the container - Default: `$user_home_dir`_/WebDAV-Share/_ |
| `webdav_mount_dir_container` | Destination mountpoint inside the container - Default: _/notebooks/WebDAV-Share/_ |
| `logging_save_date_fmt` | Creates log files in given format. Default: "+%d%m%Y". See `man date` |

---

## How It Works

### 1. JupyterHub Login

JupyterHub offers several authentication options. 
Example: GitHub, Google,...

See here for more information: 
https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html

If you want to use Shibboleth as authentication, then see here: [Shibboleth Integration](#shibboleth-integration)

###  2. The Spawner Class

The spawner requires the following functions/variables:

| Method/Variable | Description |
| ---------------- | ------------ |
| `batch_script` | The actual batch script that is executed on the compute node of the HPC system |
| `batch_submit_cmd` | The command for executing a batch job on the HPC system |
| `batch_query_cmd` | The command to query a status for a job. It also extracts the node hostname on which the job is running |
| `batch_cancel_cmd` | The command to stop a job on the HPC system |
| `state_exechost_re` | Extraction pattern (RegEx), which is used to allow the JupyterHub of the node hostname to extract from __batch_query_cmd__ |
| `state_pending_re` | Status when a job is still in the queue on the HPC system (RegEx) |
| `state_running_re` | Status when a job is running on the HPC system |
| `parse_job_id` | method specifying how to extract the workload manager's job request ID |

All this information is in the JupyterHub configuration file `jupyterhub_config.py` in the class `CustomHPCSpawner`.

### 3. Wrapper Scripts

On the HPC system, wrapper scripts are used to execute and stop the job (`batch_submit_cmd` & `batch_cancel_cmd`) so that other functions, such as creating a "home directory" on the HPC system, can be used.

### 4. Procedure

* The spawner starts a job using `batch_submit_cmd`. The batch script defined in `batch_script` will be sent to STDIN (standard input) of the specified command in `batch_submit_cmd`.
    * __*`jh_startjob`*__:

        1. reads from STDIN and writes the batch script `batch_script` into a temporarily created file and makes it executable.
        2. creates a home directory for the user (i.e. the one who logs in to the JupyterHub web interface) defined in `$user_home_dir` (If user is a new user)
        3. creates an overlay image with an ext3 filesystem, so that changes made by a user are stored permanently and individually for each user (If user is a new user).
        4. execute the job using the temporarily created batch script
        5. output of 'jh_startjob': The output of the alloc command should contain the job request id (See point 2 -> 'parse_job_id')

    * Temporary batch script (i.e. nothing other than __*`batch_script`*__ in the spawner class on the JupyterHub server):

        1. export the WebDAV data (If used)
        2. check whether the overlay has already been __successfully__ created
        3. call of 'jh_start_singularity_environment' with node type (GPU or compute node) as first argument $1

    * __*`jh_start_singularity_environment`*__:

        1. check if the first argument $1 contains __*gpu*__ or __*compute*__
        2. mount the WebDAV share to `$webdav_mount_dir_container`. (If used)
        3. unset exported variables in `batch_script` (If used)
        4. delete the batch job script created for the user
        5. Finally starting the singularity container (If used). __$HOME__ will be set to _/userhome/_.
           5.1. Singularity also mounts `jh_starttunnel` into _/opt/_ and `jh_batchspawner_singleuser_replace` to _/opt/batchspawner/batchspawner/singleuser.py_
            5.1.1 _/opt/batchspawner/_ is the install location for the batchspawner (See singularity recipes in _/examples/_)

    * __*`jh_batchspawner_singleuser_replace`*__ & __*`jh_starttunnel`*__
  
        1. `jh_batchspawner_singleuser_replace` (Meanwhile mounted to _/opt/batchspawner/batchspawner/singleuser.py_) exports the port of the notebook server to `$JUPYTER_PORT`
        2. `jh_batchspawner_singleuser_replace` starting `jh_starttunnel` (Meanwhile in the container mounted read-only in /opt/)
        3. `jh_starttunnel` starts a SSH tunnel with port `$JUPYTER_PORT` from the compute node to the JupyterHub-Server so the JupyterHub is able to reach the notebook server at *127.0.0.1:`$JUPYTER_PORT`*

    * __*`jh_killjob`*__:

        1. stopping the job

---

## Examples

You will find examples for the configuration files jh_config and jupyterhub_config.py in the directory _examples/_.

---

## Shibboleth Integration

**Work-In-Progress**

---

## nbgrader Integration

### Installation

Installation insturctions:
https://nbgrader.readthedocs.io/en/latest/configuration/jupyterhub_config.html

To create an exchange directory for every user, just create an empty directory in `$scratch_dir` and mount it into the container with `$singularity_bind_extra`.

### Changing the Student ID to the JupyterHub logged in user name

Since the containers run as user jovyan, the value from the `$JUPYTERHUB_USER` variable is automatically used.

See here for more information: 
https://jupyter.readthedocs.io/en/latest/community/content-community.html#what-is-a-jovyan

### Create nbgrader_config.py

See here: https://nbgrader.readthedocs.io/en/stable/configuration/nbgrader_config.html#use-case-3-nbgrader-and-jupyterhub

To make _nbgrader_config.py_ available in the container, just append the file in `$singularity_bind_extra`.

---

## Using WebDAV

> Example: https://github.com/jmesmon/wdfs

---

## Security Precautions

### Singularity Host Filesystems

In case you are using Singularity, the host filesystems may be automatically mounted into the container when you start a Singularity Container.

A possible cause is the option `mount hostfs` in _singularity.conf_

See here: https://sylabs.io/guides/3.5/admin-guide/configfiles.html#singularity-conf

### JupyterHub API (https or SSH tunnel)

#### https

See here for more information:
https://jupyterhub.readthedocs.io/en/stable/reference/websecurity.html

#### SSH Tunnel

To make the JupyterHub API available on the compute node, a reverse SSH tunnel can be started from the compute node. For this purpose a "tunnelbot" user with an SSH key is created.

Set `$ssh_tunnel_api` to true.

The variables `$ssh_jh_ip`, `$ssh_tunnel_user` and `$ssh_priv_key` are set in the configuration file _jh_config_.

After _jh_starttunnel_ and _jh_batchspawner_singleuser_replace_ have been mounted into the container, the tunnel is built and the API then listens on _**127.0.0.1:8083**_

**Why 8083 and not default 8081?**

Most HPC systems use Bright as their cluster management system.
Bright uses port 8081.

The port number can be changed with option `ssh_tunnel_api_port` in _jh_config_

### tunnelbot User

You can increase the security by deactivating shell access for this user.

Just type:

```bash
usermod -s /bin/false tunnelbot
```

---

## Troubleshooting
