# Troubleshooting

## Enable debug mode

In the configuration file _jh_config_ you can enable the debug mode with the variable _enable_debug_mode_. Just set the value to true.

If the debug mode has been activated, the command defined in _cmd_run_job_debug_ is used to start a job on the HPC system. This way STDOUT/STDERR can be redirected.
In addition, the logs are filled with extended information so that it is possible to observe what is happening.
