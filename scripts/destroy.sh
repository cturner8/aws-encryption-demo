tflocal -chdir=infrastructure plan -out=tfplan -destroy
tflocal -chdir=infrastructure apply tfplan

