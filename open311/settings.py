import os.path

SERVICE_DISCOVERY_FILE= os.path.join(os.path.dirname(__file__),'api_endpoints.yaml').replace('\\', '/')

DATABASE_URI="postgresql+psycopg2://diptanuc@localhost/open311"