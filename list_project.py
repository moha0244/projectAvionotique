import dataProcessor.data_processor_page as data_processor_page
import xmlproject.xml_page as xml_page

PROJECTS = {
    "Analyseur de données": {
        "module": data_processor_page,
        "description": "Outil d'analyse et traitement des fichiers CSV de données avioniques",
        "icon": "",
        "tags": ["data", "csv"]
    },
    "️ Configuration TTC": {
        "module": xml_page,
        "description": "Générateur de fichiers XML pour la configuration des systèmes TTC",
        "icon": "",
        "tags": ["xml", "config"]
    }
}