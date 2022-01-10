#!/usr/bin/env bash

# These are scripts that will be imported to other scripts as needed.
# to run tests call the tests() function.
# Enhancement would be to add a "source-only" option to exclude certain functions 
# See https://stackoverflow.com/questions/12815774/importing-functions-from-a-shell-script

# NOTICE: Uncomment if your script depends on bashisms.
#if [ -z "$BASH_VERSION" ]; then bash $0 $@ ; exit $? ; fi

# Code template for parsing command line parameters using only portable shell
# code, while handling both long and short params, handling '-f file' and
# '-f=file' style param data and also capturing non-parameters to be inserted
# back into the shell positional parameters.
# This example shows parameter options as follows
# -c | --config => Configuration file that must provide a valid/readable file
#                  Additionally, this option can be in the form -c|--config=<file>
#                  Or -c|--config <file> (without the equals sign)
#                  So running <script>.sh --config dave.sh or <script>.sh --config=dave.sh both work
# -f | --force  => A flag switch option (no value provided) that sets a boolean env variable
# -n | --count  => An option that should be a numeric integer value
# --            => If -- is provided, everything after is ignored

process_args() {
                while [ -n "$1" ]; do
                # Copy so we can modify it (can't modify $1)
                OPT="$1"
                # Detect argument termination
                if [ x"$OPT" = x"--" ]; then
                        shift
                        for OPT ; do
                                REMAINS="$REMAINS \"$OPT\""
                        done
                        break
                fi
                # Parse current opt
                while [ x"$OPT" != x"-" ] ; do
                        case "$OPT" in
                                # Handle --flag=value opts like this
                                -c=* | --config=* )
                                        CONFIGFILE="${OPT#*=}"
                                        shift
                                        ;;
                                # and --flag value opts like this
                                -p* | --profile )
                                        PROFILE="$2"
                                        shift
                                        ;;
                                # and --flag value opts like this
                                -c* | --config )
                                        CONFIGFILE="$2"
                                        shift
                                        ;;
                                -f* | --force )
                                        FORCE=true
                                        ;;
                                # --count=value opts like this
                                -n=* | --count=* )
                                        COUNT="${OPT#*=}"
                                        shift
                                        ;;
                                # --count value opts like this
                                -n* | --count )
                                        COUNT="$2"
                                        shift
                                        ;;
                                # Anything unknown is recorded for later
                                * )
                                        REMAINS="$REMAINS \"$OPT\""
                                        break
                                        ;;
                        esac
                        # Check for multiple short options
                        # NOTICE: be sure to update this pattern to match valid options
                        NEXTOPT="${OPT#-[cfn]}" # try removing single short opt
                        if [ x"$OPT" != x"$NEXTOPT" ] ; then
                                OPT="-$NEXTOPT"  # multiple short opts, keep going
                        else
                                break  # long form, exit inner loop
                        fi
                done
                # Done with that param. move to next
                shift
        done
        # Set the non-parameters back into the positional parameters ($1 $2 ..)
        eval set -- $REMAINS
}

in_path()
{
  # given a command and the PATH, try to find the command. Returns
  # 0 if found and executable, 1 if not. Note that this temporarily modifies 
  # the the IFS (input field seperator), but restores it upon completion.

  cmd=$1
  path=$2
  retval=1
  oldIFS=$IFS
  IFS=":"

  for directory in $path
  do
    if [ -x $directory/$cmd ] ; then
      retval=0      # if we're here, we found $cmd in $directory
    fi
  done
  IFS=$oldIFS
  return $retval
}

checkForCmdInPath()
{
  var=$1
  
  # The variable slicing notation in the following conditional 
  # needs some explanation: ${var#expr} returns everything after
  # the match for 'expr' in the variable value (if any), and
  # ${var%expr} returns everything that doesn't match (in this
  # case just the very first character. You can also do this in
  # Bash with ${var:0:1} and you could use cut too: cut -c1
  
  # echo "Looking for $var in Path"
  if [ "$var" != "" ] ; then
    if [ "${var%${var#?}}" = "/" ] ; then
      if [ ! -x $var ] ; then
        return 1
      fi
    elif ! in_path $var $PATH ; then
      return 2
    fi 
  fi
}

sayhi() {
        echo "Saying Hi from the import_functions script"
}

tests() {
        echo -e "Results=> config file ='$CONFIGFILE' force='$FORCE' count='$COUNT' remains='$REMAINS'"
}

confirm_aws() {
	# Verify AWS CLI Credentials are setup
	# http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
	if ! grep -q aws_access_key_id ~/.aws/credentials; then
		if ! grep -q aws_access_key_id ~/.aws/config; then
			fail "AWS config not found or CLI not installed. Please run \"aws configure\"."
		fi
	fi
}

get_aws_account_alias() {
	profile=$1
	aws_account_name=$(aws iam list-account-aliases --profile $profile --output text | cut -f 2)
}