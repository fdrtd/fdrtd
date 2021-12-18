FROM python:latest
ENV exposePort=55500
EXPOSE ${exposePort}
RUN pip install fdrtd connexion[swagger-ui] fdrtd-simon==0.2.1
ENTRYPOINT python -m fdrtd.webserver --port=${exposePort}