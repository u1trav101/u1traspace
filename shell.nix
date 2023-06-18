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
  '';
}
