# Shibboleth

Shibboleth authentication was set up for a JupyterHub server in a test environment. Usually, metadata is exchanged directly between the service provider (SP) and the identity provider (IdP). Since JupyterHub currently does not have a plugin for this purpose, an additional proxy server had to be used. Authentication is done via an Apache reverse proxy, which then forwards the user to JupyterHub. For this purpose the [Jupyterhub REMOTE_USER Authenticator](https://github.com/cwaldbieser/jhub_remote_user_authenticator) was used. In our case, the IdP is hosted at [DFN](https://doku.tid.dfn.de/de:aai:about).

This is an **experimental setup** that has not yet been tested in productive use. The following configurations are therefore for orientation purposes only. **Use at your own risk.**

## Proxy server (Shibboleth service provider)

Apache configuration:

- `/etc/apache2/conf-enabled/shib.conf`

Shibboleth configuration:

- `/etc/shibboleth/shibboleth2.xml`

Attribute map (translates attribute names submitted by the IdP into expressions that the Shibboleth SP can understand):

- `/etc/shibboleth/attribute-map.xml`

Configuration files for the virtual host:

- `/etc/apache2/sites-available/000-default.conf`
- `/etc/apache2/sites-available/sp-proxy.conf`

## JupyterHub server

Configuration of JupyterHub:

- `/etc/jupyterhub/jupyterhub_config.py`

Python module that contains remote user authentication classes:

- `/usr/local/lib/python3.6/dist-packages/jhub_remote_user_authenticator/remote_user_auth.py`
