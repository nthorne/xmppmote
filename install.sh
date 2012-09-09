#!/bin/bash -

# vim: filetype=sh

# Set IFS explicitly to space-tab-newline to avoid tampering
IFS=' 	
'

# If found, use getconf to constructing a reasonable PATH, otherwise
# we set it manually.
if [[ -x /usr/bin/getconf ]]
then
  PATH=$(/usr/bin/getconf PATH)
else
  PATH=/bin:/usr/bin:/usr/local/bin
fi


# Binary paths
CP=$(command -v cp)
MKDIR=$(command -v mkdir)
BASENAME=$(command -v basename)
CHOWN=$(command -v chown)
CHMOD=$(command -v chmod)
SED=$(command -v sed)



# Target directories
INIT_DIR=/etc/init.d
INIT_CONFIG_DIR=/etc/default


function usage()
{
  cat <<Usage_Heredoc
Usage: $($BASENAME $0) [OPTIONS] [PATH]

Install XMPPMote to the location named by the PATH argument.

Where valid OPTIONS are:
  -h, --help  display usage
  

Usage_Heredoc
}

function error()
{
  echo "Error: $@" >&2
  exit 1
}

function parse_options()
{
  while (($#))
  do
    case $1 in
      -h|--help)
        usage
        exit 0
        ;;
      *)
        if [[ -z $INSTALL_PATH ]]
        then
          INSTALL_PATH=$1
        else
          error "Unknown option: $1. Try $($BASENAME $0) -h for usage."
        fi
        ;;
    esac

    shift
  done

  if [[ -z $INSTALL_PATH ]]
  then
    error "Installation path not given. Try $($BASENAME $0) -h for usage."
  fi
}

function check_preconditions()
{
  test -z $BASENAME && error "basename: no such command"
  test -z $CP && error "cp: no such command"
  test -z $MKDIR && error "mkdir: no such command"
  test -z $CHOWN && error "chown: no such command"
  test -z $CHMOD && error "chmod: no such command"
  test -z $SED && error "sed: no such command"

  local readonly expected_dirs=(
    $INIT_DIR
    $INIT_CONFIG_DIR
  )

  local readonly expected_files=(
    xmppmoterc.example
    rc/initd-xmppmote
    rc/config-xmppmote
  )

  for dir in ${expected_dirs[@]}
  do
    test -d $dir || error "$dir: no such directory"
  done

  for fil in ${expected_files[@]}
  do
    test -f $fil || error "$fil: no such file"
  done
}

function install_xmppmote()
{
  echo ".. creating $INSTALL_PATH"
  $MKDIR -p $INSTALL_PATH || error "$INSTALL_PATH: unable to create directory"

  echo ".. copying source files to $INSTALL_PATH"
  $CP -R . $INSTALL_PATH || error "unable to copy files to $INSTALL_PATH"

  pushd $INSTALL_PATH >/dev/null || error "unable to pushd to $INSTALL_PATH"

  echo ".. creating default configuration file"
  if [[ -w /var/run ]]
  then
    $SED 's/#\(pidfile:.*\)/\1/' xmppmoterc.example > xmppmoterc
  else
    $CP xmppmoterc.example xmppmoterc || error "unable to create default config"
  fi

  echo ".. changing configuration file's owner and permissions"
  $CHOWN daemon:daemon xmppmoterc || error "unable to make daemon owner of xmppmoterc"
  $CHMOD 600 xmppmoterc || error "unable to chmod xmppmoterc"

  echo ".. installing intscript"
  $CP rc/initd-xmppmote $INIT_DIR/xmppmote || error "unable to copy initscript"

  echo ".. creating initscript configuration file"
  $CP rc/config-xmppmote $INIT_CONFIG_DIR/xmppmote || error "unable to copy initscript config"

  echo ".. populating initscript configuration file"
  echo "# Added by install.sh" >> $INIT_CONFIG_DIR/xmppmote
  echo "DAEMON_PATH=$INSTALL_PATH" >> $INIT_CONFIG_DIR/xmppmote
  echo "DAEMON=\$DAEMON_PATH/\$NAME" >> $INIT_CONFIG_DIR/xmppmote

  echo ".. DONE!"
  popd >/dev/null
}


parse_options "$@"
check_preconditions
install_xmppmote

echo 
echo "If you want XMPPMote to start at system startup, either use any init"
echo "script insertion tool that comes with your system installation (e.g."
echo "update-rc.d), or simply create a symlink for the xmppmote init script to"
echo "the appropriate runlevel directory(/ies)."
