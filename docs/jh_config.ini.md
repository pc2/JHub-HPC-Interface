# Configuration file (jh_config.ini)

|          Option           |                                                                Description                                                                |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `jupyterhub_ip` | This IP will be used to start a SSH tunnel. It should be a reachable IP address of course |
| `jupyterhub_api_url` | The JupyterHub API URL - If you want to start a SSH tunnel, leave a local address |
| `log_file` | The file where the log information will be written. |
| `log_level` | Set the log level. If set to DEBUG the command `$cmd_run_job_debug` will be used to start a notebook server |
| `maintenance` | If set to True, no notebook server will be start, except for user `$maintenance_user` |
| `maintenance_user` | See above :-) |
| `cmd_run_job` | How to run a job with your workload manager |
| `cmd_run_job_debug` | How to run a job if debug mode is enabled |
| `cmd_kill_job` | How to kill a job  with your workload manager. Attention. '$JOBID' will be automatically replaced! |
| `cmd_job_state` | Job state of a running/planned/stopped job. Attention: '$JOBID' will be automatically replaced! |
| `cmd_job_get_exec_node` | Get the execution node from given $JOBID. Attention '$JOBID' will be automatically replaced! |
| `execnode_regex` | Filter the execution node from output of `$cmd_job_get_exec_node` using regular expressions |
| `ssh_tunnel_api` | If set to true, the API will be available localhost on the compute node on port `$ssh_tunnel_api_dst_port` |
| `ssh_tunnel_src_api_port` | The port where the API is listening on the JupyterHub Server | 
| `ssh_tunnel_dst_api_port` | The port where the API should be listen to | 
| `ssh_tunnel_user` | This user will be used to establish a SSH tunnel from the compute node to the JupyterHub server |
| `ssh_keypath` | Path of the private key to use to create a SSH tunnel. The public part of course should be written into ~`$ssh_tunnel_user`_/.ssh/authorized_keys_ |
| `use_singularity` | If set to true, `singularity` will be used and the notebook server starts in a container |
| `singularity_container_compute` | Path of the container which should be started on a regular compute node |
| `singularity_container_gpu` | Path of the container which should be started on a GPU node | 
| `singularity_extra_args` | Extra arguments that will be passed to the singularity call |
| `singularity_use_overlay` | If set to true, singularity will be started with `--overlay` |
| `singularity_overlay_c` | Options: `auto` or `spec` - auto: Automatically create a singularity overlay in `$singularity_overlay_location/USERNAME.img` - spec: Always use the specified overlay in `$singularity_overlay_location` |
| `singularity_overlay_size` | Only if `$singularity_overlay_c` is set to `auto`: The size of the new created overlay (MB) |
