import os;
import sys;
import configparser;
import logging;

"""

Creating a temporary file, write STDIN into it and mark it as executable

"""

class manageInstance:

    def __init__ (self, jobfile):

        self.jobfile = jobfile;
        self.jobstate = None;
        self.jobid = None;
        self.session = None;

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

        # check whether maintenance mode is activated
        maintenance = self.config['maintenance']['maintenance'];
        maintenance_user = self.config['maintenance']['maintenance_user'];

        self.username = os.environ.get('JUPYTERHUB_USER');
        if self.username == None:
            self.log.critical('Cannot get the username from environment variable $JUPYTERHUB_USER')
            sys.exit('Cannot get the username from environment variable $JUPYTERHUB_USER');

        if maintenance == 'True' or maintenance == 'true':
            if not str(maintenance_user) == str(self.username):
                self.log.debug(f'Maintenance mode is activated. User {self.username} tried to start a notebook server');
                sys.exit('Maintenance mode is activated. Please ask your system administrator for more information.');

    def start (self):
   
        import tempfile;
        import subprocess;

        # create temp job file
        file, filename = tempfile.mkstemp();
        jobf = open(filename, 'w');
        jobf.write(str(self.jobfile));
        jobf.close();

        # mark temp script as executable
        os.chmod(filename, 0o774);

        self.log.debug(f'Temporary file {filename} for user {self.username} created!');

        if self.session == None:
            check_debug = self.config['general']['log_level'];
            if check_debug == 'DEBUG':
                self.session = subprocess.check_output(self.config['workload_manager']['cmd_run_job_debug'] + ' ' + filename, shell=True);
            else:
                self.session = subprocess.check_output(self.config['workload_manager']['cmd_run_job'] + ' ' + filename, shell=True);

            if not self.session == None:
                self.session = self.session.decode('utf-8').rstrip();
           
            self.log.debug(f'Job for user {self.username} seems to be started');
            # print out the output of self.session (Should be the job id)
            print(self.session);
