#!/bin/bash -x
## Copy files to S3 
## TODO: 
##   - Encrypt files
##   - Split files > 5GB (required for S3)
##   - Add restore steps

## Vars
tdate=$(date '+%Y%m%d%H%M')

s3bucket="flickrflask"
s3base="flickrflask/backups/${tdate}/"
backup_dir="/mnt/mysql_backups/${tdate}"
readme="${backup_dir}/README.txt"

backup_filename="${backup_dir}/mysql_backup_${tdate}.sql"
backup_tarball="${backup_dir}/mysql_backup_${tdate}.tar.gz"
scriptname=`basename $0`

## Functions
log() {
# log to syslog
logger -i -t ${scriptname} "$@"
echo "$@"
}

## Script
log "INFO: start s3backup of ${backup_dir} to S3 bucket ${s3bucket}"

: ${DATABASE_HOST:?"Need to set DATABASE_HOST "}
: ${DATABASE_PASSWORD:?"Need to set DATABASE_PASSWORD "}
: ${DATABASE_USERNAME:?"Need to set DATABASE_USERNAME "}
: ${AWS_ACCESS_KEY_ID:?"Need to set AWS_ACCESS_KEY_ID "}
: ${AWS_SECRET_ACCESS_KEY:?"Need to set AWS_SECRET_ACCESS_KEY"}

#check for tmp local backup dir
if [ ! -d ${backup_dir} ]; then
    mkdir -p ${backup_dir}
    if [ $? != 0 ]; then
        log "ERROR: unable to create tmp backup dir ${backup_dir}"
        exit 1
    fi
fi


#create backup
/usr/bin/mysqldump --all-databases --complete-insert -h $DATABASE_HOST -u $DATABASE_USERNAME --password=$DATABASE_PASSWORD > ${backup_filename}

if [ $? != 0 ]; then
  log "ERROR: could not create mysqlbackup"
  exit 1
fi

#create backup tarball
/bin/tar -zcvf ${backup_tarball} ${backup_filename}

aws s3 cp ${backup_tarball} s3://${s3base}
aws s3 ls s3://${s3base} | grep .tar.gz
if [ $? != 0 ]; then
  log "ERROR: backup of: ${backup_filename} to S3 ${s3base} FAILED"
  exit 1
fi
log "INFO: s3backup sync of: ${backup_filename} to S3 ${s3base} complete"
rm -rf ${backup_dir}

