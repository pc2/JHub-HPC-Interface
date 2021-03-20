#!/usr/bin/env python3

import sys;
import configparser;
import os;
import subprocess;
import tempfile;
import distutils.spawn;

class JupyterEnvironment:

    def __init__ (self, cmd):

        if type(cmd) == str:
            self.cmd = cmd.split(' ');
        else:
            self.cmd = cmd;

        self.build_cmd = [];

        lib_dir = os.path.dirname(__file__) + '/';
        self.config = configparser.ConfigParser();
        if os.path.isfile(lib_dir + 'config/jh_config.ini'):
            self.config.read(lib_dir + 'config/jh_config.ini');
        else:
            sys.exit(f'Could not find config file {lib_dir}config/jh_config.ini');

        use_singularity = self.config['singularity']['use_singularity'];
        use_overlay = self.config['singularity']['singularity_use_overlay'];
        singularity_extra_args = self.config['singularity']['singularity_extra_args'];

        if use_singularity == 'True' or use_singularity == 'true':
            if distutils.spawn.find_executable('singularity') == None:
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
                    username = os.environ['JUPYTERHUB_USER'];
                    if not os.path.isfile(f'{spec_overlay}/{username}.img'):
                        overlay_size = self.config['singularity']['singularity_overlay_size'];
                        dd_cmd = subprocess.Popen(f'dd if=/dev/zero of={spec_overlay}/{username}.img bs=1M count={overlay_size}', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL);
                        dd_cmd.wait();

                        # create an empty directory to specify the root directory of the new created overlay
                        overlay_root = tempfile.mkdtemp();
                        overlay_root_work = os.mkdir(overlay_root + '/work');
                        overlay_root_upper = os.mkdir(overlay_root + '/upper');
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

        # Run command in self.build_cmd
        self.start_environment(self.build_cmd);

    def start_environment (self, buildcmd):

        jupyter_env_cmd = subprocess.check_output(buildcmd, shell=True)
        filet = open('/tmp/subenv', 'w');
        filet.write(str(jupyter_env_cmd));
        filet.close();
        self.ssh_tunnel();
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
            
            if not os.path.isfile(str(self.ssh_keypath)):
                sys.exit('Error: Cannot find private SSH key to make the JupyterHub API available on the compute node');

            ssh_api_cmd = f'ssh -fN -i {self.ssh_keypath} -o StrictHostKeyChecking=no -L {self.ssh_api_dest_port}:127.0.0.1:{self.ssh_api_port} {self.ssh_tunnel_user}@{self.jupyterhub_ip}';

            subprocess.Popen(ssh_api_cmd, shell=True);



if __name__ == '__main__':
    JupyterEnvironment(sys.argv[1:]);
