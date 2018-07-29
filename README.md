# Currency API

[![Build Status](https://travis-ci.org/avara1986/currency-api.svg?branch=master)](https://travis-ci.org/avara1986/currency-api)
[![Coverage Status](https://coveralls.io/repos/github/avara1986/currency-api/badge.svg?branch=master)](https://coveralls.io/github/avara1986/currency-api?branch=master)
[![Requirements Status](https://requires.io/github/avara1986/currency-api/requirements.svg?branch=master)](https://requires.io/github/avara1986/currency-api/requirements/?branch=master)

# Instalación

    virtualenv -p python3.6 venv
    source venv/bin/activate
    pip install -r requirements-tests.txt
    python manage.py migrate
    python manage.py loaddata -e contenttypes fixtures.json
    
# Ejecutar el proyecto

Para que nuestro proyecto funcione contra Fixer.io se puede ejecutar con:
    
    python manage.py runserver

Para utilizar mocks:

    python manage.py runserver --settings=project.settings_test

# Arquitectura

La estructura y lógica del proyecto se ha hecho con las siguientes premisas:

- En cada entorno nunca existirá más de un proveedor a la vez
- Nuestro core de proveedor de divisas será agnóstico del gestor de base de datos y de la aplicación
- Añadir un nuevo proveedor implicará despliegue de código. Podría buscarse una solución para que en cualquier momento, desplegando la aplicación, se puede cambiar un proveedor por otro
- El job para recuperar los cambios de divisa se divide en la recuperación de los precios en tiempo real para recuperar los valores diarios y otro para recuperar el histórico de datos si en cualquier momento añadimos una nueva moneda en el proyecto y tenemos en cuenta que el proveedor no nos va a permitir hacer en un solo día las llamadas necesarias para traernos varios años.

## Problemas conocidos
- Como no se mencionaba y viendo otros portales, la divisa base se mantiene como constante en la configuración
  y se almacena en la BBDD. Si se quisiese que la divisa base fuese configurable por el usuario habría que refactorizar
- El versionado se ha planteado para modificar los datos de respuesta (en los serializers) si la aplicación cambiase de lógica
  con frecuencia puede que no sea la forma óptima de plantear el versionado

## Currency_providers
Core de la aplicación, aquí definiremos los origenes de datos.

## Swagger
Para consultar el swagger:

    http://localhost:8000/

## Login:

    curl -X POST -d "grant_type=password&username=prometeo&password=test1234" -u"lWFeJLhTlCUKyKBAE0c18lS2ON8EpxcTYppac3bW:DZMuYv5zSgRzeZ3VfGTuWzasBUqwcVvdEENQiw5QSH8v1Hq1q5lbkMNKB42YtzsQNANcWoGdcglo2aAVF9xmYHh3FudceoGiJUkjWjM3ZmbS08HL2PvN1vP09Stu3UgU" http://localhost:8000/o/token/


## Información de divisa

**Endpoint:** http://localhost:8000/v2/rates/

Parámetros:
 - start_date: fecha desde donde queremos recuperar los valores
 - end_date: fecha hasta donde queremos recuperar los valores
 - currency: divisa que queremos recuperar [OPCIONAL]

Ejemplo de llamada:

    curl -X GET "http://localhost:8000/v2/rates/?start_date=2017-05-01&end_date=2017-07-01&currency=EUR" -H 'Authorization: Bearer 9Loy1DQcYJxKQsdcfhdApYwZb46JB4' -H "accept: application/json" 

## Cambio de divisa

**Endpoint:** http://localhost:8000/v2/rates/exchange/

Ejemplo de datos que hay que enviarle:

    {
      "origin_currency": "EUR",
      "target_currency": "USD",
      "amount": 5,
      "date_invested": "2018-07-28"
    }

Ejemplo de llamada:

    curl -X POST "http://localhost:8000/v2/rates/exchange/" -H "Content-Type: application/json" -d "{ \"origin_currency\": \"EUR\", \"target_currency\": \"USD\", \"amount\": 5, \"date_invested\": \"2018-07-28\"}" -H 'Authorization: Bearer 9Loy1DQcYJxKQsdcfhdApYwZb46JB4'

## Time-Weighted Rate

**Endpoint:** http://localhost:8000/v2/rates/time_weighted_rate/

Ejemplo de datos que hay que enviarle:

    {
      "origin_currency": "EUR",
      "target_currency": "USD",
      "amount": 5,
      "date_invested": "2018-07-26"
    }

Ejemplo de llamada:

    curl -X POST "http://localhost:8000/v2/rates/time_weighted_rate/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"origin_currency\": \"EUR\", \"target_currency\": \"USD\", \"amount\": 5, \"date_invested\": \"2018-07-26\"}" -H 'Authorization: Bearer 9Loy1DQcYJxKQsdcfhdApYwZb46JB4'

## Backoffice

Nuestra gráfica de evolución de precios la podemos encontrar en:
    
    http://localhost:8000/v2/backoffice/

Que obtiene los datos de:

    http://localhost:8000/v2/rates/graph/?currency=EUR

# Job
    
Para recuperar un valor de una divisa en concreto:
    
    python manage.py retrive_rates EUR 2018-07-22 --settings=project.settings_test

Para generar X días hacia atrás con valores random una divisa en concreto:

    python manage.py generate_random_data CHF 10000 --settings=project.settings_test^

Estos se podrían pasar a un job de cron (o una lambda ;) )

0 8,15,20,23 * * *    {path_a_virtualenv}/venv/bin/python {path_a_proyecto}/manage.py generate_random_data CHF 10000 --settings=project.settings >> {mis_logs}/ingest.log


Create and push the image

    docker build -t templatedjango -f Dockerfile .

Test the image:

    docker run -d -p 8000:8000 templatedjango
    
    
Push to Kubernetes:

    kubectl create -f service.yaml
    
    
## How to contrib

TODO

### Update docs

   sphinx-build -b html docs/ _build