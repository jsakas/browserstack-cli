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
      f = open(os.path.join(os.path.expanduser('~'),'.browserstackrc'))
      credentials_object = json.loads(f.read())
      return credentials_object['username'], credentials_object['key']
    except Exception as e:
      pass

    # ...then in current working directory
    try:
      f = open(os.path.join(os.getcwd(),'.browserstackrc'))
      credentials_object = json.loads(f.read())
      return credentials_object['username'], credentials_object['key']
    except Exception as e:
      pass

    # if we made it this far, something is wrong
    raise Exception('BrowserStack credentials could not be found.')

  def wait(self):
    input('Waiting...')

  def launch_browser(self, payload):
    self.connection.request('POST', '/4/worker', 
      urllib.parse.urlencode(payload), 
      headers=self.auth_headers
    )
    response = self.connection.getresponse()
    results = response.read()

    if self.attach: self.wait()
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

  def get_browsers(self):
    self.connection.request('GET', '/4/browsers?flat=true', headers=self.auth_headers)
    response = self.connection.getresponse()
    results = response.read()

    # TODO - the following is just quick and dirty way to print a table, this should be refactored
    #
    # first print the keys
    column_length = 20
    for key in json.loads(results.decode('utf-8'))[0]:
      print(key.ljust(column_length), end='')
    print('')

    for key in json.loads(results.decode('utf-8'))[0]:
      print(''.ljust(column_length -1, '-').ljust(column_length, ' '), end='')
    print('')
    
    # then print the values
    for result in json.loads(results.decode('utf-8')):
      for key in result:
        value = result.get(key, '')
        if not value:
          value = ''
        print(value.ljust(column_length), end='')
      print('')
    print('')

    return results

