tflocal -chdir=infrastructure plan -out=tfplan
tflocal -chdir=infrastructure apply tfplan

