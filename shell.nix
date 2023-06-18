with (import <nixpkgs> {});
pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.env";
  nativeBuildInputs = [
    python311
    libmysqlclient
    zlib.dev
    python311Packages.pillow
  ];

  buildInputs = [
    redis
    mariadb
    ffmpeg
  ];

  shellHook = ''
    set -h #remove "bash: hash: hashing disabled" warning !
    SOURCE_DATE_EPOCH=$(date +%s)
    if ! [ -d "${venvDir}" ]; then
      python -m venv "${venvDir}"
    fi
    source "${venvDir}/bin/activate"
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    mkdir -p .redis/lib
    mkdir -p .redis/log
    touch .redis/log/redis-server.log
    redis-server redis.conf

    MYSQL_BASEDIR=${pkgs.mariadb}
    MYSQL_HOME=$PWD/.mysql
    MYSQL_DATADIR=$MYSQL_HOME/data
    export MYSQL_UNIX_PORT=$MYSQL_HOME/mysql.sock
    MYSQL_PID_FILE=$MYSQL_HOME/mysql.pid
    alias mysql='mysql -u root'

    if [ ! -d "$MYSQL_HOME" ]; then
      # Make sure to use normal authentication method otherwise we can only
      # connect with unix account. But users do not actually exists in nix.
      mysql_install_db --auth-root-authentication-method=normal \
        --datadir=$MYSQL_DATADIR --basedir=$MYSQL_BASEDIR \
        --pid-file=$MYSQL_PID_FILE
    fi

    # Starts the daemon
    mysqld --datadir=$MYSQL_DATADIR --pid-file=$MYSQL_PID_FILE \
      --socket=$MYSQL_UNIX_PORT 2> $MYSQL_HOME/mysql.log &
    MYSQL_PID=$!

    finish()
    {
      mysqladmin -u root --socket=$MYSQL_UNIX_PORT shutdown
      kill $MYSQL_PID
      wait $MYSQL_PID
    }
    trap finish EXIT
  '';
}
