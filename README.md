# Prometheus Google Analytics Reporting API (V4) Exporter

Exposes a set of basic metrics from the Google Analytics Reporting API (V4), to a Prometheus compatible endpoint. 
*This is a very basic implementation, designed for a specific purpose. If you wish to extend/fork this repo to be something greater...  We are more than open to any pull requests / feedback*

## Configuration

This exporter is setup to take the following parameters from environment variables:
* `BIND_PORT` The port you wish to run the container on, defaults to 9173
* `START_DATE` The start date you wish to pass to the API, you can't deal with totals here so set it to before you began monitoring. Format: `YYYY-MM-DD`
* `ACCOUNT_EMAIL` The email address of the service account given access to the API
* `VIEW_ID` The 'view_id' that google assigns to your sites statistics

Account email and view ID need to be obtained from your google account details. Details on how can be found [here](https://developers.google.com/analytics/devguides/reporting/core/v4/) You also need to supply a PEM file with a key to access the API, details on this link above.

## Install and deploy

Run manually from Docker Hub:
```
docker run -d --restart=always -p 9171:9171 -e IMAGES="infinityworks/ranch-eye, infinityworks/prom-conf" infinityworks/github-exporter
```

Build a docker image:
```
docker build -t <image-name> .
docker run -d --restart=always -p 9171:9171 -e IMAGES="infinityworks/ranch-eye, infinityworks/prom-conf" <image-name>
```

## Docker compose

```
github-exporter:
    tty: true
    stdin_open: true
    expose:
      - 9171:9171
    image: infinityworks/github-exporter
```

## Metrics

Metrics will be made available on port 9171 by default

```
# HELP github_repo_subscribers subscribers
# TYPE github_repo_subscribers gauge
github_repo_subscribers{repo="docker-hub-exporter",user="infinityworksltd"} 1.0
github_repo_subscribers{repo="prometheus-rancher-exporter",user="infinityworksltd"} 2.0
# HELP github_repo_open_issues open_issues
# TYPE github_repo_open_issues gauge
github_repo_open_issues{repo="docker-hub-exporter",user="infinityworksltd"} 1.0
github_repo_open_issues{repo="prometheus-rancher-exporter",user="infinityworksltd"} 2.0
# HELP github_repo_watchers watchers
# TYPE github_repo_watchers gauge
github_repo_watchers{repo="docker-hub-exporter",user="infinityworksltd"} 1.0
github_repo_watchers{repo="prometheus-rancher-exporter",user="infinityworksltd"} 6.0
# HELP github_repo_stars stars
# TYPE github_repo_stars gauge
github_repo_stars{repo="docker-hub-exporter",user="infinityworksltd"} 1.0
github_repo_stars{repo="prometheus-rancher-exporter",user="infinityworksltd"} 6.0
# HELP github_repo_forks forks
# TYPE github_repo_forks gauge
github_repo_forks{repo="docker-hub-exporter",user="infinityworksltd"} 0.0
github_repo_forks{repo="prometheus-rancher-exporter",user="infinityworksltd"} 9.0
# HELP github_repo_has_issues has_issues
# TYPE github_repo_has_issues gauge
github_repo_has_issues{repo="docker-hub-exporter",user="infinityworksltd"} 1.0
github_repo_has_issues{repo="prometheus-rancher-exporter",user="infinityworksltd"} 1.0
```

## Metadata
[![](https://images.microbadger.com/badges/image/infinityworks/github-exporter.svg)](http://microbadger.com/images/infinityworks/github-exporter "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/infinityworks/github-exporter.svg)](http://microbadger.com/images/infinityworks/github-exporter "Get your own version badge on microbadger.com")
