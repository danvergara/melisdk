# melisdk (MercadoLibre's Python SDK)

This is not the official Python SDK for MercadoLibre's Platform, but works. And you cant install it from PYPI.

[![PyPI version](https://badge.fury.io/py/melisdk.svg)](https://badge.fury.io/py/melisdk)

## How do I install it?

```
$ pip3 install melisdk
```

from the source

```
$ git clone https://github.com/dany2691/melisdk.git
$ cd melisdk
$ python3 setup.py install
```

## How do I use it?

The first thing to do is to instance a ```Meli``` class. You'll need to give a ```clientId``` and a ```clientSecret```. You can obtain both after creating your own application. For more information on this please read: [creating an application](http://developers.mercadolibre.com/application-manager/)

### Including the Lib
Include the lib meli in your project

### Attention
Don't forget to set the authentication URL of your country in file lib/config.ini

```python
from melisdk import Meli
```
Start the development!

### Create an instance of Meli class
Simple like this
```python
meli = Meli(client_id=1234, client_secret="a secret")
```
With this instance you can start working on MercadoLibre's APIs.

There are some design considerations worth to mention.

1. This SDK is just a thin layer on top of an http client to handle all the OAuth WebServer flow for you.

2. There is JSON parsing. this SDK will include [json](http://docs.python.org/2/library/json.html) for internal usage.

3. If you already have the access_token and the refresh_token you can pass in the constructor

```python
meli = Meli(client_id=1234, client_secret="a secret", access_token="Access_Token", refresh_token="Refresh_Token")
```

## How do I redirect users to authorize my application?

This is a 2 step process.

First get the link to redirect the user. This is very easy! Just:

```python
redirectUrl = meli.auth_url(redirect_URI="http://somecallbackurl")
```

This will give you the url to redirect the user. You need to specify a callback url which will be the one that the user will redirected after a successfull authrization process.

Once the user is redirected to your callback url, you'll receive in the query string, a parameter named ```code```. You'll need this for the second part of the process.

```python
meli.authorize(code="the received code", redirect_URI="http://somecallbackurl")
```

This will get an ```access_token``` and a ```refresh_token``` (is case your application has the ```offline_access```) for your application and your user.

At this stage your are ready to make call to the API on behalf of the user.

#### Making GET calls

```python
params = {'access_token' : meli.access_token}
response = meli.get(path="/users/me", params=params)
```

#### Making POST calls

```python
params = {'access_token' : meli.access_token}

  #this body will be converted into json for you
body = {'foo'  : 'bar', 'bar' : 'foo'}

response = meli.post(path="/items", body=body, params=params)
```

#### Making PUT calls

```python
params = {'access_token' : meli.access_token}

  #this body will be converted into json for you
body = {'foo'  : 'bar', 'bar' : 'foo'}

response = meli.put(path="/items/123", body=body, params=params)
```

#### Making DELETE calls
```python
params = {'access_token' : meli.access_token}
response = meli.delete(path="/questions/123", params=params)
```

## I want to contribute!

That is great! Just fork the project in github. Create a topic branch, write some code, and add some tests for your new code.

Thanks for helping!

# Development setup

This project uses _pipenv_ for dependecy resolution. It's a kind of mix between
pip and virtualenv. Follow the next instructions to setup the development enviroment.

```sh
$ git clone https://github.com/dany2691/melisdk.git
$ cd melisdk
$ pipenv shell
$ pip3 install -e .
```

To run the test-suite, inside the melisdk directory:

```shell
$ python -m unittest -vv tests/test_meli.py
```

## Meta

Daniel Omar Vergara Pérez – [@dan1_net](https://twitter.com/dan1_net) – daniel.omar.vergara@gmail.com

[https://github.com/dany2691](https://github.com/dany2691)

## Contributing

1. Fork it (<https://gitlab.com/hexagondata_projects/melisdk>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
