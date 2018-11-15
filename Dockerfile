FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip apache2 apache2-dev libapache2-mod-wsgi-py3
RUN pip3 install mod_wsgi
COPY . /pytatki
WORKDIR /pytatki
RUN cp examples/config.json .
RUN cp examples/pytatki.wsgi .
ADD examples/httpd.conf /etc/apache2/httpd.conf
ADD examples/apache.conf /etc/apache2/sites-enabled/000-default.conf
EXPOSE 80
CMD apachectl -D FOREGROUND
