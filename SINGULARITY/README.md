# Singularity

All containers should run as user jovyan.

See here for more information:
https://jupyter.readthedocs.io/en/latest/community/content-community.html#what-is-a-jovyan

The value `USER_ID` inside the Singularity recipes should be the UID of the user who is responsible for the calculations.

If you want to create a singularity recipe, you have to install (at least) following python packages:

* notebook
* batchspawner
* jupyterhub
