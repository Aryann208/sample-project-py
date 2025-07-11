import json
import yaml
import os
import logging
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError

class ConfigLoader:
    """
    Singleton class for loading and managing configuration from JSON or YAML files.
    Supports environment-specific configurations and schema validation.
    """
    _instance = None
    _config = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, schema: Optional[Dict[str, Any]] = None):
        """
        Initialize the ConfigLoader with an optional schema for validation.
        
        Args:
            schema (Optional[Dict[str, Any]]): JSON schema for configuration validation
        """
        if self._initialized:
            return
            
        self.schema = schema
        self.logger = logging.getLogger(__name__)
        self._initialized = True
    
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load configuration from a file (JSON or YAML).
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dict containing the configuration
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported or parsing fails
        """
        if not os.path.exists(file_path):
            self.logger.error(f"Configuration file not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.json':
                with open(file_path, 'r') as file:
                    config = json.load(file)
            elif file_extension in ['.yaml', '.yml']:
                with open(file_path, 'r') as file:
                    config = yaml.safe_load(file)
            else:
                self.logger.error(f"Unsupported file format: {file_extension}")
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            self._config = config
            
            # Validate configuration if schema is provided
            if self.schema:
                self._validate_config(config)
                
            return config
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            self.logger.error(f"Error parsing configuration file: {str(e)}")
            raise ValueError(f"Error parsing configuration file: {str(e)}")

    def get_config(self) -> Dict[str, Any]:
        """
        Get the loaded configuration.
        
        Returns:
            Dict containing the configuration
        """
        return self._config

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific value from the configuration.
        
        Args:
            key: The key to look up
            default: Default value to return if key is not found
            
        Returns:
            The value for the key or the default value
        """
        return self._config.get(key, default)

    def load_environment_config(self, base_path: str, environment: str) -> Dict[str, Any]:
        """
        Load environment-specific configuration.
        
        Args:
            base_path: Base directory for configuration files
            environment: Environment name (e.g., 'development', 'production')
            
        Returns:
            Dict containing the environment-specific configuration
        """
        # First try to load environment-specific config
        env_file = os.path.join(base_path, f"config.{environment}.json")
        if os.path.exists(env_file):
            return self.load_file(env_file)
            
        env_file = os.path.join(base_path, f"config.{environment}.yaml")
        if os.path.exists(env_file):
            return self.load_file(env_file)
            
        env_file = os.path.join(base_path, f"config.{environment}.yml")
        if os.path.exists(env_file):
            return self.load_file(env_file)
            
        # Fall back to default config
        default_files = [
            os.path.join(base_path, "config.json"),
            os.path.join(base_path, "config.yaml"),
            os.path.join(base_path, "config.yml")
        ]
        
        for file_path in default_files:
            if os.path.exists(file_path):
                return self.load_file(file_path)
                
        raise FileNotFoundError(f"No configuration file found in {base_path}")

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate the loaded configuration against the schema.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If the configuration doesn't match the schema
        """
        try:
            validate(instance=config, schema=self.schema)
            self.logger.info("Configuration validation successful")
        except ValidationError as e:
            self.logger.error(f"Configuration validation error: {str(e)}")
            raise ValueError(f"Configuration validation error: {str(e)}")

    def merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries, with override_config taking precedence.
        
        Args:
            base_config: Base configuration dictionary
            override_config: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        result = base_config.copy()
        
        for key, value in override_config.items():
            # If both values are dictionaries, merge them recursively
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result


def load_config(file_path: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to load configuration from a file.
    
    Args:
        file_path: Path to the configuration file
        schema: JSON schema for configuration validation
        
    Returns:
        Dict containing the configuration
    """
    loader = ConfigLoader(schema)
    return loader.load_file(file_path)


def get_environment_config(base_path: str, environment: str = None, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Load environment-specific configuration.
    
    Args:
        base_path: Base directory for configuration files
        environment: Environment name, defaults to value from ENV environment variable
        schema: JSON schema for configuration validation
        
    Returns:
        Dict containing the environment-specific configuration
    """
    if environment is None:
        
        
        
        environment = os.environ.get('ENV', 'development')
    
    loader = ConfigLoader(schema)
    return loader.load_environment_config(base_path, environment)