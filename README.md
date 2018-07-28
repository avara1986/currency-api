# Currency API

[![Build Status](https://travis-ci.org/avara1986/currency-api.svg?branch=master)](https://travis-ci.org/avara1986/currency-api)
[![Coverage Status](https://coveralls.io/repos/github/avara1986/currency-api/badge.svg?branch=master)](https://coveralls.io/github/avara1986/currency-api?branch=master)
[![Requirements Status](https://requires.io/github/avara1986/currency-api/requirements.svg?branch=master)](https://requires.io/github/avara1986/currency-api/requirements/?branch=master)



# Arquitectura

La estructura y lógica del proyecto se ha hecho con las siguientes premisas:

- En cada entorno nunca existirá más de un proveedor a la vez
- Nuestro core de proveedor de divisas será agnóstico del gestor de base de datos y de la aplicación
- Añadir un nuevo proveedor implicará despliegue de código. Podría buscarse una solución que 
- En cualquier momento, desplegando la aplicación, se puede cambiar un proveedor por otro
- El job para recuperar los cambios de divisa se divide en la recuperación de los precios en tiempo real para recuperar los valores diarios y otro para recuperar el histórico de datos si en cualquier momento añadimos una nueva moneda en el proyecto y tenemos en cuenta que el proveedor no nos va a permitir hacer en un solo día las llamadas necesarias para traernos varios años.
- Los access keys, contraseñas se definen por variables de entorno
## Currency_providers
Core de la aplicación, aquí definiremos los origenes de datos.


# Job
    
    python manage.py retrive_rates EUR 2018-07-22 --settings=project.settings_test


    python manage.py retrive_rates EUR 2018-07-22 --settings=project.settings

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