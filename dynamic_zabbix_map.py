import json
import logging
from typing import List, Dict, Optional
from zabbix_utils import ZabbixAPI, APIRequestError

ZABBIX_URL = "http://demolab.imagunet.com/zabbix/api_jsonrpc.php"
ZABBIX_TOKEN = "A COLOCA TOKEN AQUI"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_json(path: str) -> List[Dict]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(f"Cargado archivo JSON: {path} con {len(data)} entradas.")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error cargando JSON {path}: {e}")
        raise

def resolve_hostid(api: ZabbixAPI, name: str) -> str:
    try:
        result = api.host.get(filter={'host': name}, output=['hostid'])
        if not result:
            raise ValueError(f"Host no encontrado: {name}")
        return result[0]['hostid']
    except APIRequestError as e:
        logger.error(f"Error buscando hostid para '{name}': {e}")
        raise

def get_mapid_by_name(api: ZabbixAPI, name: str) -> Optional[str]:
    try:
        result = api.map.get(filter={'name': name}, output=['sysmapid'])
        if result:
            logger.info(f"Mapa existente encontrado: '{name}' ID {result[0]['sysmapid']}")
            return result[0]['sysmapid']
    except APIRequestError as e:
        logger.error(f"Error buscando mapa '{name}': {e}")
        raise
    return None

def build_selements(api: ZabbixAPI, elements: List[Dict]) -> List[Dict]:
    selements = []
    for idx, elem in enumerate(elements, start=1):
        hostid = None
        if 'name' in elem:
            hostid = resolve_hostid(api, elem['name'])
        elif 'elementspecificid' in elem:
            hostid = elem['elementspecificid']
        else:
            logger.error(f"Elemento sin nombre ni elementspecificid: {elem}")
            raise ValueError("Elemento inválido")

        selement = {
            "selementid": str(idx),
            "elements": [{"hostid": hostid}],
            "elementtype": elem.get("elementtype", 0),
            "iconid_off": elem.get("iconid", 1),
            "x": elem.get("x", 0),
            "y": elem.get("y", 0)
        }
        selements.append(selement)
    return selements

def create_full_map(api: ZabbixAPI, name: str, width: int, height: int,
                    selements: List[Dict], links: Optional[List[Dict]] = None,
                    background: Optional[str] = None) -> str:
    params = {
        "name": name,
        "width": width,
        "height": height,
        "selements": selements
    }
    if links:
        params["links"] = links
    if background:
        params["backgroundid"] = background

    try:
        response = api.map.create(**params)
        mapid = response['sysmapids'][0]
        logger.info(f"Mapa creado '{name}' con ID {mapid}")
        return mapid
    except APIRequestError as e:
        logger.error(f"Error creando mapa completo: {e}")
        raise

def update_full_map(api: ZabbixAPI, mapid: str, width: int, height: int,
                    selements: List[Dict], links: Optional[List[Dict]] = None,
                    background: Optional[str] = None) -> str:
    params = {
        "sysmapid": str(mapid),
        "width": width,
        "height": height,
        "selements": selements
    }
    if links:
        params["links"] = links
    if background:
        params["backgroundid"] = background

    try:
        response = api.map.update(**params)
        mapid = response['sysmapids'][0]
        logger.info(f"Mapa actualizado ID {mapid}")
        return mapid
    except APIRequestError as e:
        logger.error(f"Error actualizando mapa: {e}")
        raise

def main():
    try:
        api = ZabbixAPI(url=ZABBIX_URL, token=ZABBIX_TOKEN, skip_version_check=True)
        logger.info("Autenticado en API Zabbix con token")

        map_name = "Mapa Dinámico de Arquitectura"
        width, height = 800, 600
        background_id = None

        elements_file = "elements.json"
        links_file = "links.json"

        elements = load_json(elements_file)
        if not elements:
            logger.error("No se encontraron elementos para agregar. Abortando.")
            return

        links = []
        try:
            links = load_json(links_file)
        except Exception:
            logger.warning("Archivo de enlaces no encontrado o inválido, se omitirá.")

        selements = build_selements(api, elements)
        mapid = get_mapid_by_name(api, map_name)

        if mapid is None:
            mapid = create_full_map(api, map_name, width, height, selements, links, background_id)
        else:
            mapid = update_full_map(api, mapid, width, height, selements, links, background_id)

        logger.info("Generación de mapa dinámico completada exitosamente.")

    except Exception as e:
        logger.critical(f"Error fatal durante la ejecución: {e}")

if __name__ == "__main__":
    main()
