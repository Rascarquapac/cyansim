import logging

# Configure the global logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='simulator.log',
					filemode='w')

logger = logging.getLogger('simulator')