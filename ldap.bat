#docker pull osixia/openldap
#docker pull osixia/phpldapadmin

#ldapsearch -x -H ldap://127.0.0.1:389 -b dc=ZHAN,dc=com -D "cn=admin,dc=ZHAN,dc=com" -w 881224

# docker run -p 389:389 -p 636:636 --name my-openldap-container --env LDAP_ORGANISATION="ZHAN" --env LDAP_DOMAIN="ZHAN.COM" --env LDAP_ADMIN_PASSWORD="881224" -it osixia/openldap 

# docker run -p 389:389 -p 636:636 --name my-openldap-container --env LDAP_ORGANISATION="ihopeit" --env LDAP_DOMAIN="ihopeit.com" --env LDAP_ADMIN_PASSWORD="admin_passwd_4_ldap" --detach osixia/openldap

docker run -d --privileged -p 80:80 -p 443:443 --name phpldapadmin-service --hostname phpldapadmin-service --link my-openldap-container:ldap-host --env PHPLDAPADMIN_HTTPS=false --env PHPLDAPADMIN_LDAP_HOSTS=ldap-host -it osixia/phpldapadmin
