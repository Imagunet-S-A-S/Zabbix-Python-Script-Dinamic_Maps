<img src="images/Imagunet-Colombia.png" alt="Imagunet logo" width="200" style="margin-right: 20px;"/>

[![LinkedIn](https://img.shields.io/badge/linkedin-profile-blue?style=flat&logo=linkedin&labelColor=2d2d2d&color=0077b5)](https://www.linkedin.com/company/imagunet)

# Generador de Mapas Dinámicos para Zabbix

## Descripción

Este script está diseñado para interactuar con la API de Zabbix y crear o actualizar mapas dinámicos en Zabbix. Su propósito principal es generar y personalizar mapas basados en archivos JSON para elementos y enlaces. Estos mapas pueden ser parte de una visualización más amplia de la arquitectura de red dentro de la herramienta de monitoreo Zabbix.

### Autor: Giovanny Rodríguez  
### Empresa: Imagunet

## Funcionalidades

- Carga archivos JSON para elementos y enlaces del mapa.
- Resuelve los IDs de los hosts para cada elemento en la base de datos de Zabbix.
- Crea o actualiza mapas dinámicos en Zabbix.
- Permite definir el fondo, el ancho y la altura del mapa.
- Utiliza un sistema de logging para facilitar la depuración y seguimiento del proceso.

## Requisitos

- *Python*: Versión 3.9 o superior.
- *Zabbix API*: Se requiere el paquete zabbix-utils para interactuar con la API de Zabbix.
- *Dependencias*:
  - json
  - logging
  - typing
  - zabbix_utils

## Instalación

### Instalar dependencias

Asegúrate de tener instalada la versión 3.9 o superior de Python. Luego, instala las bibliotecas necesarias ejecutando el siguiente comando:

```bash
pip install zabbix-utils
