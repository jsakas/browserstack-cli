import os, http.client, base64, json, urllib


class BrowserStackAPIClient:
  def __init__(self):
    try:
      self.username, self.key = self.find_credentials()
    except Exception as e:
      print(e)
      exit()

    user_pass = '{}:{}'.format(self.username, self.key)
    auth_string = base64.b64encode(user_pass.encode())

    self.auth_headers = { 'Authorization' : 'Basic %s' %  auth_string.decode('ascii') }
    self.connection = http.client.HTTPSConnection('api.browserstack.com')

  def find_credentials(self):
    # look for environment variables first
    if os.environ.get('BROWSERSTACK_API_USERNAME') and os.environ.get('BROWSERSTACK_API_KEY'):
      return os.environ.get('BROWSERSTACK_API_USERNAME'), os.environ.get('BROWSERSTACK_API_KEY')

    # look for .browserstackrc, first in ~/
    try:
      f = open(os.path.join(os.path.expanduser('~'),'.browserstack.json'))
      credentials_object = json.loads(f.read())
      return credentials_object['username'], credentials_object['key']
    except Exception as e:
      pass

    # ...then in current working directory
    try:
      f = open(os.path.join(os.getcwd(),'.browserstack.json'))
      credentials_object = json.loads(f.read())
      return credentials_object['username'], credentials_object['key']
    except Exception as e:
      pass

    # if we made it this far, something is wrong
    raise Exception('BrowserStack credentials could not be found.')

  def wait(self):
    input('Waiting...')

  def launch_browser(self, payload, attach=False):
    self.connection.request('POST', '/4/worker', 
      urllib.parse.urlencode(payload), 
      headers=self.auth_headers
    )
    response = self.connection.getresponse()
    self.handle_api_response(response)

    results = response.read()
    if attach: self.wait()
    
    return results

  def get_worker(self, worker_id):
    endpoint = '/4/worker/{}'.format(worker_id)
    self.connection.request('GET', endpoint, headers=self.auth_headers)
    response = self.connection.getresponse()
    results = response.read()
    return results

  def kill_worker(self, worker_id):
    endpoint = '/4/worker/{}'.format(worker_id)
    self.connection.request('DELETE', endpoint, headers=self.auth_headers)
    response = self.connection.getresponse()
    results = response.read()
    return results

  def get_browsers(self, output_filter={}):
    self.connection.request('GET', '/4/browsers?flat=true', headers=self.auth_headers)
    response = self.connection.getresponse()
    results = response.read()
    self.print_table(json.loads(results.decode('utf-8')), output_filter)
    return results

  def handle_api_response(self, response):
    if response.code != 200:
      print('API returned a non 200 response code: {}'.format(response.code))
      print(response.read())
      exit()

  def print_table(self, data, row_filter={}):
    row_filter = dict(filter(lambda item: item[1] is not None, row_filter.items()))

    column_length = 20

    # table header
    print(''.join([column.ljust(column_length) for column in data[0].keys()]))
    print(''.join([''.ljust(column_length, '-') for column in data[0].keys()]))

    # table values
    for result in data:
      try:
        # filter out rows if there is a filter
        if row_filter:
          for f in row_filter.keys():
            if row_filter[f].lower() not in result[f].lower():
              raise Exception('Filtered row')

        row = [str(key).replace('None', '') for key in result.values()]
        print(''.join(column.ljust(column_length) for column in row))
      except Exception as e:
        continue
