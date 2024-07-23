"""
This is the demo code that uses hydra to access the parameters in under the directory config.

Author: 
"""

import hydra
from hydra.core.config_store import ConfigStore
from config import OnlineRetailConfig

cs = ConfigStore.instance()
cs.store(name="online_retail_config", node=OnlineRetailConfig)

@hydra.main(version_base=None, config_path="../conf", config_name="config")
def process_data(config: OnlineRetailConfig) -> None:
    """Function to process the data"""

    print(f"Config data: {config}")


if __name__ == "__main__":
    process_data()