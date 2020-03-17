from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import time, httplib2, os


class GarCollector(object):

  def collect(self):
    analytics = self._initialize_analyticsreporting()
    response = self._get_report(analytics)
    self._get_metrics(response)

    for metric in self._gauges:
      yield self._gauges[metric]

  def _initialize_analyticsreporting(self):
    
    credentials = ServiceAccountCredentials.from_p12_keyfile(
      SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())
    analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
    
    return analytics

  def _get_report(self, analytics):

    return analytics.reports().batchGet(
        body={
          'reportRequests': [
          {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': str(os.getenv('START_DATE')), 'endDate': 'today'}],
            'metrics': [{'expression': 'ga:sessions'}, {'expression': 'ga:pageviews'}, {'expression': 'ga:users'}, {'expression': 'ga:avgDomainLookupTime'}, {'expression': 'ga:avgPageDownloadTime'}, {'expression': 'ga:avgRedirectionTime'}, {'expression': 'ga:avgServerConnectionTime'}, {'expression': 'ga:avgServerResponseTime'}, {'expression': 'ga:avgPageLoadTime'}]
          }]
        }
    ).execute()

  def _get_metrics(self, response):
    METRIC_PREFIX = 'ga_reporting'
    LABELS = ['view_id', 'service_email']
    self._gauges = {}

    for report in response.get('reports', []):
      columnHeader = report.get('columnHeader', {})
      dimensionHeaders = columnHeader.get('dimensions', [])
      metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
      rows = report.get('data', {}).get('rows', [])

      for row in rows:
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
          print(header + ': ' + dimension)

        for i, values in enumerate(dateRangeValues):
          print('Date range (' + str(i) + ')')

          for metricHeader, returnValue in zip(metricHeaders, values.get('values')):
            metric = metricHeader.get('name')[3:]
            print(metric + ': ' + returnValue)
            self._gauges[metric] = GaugeMetricFamily('%s_%s' % (METRIC_PREFIX, metric), '%s' % metric, value=None, labels=LABELS)
            self._gauges[metric].add_metric([VIEW_ID, SERVICE_ACCOUNT_EMAIL], value=float(returnValue))


if __name__ == '__main__':
  SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
  DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
  KEY_FILE_LOCATION = './client_secrets.p12'
  SERVICE_ACCOUNT_EMAIL = str(os.getenv('ACCOUNT_EMAIL'))
  VIEW_ID = str(os.getenv('VIEW_ID'))

  start_http_server(int(os.getenv('BIND_PORT')))
  REGISTRY.register(GarCollector())
  
  while True: time.sleep(1)
