with (import <nixpkgs> {});
pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.env";
  nativeBuildInputs = [
    python311
    libmysqlclient
    zlib.dev
    python311Packages.pillow
    wget
    killall
  ];

  buildInputs = [
    redis
    mariadb_1011
    ffmpeg
  ];

  shellHook = ''
    set -h #remove "bash: hash: hashing disabled" warning !
    SOURCE_DATE_EPOCH=$(date +%s)
    if ! [ -d "${venvDir}" ]; then
      python -m venv "${venvDir}"
    fi
    source "${venvDir}/bin/activate"
    echo Upgrading pip...
    python -m pip install --upgrade pip -q -q -q --exists-action i
    echo Installing python packages...
    pip install -r requirements.txt -q -q -q --exists-action i

    mkdir -p $PWD/.nix-shell/redis/lib
    mkdir -p $PWD/.nix-shell/redis/log
    touch $PWD/.nix-shell/redis/log/redis-server.log
    echo Starting Redis...
    redis-server $PWD/redis.conf

    MYSQL_BASEDIR=${pkgs.mariadb}
    MYSQL_HOME=$PWD/.nix-shell/mysql
    MYSQL_DATADIR=$MYSQL_HOME/data
    export MYSQL_UNIX_PORT=$MYSQL_HOME/mysql.sock
    MYSQL_PID_FILE=$MYSQL_HOME/mysql.pid
    alias mysql='sudo mysql --socket=$MYSQL_UNIX_PORT'
    
    if [ ! -d "$MYSQL_HOME" ]; then
      # Make sure to use normal authentication method otherwise we can only
      # connect with unix account. But users do not actually exists in nix.
      echo Creating MariaDB database...
      mysql_install_db --auth-root-authentication-method=normal \
        --datadir=$MYSQL_DATADIR --basedir=$MYSQL_BASEDIR \
        --pid-file=$MYSQL_PID_FILE
    fi

    # Starts the daemon
    echo Starting MariaDB...
    mysqld --datadir=$MYSQL_DATADIR --pid-file=$MYSQL_PID_FILE \
      --socket=$MYSQL_UNIX_PORT 2> $MYSQL_HOME/mysql.log &
    MYSQL_PID=$!

    # Changes the mysql root password
    sudo mysql --socket=$MYSQL_UNIX_PORT -e "SET PASSWORD FOR root@'localhost' = PASSWORD('root')"

    # Downloads minio server and client
    if [ ! -f $PWD/minio ]; then
      echo Downloading minio...
      wget https://dl.min.io/server/minio/release/linux-amd64/minio
    fi
    if [ ! -f $PWD/mc ]; then
      echo Downloading minio client...
      wget https://dl.min.io/client/mc/release/linux-amd64/mc
    fi
    chmod +x minio
    chmod +x mc
    mkdir -p $PWD/.nix-shell/minio
    echo Starting MinIO...
    $PWD/minio server $PWD/.nix-shell/minio > /dev/null 2>&1 &
    sleep 1

    # Creating S3 bucket
    echo Creating S3 bucket...
    $PWD/mc alias set minio http://localhost:9000 minioadmin minioadmin
    $PWD/mc mb minio/chiyo-cdn

    # Starting celery
    echo Starting Celery worker...
    celery -A wsgi.celery_app worker > /dev/null 2>&1 &

    # Starting Flask
    python wsgi.py

    finish()
    {
      sudo mysqladmin --socket=$MYSQL_UNIX_PORT shutdown
      kill $MYSQL_PID
      wait $MYSQL_PID
      sudo killall celery
      sudo killall minio
      sudo killall redis-server
    }
    trap finish EXIT
  '';
}
