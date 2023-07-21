#
# Regular cron jobs for the forensic-vm package
#
0 4	* * *	root	[ -x /usr/bin/forensic-vm_maintenance ] && /usr/bin/forensic-vm_maintenance
