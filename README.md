# Currency API

[![Build Status](https://travis-ci.org/avara1986/currency-api.svg?branch=master)](https://travis-ci.org/avara1986/currency-api)
[![Coverage Status](https://coveralls.io/repos/github/avara1986/currency-api/badge.svg?branch=master)](https://coveralls.io/github/avara1986/currency-api?branch=master)
[![Requirements Status](https://requires.io/github/avara1986/currency-api/requirements.svg?branch=master)](https://requires.io/github/avara1986/currency-api/requirements/?branch=master)

# Instalación

    virtualenv -p python3.6 venv
    source venv/bin/activate
    pip install -r requirements-tests.txt
    python manage.py migrate
    
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
- 
- Los access keys, contraseñas se definen por variables de entorno

## Currency_providers
Core de la aplicación, aquí definiremos los origenes de datos.

## Información de divisa

**Endpoint:** http://localhost:8000/rates/

Parámetros:
 - start_date: fecha desde donde queremos recuperar los valores
 - end_date: fecha hasta donde queremos recuperar los valores
 - currency: divisa que queremos recuperar [OPCIONAL]

Ejemplo de llamada:

    curl -X GET "http://localhost:8000/rates/?start_date=2017-05-01&end_date=2017-07-01&currency=EUR" -H "accept: application/json" 

## Cambio de divisa

**Endpoint:** http://localhost:8000/rates/exchange/

Ejemplo de datos que hay que enviarle:

    {
      "origin_currency": "EUR",
      "target_currency": "EUR",
      "amount": 5,
      "date_invested": "2018-07-28"
    }

Ejemplo de llamada:

    curl -X POST "http://localhost:8000/rates/exchange/" -H "Content-Type: application/json" -d "{ \"origin_currency\": \"EUR\", \"target_currency\": \"EUR\", \"amount\": 5, \"date_invested\": \"2018-07-28\"}"

## Backoffice
Nuestra gráfica de evolución de precios la podemos encontrar en:
    
    http://localhost:8000/backoffice/

Que obtiene los datos de:

    http://localhost:8000/rates/graph/?currency=EUR

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