# How It Works

## JupyterHub Login

JupyterHub offers several authentication options. 
Example: GitHub, Google,...

See here for more information: 
https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html

## The Spawner Class

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

## Wrapper Scripts

On the HPC system, wrapper scripts are used to execute and stop the job (`batch_submit_cmd` & `batch_cancel_cmd`) so that other functions, such as creating a "home directory" on the HPC system, can be used.

## Procedure

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
        3. call of 'jh_start_notebook_environment' with node type (GPU or compute node) as first argument $1

    * __*`jh_start_notebook_environment`*__:

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
