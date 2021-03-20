import os;
import sys;
import configparser;

class manageInstance:

    def __init__ (self, jobfile):

        self.jobfile = jobfile;
        self.jobstate = None;
        self.jobid = None;
        self.session = None;

        lib_dir = os.path.dirname(__file__) + '/';
        self.config = configparser.ConfigParser();
        if os.path.isfile(lib_dir + 'config/jh_config.ini'):
            self.config.read(lib_dir + 'config/jh_config.ini');
        else:
            sys.exit(f'Could not find config file {lib_dir}config/jh_config.ini');

        # check whether maintenance mode is activated
        maintenance = self.config['maintenance']['maintenance'];
        maintenance_user = self.config['maintenance']['maintenance_user'];

        if maintenance == 'True' or maintenance == 'true':
            if not str(maintenance_user) == str(os.environ['JUPYTERHUB_USER']):
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

        if self.session == None:

            check_debug = self.config['maintenance']['enable_debug_mode'];
            if check_debug == 'True':
                self.session = subprocess.check_output(self.config['workload_manager']['cmd_run_job'] + ' ' + filename, shell=True);
            else:
                self.session = subprocess.check_output(self.config['workload_manager']['cmd_run_job_debug'] + ' ' + filename, shell=True);

            if not self.session == None:
                self.session = self.session.decode('utf-8').rstrip();
            
            print(self.session);
