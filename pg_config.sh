debconf-set-selections <<< 'mysql-server mysql-server/root_password password 12345'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 12345'
apt-get -qqy update
apt-get -qqy install -y mysql-server-5.5
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
apt-get install mysql-client-core-5.5
apt-get install python-dev libmysqlclient-dev
pip install -U pip
pip install MySQL-python
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install redis
pip install passlib
pip install itsdangerous
pip install flask-httpauth
su mysql -c 'createuser -dRS vagrant'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
