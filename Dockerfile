FROM debian:latest


RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    python3-setuptools \
    python3-wheel \
    gnupg

RUN curl -sL https://deb.nodesource.com/setup_11.x | bash - \
    && apt-get install -y --no-install-recommends \
    nodejs \
    vim \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY . /var/www/pytatki

WORKDIR /var/www/pytatki

RUN pip3 install -r /var/www/pytatki/requirements/common.txt
RUN npm install && npm run build

COPY ./examples/apache.conf /etc/apache2/sites-available/pytatki.conf
RUN a2ensite pytatki
RUN a2enmod headers

COPY ./examples/pytatki.wsgi /var/www/pytatki/pytatki.wsgi

RUN a2dissite 000-default.conf
RUN a2ensite pytatki.conf

EXPOSE 80

WORKDIR /var/www/pytatki

CMD  /usr/sbin/apache2ctl -D FOREGROUND