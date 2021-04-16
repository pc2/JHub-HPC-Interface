#!/usr/bin/env python3

import sys;
import configparser;
import os;
import subprocess;
import tempfile;
import distutils.spawn;
import logging;

class JupyterEnvironment:

    def __init__ (self, cmd):

        if type(cmd) == str:
            self.cmd = cmd.split(' ');
        else:
            self.cmd = cmd;

        self.build_cmd = [];

        # read config file
        lib_dir = os.path.dirname(__file__) + '/';
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation());
        if os.path.isfile(lib_dir + 'config/jh_config.ini'):
            self.config.read(lib_dir + 'config/jh_config.ini');
        else:
            sys.exit(f'Could not find config file {lib_dir}config/jh_config.ini');

        # setup logging
        logging.basicConfig(
            filename=str(self.config['general']['log_file']),
            level=str(self.config['general']['log_level']),
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
        );

        self.log = logging.getLogger(__name__);
        self.log.addHandler(logging.NullHandler());

        # get username
        self.username = os.environ.get('JUPYTERHUB_USER');
        if self.username == None:
            self.log.critical('Cannot get the username with the environment variable $JUPYTERHUB_USER!');
            sys.exit('Cannot get the username with the environment variable $JUPYTERHUB_USER!');

        # read config file values
        use_singularity = self.config['singularity']['use_singularity'];
        use_overlay = self.config['singularity']['singularity_use_overlay'];
        singularity_extra_args = self.config['singularity']['singularity_extra_args'];

        if use_singularity == 'True' or use_singularity == 'true':
            if distutils.spawn.find_executable('singularity') == None:
                self.log.critical('"use_singularity" in jh_config.ini is set to true but cannot find singularity executable!');
                sys.exit("'use_singularity' in jh_config.ini is set to true but cannot find singularity executable?");
            self.build_cmd.append('singularity exec');
            if 'compute' in self.cmd:
                singularity_container = self.config['singularity']['singularity_container_compute'];
                self.cmd.remove('compute');
            elif 'gpu' in self.cmd:
                singularity_container = self.config['singularity']['singularity_container_gpu'];
                self.cmd.remove('gpu');
            if use_overlay == 'True' or use_overlay == 'true':
                create_overlay = self.config['singularity']['singularity_overlay_c'];
                spec_overlay = self.config['singularity']['singularity_overlay_location'];
                if create_overlay == 'spec':
                    self.build_cmd.append(f'--overlay {spec_overlay}');
                elif create_overlay == 'auto':
                    username = self.username;
                    self.build_cmd.append(f'--overlay {spec_overlay}/{username}.img');
                    if not os.path.isfile(f'{spec_overlay}/{username}.img'):
                        overlay_size = self.config['singularity']['singularity_overlay_size'];
                        self.log.info(f'Creating Singularity overlay for user {username}');
                        dd_cmd = subprocess.Popen(f'dd if=/dev/zero of={spec_overlay}/{username}.img bs=1M count={overlay_size}', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL);
                        dd_cmd.wait();

                        # create an empty directory to specify the root directory of the new created overlay
                        overlay_root = tempfile.mkdtemp();
                        try: 
                            overlay_root_work = os.mkdir(overlay_root + '/work');
                            overlay_root_upper = os.mkdir(overlay_root + '/upper');
                        except OSError:
                            self.log.critical(f'Cannot create a valid Singularity overlay in directory {overlay_root}!');
                            sys.exit(f'Cannot create a valid Singularity overlay in directory {overlay_root}!');
                        self.log.debug(f'Create a ext3 filesystem for user {spec_overlay}/{username}.img');
                        ext3_cmd = subprocess.Popen(f'mkfs.ext3 -Fqd {overlay_root} -t ext3 {spec_overlay}/{username}.img', shell=True, stdout=subprocess.DEVNULL);
                        ext3_cmd.wait();
            if not singularity_extra_args == '':
                extra_arguments = singularity_extra_args.split(',');
                for i in extra_arguments:
                    self.build_cmd.append(str(i));

            self.build_cmd.append(str(singularity_container));

        # check for keywords like compute or singularity to delete
        if 'compute' in self.cmd:
            self.cmd.remove('compute');
        if 'gpu' in self.cmd:
            self.cmd.remove('gpu');

        self.build_cmd.append(" ".join(self.cmd));

        self.build_cmd = ' '.join(self.build_cmd);

        # Configure the environment with environment variables from jh_config.ini
        self.configure_environment();
        # Run command in self.build_cmd
        self.start_environment();

    def configure_environment (self):
        self.jupyterhub_api_url = self.config['general']['jupyterhub_api_url'];
        os.environ['JUPYTERHUB_API_URL'] = str(self.jupyterhub_api_url);

    def start_environment (self):
        if not self.build_cmd == None:
            self.log.info(f'Starting Jupyter Environment for user {self.username} with cmd: {self.build_cmd}');
            self.ssh_tunnel();
            jupyter_env_cmd = subprocess.check_output(self.build_cmd, shell=True)
            jupyter_env_cmd.wait();

    def ssh_tunnel (self):

        # make the JupyterHub API available on the compute node on 127.0.0.1:$ssh_tunnel_dst_api_port
        self.ssh_api = self.config['ssh_config']['ssh_tunnel_api'];
        if self.ssh_api == 'True' or self.ssh_api == 'true':
            self.ssh_api_port = self.config['ssh_config']['ssh_tunnel_src_api_port'];
            self.ssh_api_dest_port = self.config['ssh_config']['ssh_tunnel_dst_api_port'];
            self.ssh_tunnel_user = self.config['ssh_config']['ssh_tunnel_user'];
            self.jupyterhub_ip = self.config['general']['jupyterhub_ip'];
            self.ssh_keypath = self.config['ssh_config']['ssh_keypath'];
            
            if not os.path.isfile(os.path.expandvars(str(self.ssh_keypath))):
                self.log.critical(f'Cannot find private SSH key {self.ssh_keypath}!');
                sys.exit(f'Error: Cannot find private SSH key ({self.ssh_keypath})to make the JupyterHub API available on the compute node');

            ssh_api_cmd = f'ssh -fN -i {self.ssh_keypath} -o StrictHostKeyChecking=no -L {self.ssh_api_dest_port}:127.0.0.1:{self.ssh_api_port} {self.ssh_tunnel_user}@{self.jupyterhub_ip}';
            self.log.debug(f'Starting SSH tunnel for the JupyterHub API with cmd: {ssh_api_cmd}');

            subprocess.Popen(ssh_api_cmd, shell=True);

        else:
            self.log.debug('"ssh_tunnel_api" inf jh_config.ini is set to False. Do not start a SSH tunnel for the JupyterHub API!');



if __name__ == '__main__':
    JupyterEnvironment(sys.argv[1:]);
