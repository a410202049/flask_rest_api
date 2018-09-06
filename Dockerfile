FROM python:2.7

# ENV
ARG PROJ_FOLDER_NAME=eaccount-service
ARG PROJ_NAME=src
ENV SERVER_ID container
ENV SERVICE_ID $PROJ_NAME

# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python requirements.txt
ADD ./$PROJ_NAME/requirements.txt requirements.txt
RUN pip install --index-url http://plat_username:axf_plat@nexus.devops.axinfu.com/repository/pypi-all/simple --trusted-host nexus.devops.axinfu.com -r requirements.txt

# install software
RUN pip install uwsgi

# copy project files
COPY ./$PROJ_NAME /src

# create logs dir
RUN mkdir /var/log/micro-service/
RUN mkdir /var/log/eaccount-service/

WORKDIR /src

EXPOSE 80
CMD uwsgi --processes=1 -M --gevent=100 --http-socket :80 -w devel:app