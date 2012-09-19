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

readonly COVERAGE=$(command -v coverage)


function usage()
{
  cat <<Usage_Heredoc
Usage: $(basename $0) [OPTIONS]

Tiny wrapper script for running all unit tests and showing test coverage.

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
        error "Unknown option: $1. Try $(basename $0) -h for options."
        ;;
    esac

    shift
  done
}

function check_preconditions()
{
  test -z $COVERAGE && error "coverage: no such command"
}

function get_coverage()
{
  coverage run run_all_tests.py
  coverage report -m
}


parse_options "$@"
check_preconditions
get_coverage
