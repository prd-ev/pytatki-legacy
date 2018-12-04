FROM pniedzwiedzinski/flask-react


COPY ./requirements/common.txt /home/
COPY ./package.json /var/www/pytatki/
RUN pip3 install -r /home/common.txt
WORKDIR /var/www/pytatki
RUN npm install


COPY ./examples/apache.conf /etc/apache2/sites-available/pytatki.conf
RUN mkdir /etc/apache2/sites-enabled/ && \
    ln -s /etc/apache2/sites-available/pytatki.conf /etc/apache2/sites-enabled/pytatki.conf

RUN ln -sf /dev/stdout /var/log/apache2/access.log && \
    ln -sf /dev/stderr /var/log/apache2/error.log

#ln -s /etc/apache2/mods-available/headers.conf /etc/apache2/mods-enabled/headers.conf
COPY ./examples/pytatki.wsgi /var/www/pytatki/pytatki.wsgi

RUN ln -s  /var/run /run

COPY . /var/www/pytatki

RUN  npm run build

EXPOSE 80

WORKDIR /var/www/pytatki

CMD  exec /usr/sbin/httpd -D FOREGROUND