#!/usr/bin/env bash
set -u
set -e

# Configurable items
PGBOUNCER_LOCAL="37.235.102.243"
PGBOUNCER_REMOTE="37.235.102.54"
PGPASSWORD="pass"
PGBOUNCER_DATABASE_INI="/etc/pgbouncer/pgbouncer-other.ini"
PGBOUNCER_DATABASE="repmgr"
PGBOUNCER_PORT=6432
POSTGRES_PORT=5435
REPMGR_CONFIG="/etc/postgresql/11/ha_snd/repmgr/repmgr_snd.conf"
SSH_PATH="/var/lib/postgresql/.ssh/rop_rsa"

# 1. Promote this node from standby to primary

repmgr standby promote -f $REPMGR_CONFIG --log-to-file

# 2. Reconfigure pgbouncer instances

PGBOUNCER_DATABASE_INI_NEW="/tmp/pgbouncer-other.ini"

# Recreate the pgbouncer config file
echo -e "[databases]\n" > $PGBOUNCER_DATABASE_INI_NEW
echo -e "\"$PGBOUNCER_DATABASE\"= host=\"$PGBOUNCER_LOCAL\" port=$POSTGRES_PORT" >> $PGBOUNCER_DATABASE_INI_NEW

# Add new key to ssh client
eval `ssh-agent -s`
ssh-add $SSH_PATH

cp $PGBOUNCER_DATABASE_INI_NEW $PGBOUNCER_DATABASE_INI
scp $PGBOUNCER_DATABASE_INI_NEW postgres@$PGBOUNCER_REMOTE:$PGBOUNCER_DATABASE_INI

# 3. Restart pgbouncer instances

PGPASSWORD=$PGPASSWORD psql -tc "reload" -h $PGBOUNCER_LOCAL -p $PGBOUNCER_PORT -U postgres pgbouncer
PGPASSWORD=$PGPASSWORD psql -tc "reload" -h $PGBOUNCER_REMOTE -p $PGBOUNCER_PORT -U postgres pgbouncer

# Clean up generated file
rm $PGBOUNCER_DATABASE_INI_NEW

echo "Reconfiguration of pgbouncer complete"