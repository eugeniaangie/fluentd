# # fluentd/Dockerfile

# FROM fluent/fluentd:v1.12.0-debian-1.0
# USER root
# RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.0.3"]
# USER fluent


FROM fluent/fluentd:v1.12.0-debian-1.0

# Install dependencies and update Ruby
USER root
RUN gem uninstall -I elasticsearch && gem install elasticsearch -v 7.17.0
RUN apt-get update && apt-get install -y \
    sudo \
 && rm -rf /var/lib/apt/lists/* \
 && gem install faraday -v 2.8.1 \
  && gem install excon -v 0.109.0 \
 && gem install fluent-plugin-elasticsearch --no-document --version 5.0.3 \
#  && gem install rbenv

# Set up rbenv and install Ruby 3.0.0
# RUN rbenv init -
# RUN rbenv install 3.0.0
# RUN rbenv global 3.0.0

# Switch back to fluent user
USER fluent
