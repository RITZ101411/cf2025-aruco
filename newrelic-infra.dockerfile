FROM newrelic/infrastructure:latest
COPY ./newrelic-infra.yml /etc/newrelic-infra.yml
COPY ./nginx-config.yml /etc/newrelic-infra/integrations.d/nginx-config.yml
COPY ./logging.yml /etc/newrelic-infra/logging.d/logging.yml