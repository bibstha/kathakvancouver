# syntax=docker/dockerfile:1

# --- Build stage: render the Jekyll site to /site/_site ---
FROM ruby:4.0-slim AS build
WORKDIR /site

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential git && \
    rm -rf /var/lib/apt/lists/*

COPY Gemfile Gemfile.lock ./
RUN bundle config set --local path 'vendor/bundle' && \
    bundle install

COPY . .
RUN bundle exec jekyll build --destination /out

# --- Runtime stage: nginx serves static files ---
FROM nginx:alpine
COPY --from=build /out /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
