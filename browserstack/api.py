import os, http.client, base64, json, urllib


class BrowserStackAPIClient:

  def __init__(self):
    print('BrowserStackAPIClient() constructed')

    self.username = os.environ.get('BROWSERSTACK_API_USERNAME')
    self.key = os.environ.get('BROWSERSTACK_API_KEY')

    userAndPass = '{}:{}'.format(self.username, self.key)
    authString = base64.b64encode(userAndPass.encode())

    self.auth_headers = { 'Authorization' : 'Basic %s' %  authString.decode('ascii') }
    self.connection = http.client.HTTPSConnection('api.browserstack.com')


  def launch_browser(self, payload):
    self.connection.request('POST', '/4/worker', 
      urllib.parse.urlencode(payload), 
      headers=self.auth_headers
    )

    response = self.connection.getresponse()
    results = response.read()
    results = json.loads(results.decode('utf-8'))
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
    for key in json.loads(results.decode('utf-8'))[0]:
      print(key.ljust(30), end='')
    print('')
    
    # then print the values
    for result in json.loads(results.decode('utf-8')):
      for key in result:
        value = result.get(key, '')
        if not value:
          value = ''
        print(value.ljust(30), end='')
      print('')

    return results

