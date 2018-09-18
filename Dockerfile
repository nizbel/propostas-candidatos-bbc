# Use an official Python runtime as a parent image
FROM python:2.7

COPY . /home/nizbel/propostas-candidatos-bbc

COPY settings_prod.py /home/nizbel/propostas-candidatos-bbc/presidenciaveis/settings.py

# Apagar arquivos de settings
RUN rm /home/nizbel/propostas-candidatos-bbc/settings_prod.py
RUN rm -rf /home/nizbel/propostas-candidatos-bbc/.hg

# Apagar arquivos pyc
RUN find /home/nizbel/propostas-candidatos-bbc -name "*.pyc" | xargs rm

WORKDIR /home/nizbel/propostas-candidatos-bbc

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Remover static
RUN rm -rf /home/nizbel/propostas-candidatos-bbc/static

EXPOSE 80

# Instalar apache
RUN apt-get update
RUN apt-get install -y apache2 apache2-utils libexpat1 ssl-cert && apt-get clean

RUN apt-get install -y libapache2-mod-wsgi

WORKDIR /home/nizbel/propostas-candidatos-bbc/apache-conf
RUN . /home/nizbel/propostas-candidatos-bbc/apache-conf/set-apache.sh

WORKDIR /home/nizbel/propostas-candidatos-bbc

# Remover pastas nao utilizadas
RUN rm -rf /home/nizbel/propostas-candidatos-bbc/apache-conf

RUN apt-get install nano

# Run app.py when the container launches
CMD apachectl -D FOREGROUND
