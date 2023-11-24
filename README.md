#  :test_tube: Trajano Trade Algorithm
[![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)]()
[![GitHub commit activity the past week, 4 weeks](https://img.shields.io/github/commit-activity/y/eslint/eslint.svg?style=flat)]() [![GitHub commits since](https://img.shields.io/github/commits-since/tterb/playmusic/v1.2.0.svg)]() 

## Descripción

Este proyecto es un robot de trading automatizado para criptomonedas que implementa una estrategia predefinida. El bot está diseñado para ejecutar operaciones de compra y venta según las condiciones establecidas en la estrategia.Las estrategias se definirán dentro de un modulo específico y estas se basarán en modelos estadísticos-descriptivos y predictívos. 

## Características

- Implementación de una estrategia predefinida de trading.
- Soporte para múltiples exchanges de criptomonedas.
- Configuración flexible de parámetros y límites.
- Registro detallado de operaciones y resultados.

## Requisitos del Sistema

- Python 3.x
- Dependencias adicionales especificadas en `requirements.txt`

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/rubgarcia97/Trade-Algorithm.git
    ```

2. Instala las dependencias:

    ```bash
    cd Trade-Algorithm
    pip install -r requirements.txt
    ```

## Configuración

1. Configura tus credenciales de API para los exchanges en el archivo `config.yaml`.
2. Ajusta los parámetros de la estrategia en el archivo `strategy.yaml`.

## Uso

Ejecuta el bot con el siguiente comando:

```bash
python main.py
```
A continuación se abrirá una ventana gráfica donde se podrá inciar iniciar/detener la estrategia. El bot operará automáticamente según la estrategia predefinida.

## Contribución
Si deseas contribuir al desarrollo de este proyecto, sigue estos pasos:

    1. Haz un fork del repositorio.
    2. Crea una rama para tu contribución: git checkout -b feature/nueva-funcionalidad.
    3. Realiza tus cambios y haz commits: git commit -am 'Añade nueva funcionalidad'.
    4. Haz push a la rama: git push origin feature/nueva-funcionalidad.
    5. Abre un pull request en GitHub.

## Problemas y Sugerencias

Si encuentras algún problema o tienes sugerencias para mejorar el bot, por favor, abre un #issue.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
