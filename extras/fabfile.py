from fabric.api import env, local, run, sudo, put
from fabric.contrib.files import upload_template

  
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # use vagrant ssh key
    result = local('vagrant ssh_config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]

def openrdiopenrdi():
    env.user = 'ubuntu'
    env.hosts = ['openrdi.openrdi.org']
    env.key_filename = 'geonode-gfdrr-labs.pem'

def install():
    """Install openrdi and it's dependencies
    """
    run('wget https://github.com/GFDRR/openrdi/raw/master/scripts/openrdi-install')
    run('echo "source ~/venv/bin/activate" >> .bash_aliases')
    run('bash openrdi-install')

def production():
    """Install and configure Apache and Tomcat
    """
    ctx = dict(user=env.user, host=env.host, project_home='/home/%s' % env.user)
    upload_template('project.apache', 'project.apache', context=ctx)
    sudo('apt-get install -y libapache2-mod-wsgi')
    sudo('/bin/mv -f project.apache /etc/apache2/sites-available/openrdi')
    sudo('ln -sf /etc/default/geonode %s/openrdi/openrdi/local_settings.py' % ctx['project_home'])
    sudo('a2dissite default')
    sudo('a2ensite openrdi')
    sudo('a2enmod proxy_http')
    run('mkdir -p logs')
    run('. venv/bin/activate; openrdi collectstatic --noinput')
    sudo('/etc/init.d/apache2 restart')

def manual():
    """Manual steps, not everything can be automated, but we try.
    """

    print "Please perform the following manual steps"
    print
    # Step 1
    print "Step 1. Create a superuser to administer Risk in a Box"
    print "        ssh into the production server and run:"
    print "        django-admin.py createsuperuser"


def openrdi():
    """Do a full production setup of Haitidata
    """

    install()
    production()
    manual()

def stop():
    """Stop openrdi
    """

    sudo('service tomcat6 stop')
    sudo('service apache2 stop')
    #FIXME: This can have unintended consecuences shutting down
    # a Java server that is not GeoNode related.
#    sudo('killall -9 java')

def start():
    """Start openrdi
    """

    run('source venv/bin/activate;django-admin.py syncdb --noinput')
    sudo('service tomcat6 start')
    sudo('service apache2 start')

def restart():
    """Restart openrdi
    """

    stop()
    start()

def pull():
    """Pull the latest changes of the codebase from github and reload the server
    """

    run('cd openrdi; git pull')
    run('cd geonode; git pull')
    run('touch openrdi/extras/project.wsgi')

def log():
    """Handy way to check the logs
    """

    GEOSERVER_LOG = 'tomcat/webapps/geoserver-geonode-dev/data/logs/geoserver.log'
    run('tail logs/*')
    run('tail -n 50 %s' % GEOSERVER_LOG)

def dns():
    """Useful when default DNS does not work
    """
    sudo('rm /etc/resolv.conf')
    sudo('echo "nameserver 4.2.2.2" >> /etc/resolv.conf')


def ariel():
    """Setup dev env for Ariel
    """
    sudo('apt-get install -y git-core')
    put('id_rsa', '.ssh/id_rsa')
    put('id_rsa.pub', '.ssh/id_rsa.pub')
    run('git config --global user.name "Ariel Nunez"')
    run('git config --global user.email ingenieroariel@gmail.com')


def robert():
    """Setup dev env for Robert
    """
    sudo('apt-get install -y git-core')
    put('id_dsa', '.ssh/id_dsa')
    put('id_dsa.pub', '.ssh/id_dsa.pub')
    run('git config --global user.name "Robert Soden"')
    run('git config --global user.email robert.soden@gmail.com')
