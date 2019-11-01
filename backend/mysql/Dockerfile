FROM mysql:5.7.28

LABEL maintainer="TavisD <tavisdxh@outlook.com>"

COPY docker-entrypoint-initdb.d/*.sql /docker-entrypoint-initdb.d/
COPY my.cnf /etc/mysql/conf.d/my.cnf

EXPOSE 3306

CMD ["mysqld"]