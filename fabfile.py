import os
from socket import gethostname

from fabric.api import cd, env, lcd, local, put, run, sudo
from fabric.contrib.files import exists

app_dir = '/apps/moonie_web'
git_repo = 'https://github.com/musale/moweb.git'

tmp = "/tmp/moonie"
tmp_f = "%s/moonie.tar.gz" % tmp

env.use_ssh_config = True
env.hosts = ['moonie']
if env.hosts == ['moonie']:
    user = 'vagrant'
else:
    user = 'root'

sql = "CREATE DATABASE moonie;CREATE USER 'moonie'@'%'" +\
      " IDENTIFIED BY 'user@moonie';GRANT ALL PRIVILEGES ON " +\
      "moonie.* TO  'moonie'@'%';FLUSH PRIVILEGES;"


def stage():
    env.hosts = ['moon']


def live():
    env.hosts = ['digi']


def setup():
    sudo('yum -y install epel-release')
    sudo('yum -y update')
    setup_db()
    setup_app()


def deploy():
    pull_updates()
    prep_remote()
    restart_services()


def pull_updates():
    with cd(app_dir):
        if not exists('static'):
            run('mkdir static')
        if not exists('media'):
            run('mkdir media')
        if not exists('moonie'):
            run('git clone %s' % git_repo)
        with cd('moonie'):
            run('git pull origin master')
        with cd('/var/log'):
            if not exists('moonie'):
                sudo('mkdir -p moonie/app')
                sudo('chown -R %s:%s moonie')
                run('touch moonie/app/moonie.log')


def xdeploy():
    if os.path.exists(tmp):
        local('rm -rf %s' % tmp)
    local('mkdir %s' % tmp)
    with lcd(app_dir):
        local('tar -czhf %s moonie --exclude=".git*"' % (tmp_f))
    if exists(tmp):
        run('rm -rf %s' % tmp)
    run('mkdir %s' % tmp)
    put(tmp_f, tmp_f)
    with cd(app_dir):
        if exists('moonie'):
            run('rm -rf moonie')
        run('tar -xzf %s' % tmp_f)
        with cd('/var/log'):
            if not exists('moonie'):
                sudo('mkdir -p moonie/app')
                sudo('chown -R %s:%s moonie' % (user, user,))
                run('touch moonie/app/moonie.log')
    prep_remote()
    restart_services()


def prep_remote():
    """Prepare remote for deployment."""
    with cd('%s/moonie' % app_dir):
        sudo('pip install -r requirements.txt')
        run('python manage.py makemigrations')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')


def setup_db():
    sudo('yum install -y mariadb mariadb-devel mariadb-server')
    start_mysql()
    enable_mysql()
    sudo('mysql_secure_installation')
    run('mysql -u root -proot@fmob -e "%s"' % (sql,))


def setup_app():
    """Set up app server."""
    sudo('yum install -y gcc nginx python-pip python-devel')
    print gethostname()
    if not exists(app_dir):
        sudo('mkdir -p %s' % (app_dir,))
        sudo('chown -R %s:%s /apps' % (user, user,))
        run('mkdir %s/static' % (app_dir,))
        run('mkdir %s/media' % (app_dir,))
    xdeploy()
    sudo('cp /apps/moonie_web/moonie/config/moonie.conf ' +
         '/etc/nginx/conf.d/moonie.conf')
    sudo('cp /apps/moonie_web/moonie/config/moonie.service ' +
         '/etc/systemd/system/moonie.service')
    sudo('systemctl daemon-reload')
    start_nginx()
    start_fortis()


def restart_services():
    restart_moonie()


def restart_moonie():
    sudo('systemctl restart moonie')


def start_fortis():
    sudo('systemctl start moonie')


def install_reqs():
    sudo('pip install -r requirements.txt')


def start_mysql():
    sudo('systemctl start mariadb')


def enable_mysql():
    sudo('systemctl enable mariadb')


def start_nginx():
    sudo('systemctl start nginx')


def enable_nginx():
    sudo('systemctl enable nginx')
