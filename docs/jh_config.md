# Configuration file (jh_config)

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
| `enable_webdav` | If enabled,  _jh_start_notebook_environment_ mounts WebDAV on the host filesystem using `$webdav_command` and `$webdav_mount_dir` and extends the variable $SINGULARITY_BIND with `$webdav_mount_dir_container` |
| `webdav_command` | Command how to mount files/directories with the WebDAV Protocol |
| `webdav_mount_dir` | Destination mountpoint outside of the container - Default: `$user_home_dir`_/WebDAV-Share/_ |
| `webdav_mount_dir_container` | Destination mountpoint inside the container - Default: _/notebooks/WebDAV-Share/_ |
| `logging_save_date_fmt` | Creates log files in given format. Default: "+%d%m%Y". See `man date` |
