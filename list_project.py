import dataProcessor.data_processor_page as data_processor_page
import xmlproject.xml_page as xml_page

PROJECTS = {
    "Data Viewer": {
        "module": data_processor_page,
        "description": "Tool for analysis and processing of avionics CSV data files",
        "icon": "",
        "tags": ["data", "csv"]
    },
    "️TTC Configuration": {
        "module": xml_page,
        "description": "XML file generator for TTC system configuration",
        "icon": "",
        "tags": ["xml", "config"]
    }
}
