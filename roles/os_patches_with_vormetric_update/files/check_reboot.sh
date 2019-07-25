#/bin/bash

if [[ -f /etc/SuSE-release ]]; then
        OS="SLES"
        OSV=$(cat /etc/SuSE-release |awk '/VERSION|PATCHLEVEL/ {print}' |sed 's/VERSION = //'|sed 's/PATCHLEVEL = /SP/' | paste -d ' ' - - | sed 's/ //g')
fi

if [[ -f /etc/redhat-release ]]; then
        OS="RHEL"
        OSV=$(cat /etc/redhat-release| sed 's/[a-zA-Z ()]//g' | tail -1)
fi

OS="${OS}${OSV}"
HOST=$(hostname -s)

REBOOTDATE=$(date -d "$(</proc/uptime awk '{print $1}') seconds ago" +%s)
KERNELDATE=$(rpm -qa --queryformat '%{installtime}\n' kernel*)
GLIBCDATE=$(rpm -qa --queryformat '%{installtime}\n' glibc)

KDIFFS=$(for KHISTORY in `echo ${KERNELDATE} | tr ' ' '\n'`; do echo "$((${KHISTORY} - ${REBOOTDATE}))"; done)
GDIFFS=$(for GHISTORY in `echo ${GLIBCDATE} | tr ' ' '\n'`; do echo "$((${GHISTORY} - ${REBOOTDATE}))"; done)

KFIRST=$(echo ${KDIFFS[@]} | tr ' ' '\n' | grep -v ^- | sort | head -n 1)
GFIRST=$(echo ${GDIFFS[@]} | tr ' ' '\n' | grep -v ^- | sort | head -n 1)

[[ -n ${GFIRST} ]] && { REBOOTREQUIRED="RebootRequired"; REBOOTREASON="glibc"; }
[[ -n ${KFIRST} ]] && { REBOOTREQUIRED="RebootRequired"; REBOOTREASON="kernel"; }


# on RHEL7 this also catches updated systemd
[[ ${OS} = RHEL7* ]] && [[ $(/usr/bin/needs-restarting -r | grep "Reboot is required") ]] && REBOOTREQUIRED="RebootRequired"

echo $REBOOTREQUIRED
