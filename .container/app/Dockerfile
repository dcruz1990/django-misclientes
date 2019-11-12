FROM python:3.6

LABEL maintainer="Alain Sánchez <brazzisoft.com@gmail.com>" \
      company="BRAZZISOFT"  \
      project="MisClientes"

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1
ENV MC_USER mcuser
ENV MC_USER_UID 1000
ENV MC_GROUP mcgroup
ENV MC_GROUP_GID 1000
ENV APP_HOME /app
ENV SRC_HOME $APP_HOME/src
ENV VENV_HOME $APP_HOME/venv
ENV MEDIA_HOME $APP_HOME/media
ENV STATIC_HOME $APP_HOME/static
#ENV ROOTDIR /usr/local/
#WORKDIR $ROOTDIR/

#
# System Configuration
# .: 1. Install apt-utils package & Required Locales
RUN apt-get -qq update && \
    apt-get -qqy install  \
                          apt-utils \
                          locales  \
                          python-virtualenv \
                          build-essential \
                          gettext \
                          xvfb  && \
    rm -rf /var/lib/apt/lists/*

# .: 2. Configure Locales dynamically
COPY .container/app/locales /locales
RUN cat /locales >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=es_ES.UTF-8 && \
    echo "LANGUAGE=es_ES.UTF-8" >> /etc/default/locale && \
    echo "LC_ALL=es_ES.UTF-8" >> /etc/default/locale
RUN  rm /etc/localtime && echo "America/Havana" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata && \
    mkdir /tz && cp /etc/timezone /tz/ && cp /etc/localtime /tz/

# .: 3. Set environment variables for locales
ENV LC_ALL es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES.UTF-8

# .: 4. Create file system Add application user and group
RUN groupadd -r -g $MC_GROUP_GID $MC_GROUP && useradd -r -u $MC_USER_UID -d $APP_HOME -g $MC_GROUP $MC_USER
RUN mkdir -p $STATIC_HOME && mkdir -p $MEDIA_HOME && mkdir -p $SRC_HOME && mkdir -p $VENV_HOME
RUN chown -R $MC_USER:$MC_GROUP $STATIC_HOME $MEDIA_HOME $SRC_HOME $VENV_HOME

# .: 5. Set the workdir to the APP_HOME
WORKDIR $APP_HOME

# .: 6. Application Configuration
# 6.1. Define virtualenv environment
RUN virtualenv -p python $VENV_HOME
# 6.2. Copy requirements and install them
COPY ./requirements.txt $SRC_HOME
SHELL ["/bin/bash", "-c"]
RUN source $VENV_HOME/bin/activate && pip install -r $SRC_HOME/requirements.txt
# 6.3. Copy application
COPY . $SRC_HOME
# 6.4. Define environment variables
ENV DJANGO_SETTINGS_MODULE clients.settings
# 6.5. Making sure all the files/folders are owned by MC_USER
RUN chown -R $MC_USER:$MC_GROUP $APP_HOME $STATIC_HOME $MEDIA_HOME /tz

# .: 7. Setting up the docker entrypoint file
COPY ./.container/app/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh && chown $MC_USER:$MC_GROUP /docker-entrypoint.sh

# .: 8. Switch context to MC_USER
USER $MC_USER

# .: 9. Container Metadata definition
VOLUME ["$STATIC_HOME", "$MEDIA_HOME", "/tz"]

# .: 10. Invoking Default entrypoint
CMD ["/docker-entrypoint.sh"]
