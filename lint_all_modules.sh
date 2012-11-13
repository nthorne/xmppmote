#!/bin/bash -

#Copyright (C) 2012 Niklas Thorne.

#This file is part of XMPPMote.
#
#XMPPMote is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#XMPPMote is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with XMPPMote.  If not, see <http://www.gnu.org/licenses/>.

# vim: filetype=sh

# Set IFS explicitly to space-tab-newline to avoid tampering
IFS=' 	
'

readonly PYLINT=$(command -v pylint)
readonly PYLINT_ARGS="--reports=n --output-format=parseable "
LINT_TESTS=
FILENAMES_ONLY=


function usage()
{
  cat <<Usage_Heredoc
Usage: $(basename $0) [OPTIONS]

Tiny wrapper script for linting all modules (non-unit test python files); only
produces output for those modules that contains lint remarks.

Where valid OPTIONS are:
  -h, --help            display usage
  -t, --tests           lint unit tests as well
  -f, --filenames-only  only output filenames - useful for eg.
                        vim \$($(basename $0) -f)

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
      -t|--tests)
        if [[ -z $LINT_TESTS ]]
        then
          LINT_TESTS=1
        else
          error "duplicate tests flag"
        fi
        ;;
      -f|--filenames-only)
        if [[ -z $FILENAMES_ONLY ]]
        then
          FILENAMES_ONLY=1
        else
          error "duplicate filenames-only flag"
        fi
        ;;
      *)
        error "Unknown option: $1. Try $(basename $0) -h for options."
        ;;
    esac

    shift
  done
}

function check_preconditions()
{
  test -z $PYLINT && error "pylint: no such command"
}

function lint_modules()
{
  local FILE
  local FILE_MATCH_PATTERN='-name "*.py" ! -name "__init__.py"'
  local RESPONSE
  local OUTPUT

  if [[ -z $LINT_TESTS ]]
  then
    FILES=`find . -name '*.py' ! -name '__init__.py' ! -name 'test_*.py'`
  else
    FILES=`find . -name '*.py' ! -name '__init__.py'`
  fi

  for FILE in $FILES
  do
    RESPONSE=`$PYLINT $PYLINT_ARGS $FILE 2>/dev/null`
    if [[ ! -z $RESPONSE ]]
    then
      if [[ ! -z $FILENAMES_ONLY ]]
      then
        OUTPUT="$OUTPUT $FILE"
      else
        echo $FILE
        echo "$RESPONSE"
        echo
      fi
    fi
  done

  if [[ ! -z $OUTPUT ]]
  then
    echo $OUTPUT
  fi
}


parse_options "$@"
check_preconditions
lint_modules
