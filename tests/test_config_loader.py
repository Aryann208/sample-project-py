import unittest
import os
import json
import yaml
import tempfile
from modules.config_loader import ConfigLoader, load_config, get_environment_config


class TestConfigLoader(unittest.TestCase):
    """Test cases for the ConfigLoader module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_loader = ConfigLoader()
        
        # Create test JSON config file
        self.json_config = {
            "trading": {
                "strategy": "momentum",
                "timeframe": "1h",
                "risk_percentage": 2.0
            },
            "api": {
                "key": "test_key",
                "secret": "test_secret"
            }
        }
        self.json_path = os.path.join(self.temp_dir.name, "config.json")
        with open(self.json_path, 'w') as f:
            json.dump(self.json_config, f)
        
        # Create test YAML config file
        self.yaml_config = {
            "trading": {
                "strategy": "mean_reversion",
                "timeframe": "4h",
                "risk_percentage": 1.5
            },
            "api": {
                "key": "yaml_key",
                "secret": "yaml_secret"
            }
        }
        self.yaml_path = os.path.join(self.temp_dir.name, "config.yaml")
        with open(self.yaml_path, 'w') as f:
            yaml.dump(self.yaml_config, f)
        
        # Create environment-specific config
        self.env_config = {
            "trading": {
                "strategy": "production_strategy",
                "timeframe": "1d",
                "risk_percentage": 1.0
            },
            "api": {
                "key": "prod_key",
                "secret": "prod_secret"
            }
        }
        self.env_path = os.path.join(self.temp_dir.name, "config.production.yaml")
        with open(self.env_path, 'w') as f:
            yaml.dump(self.env_config, f)
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_load_json_config(self):
        """Test loading JSON configuration."""
        config = self.config_loader.load_file(self.json_path)
        self.assertEqual(config, self.json_config)
        self.assertEqual(config["trading"]["strategy"], "momentum")
        self.assertEqual(config["api"]["key"], "test_key")
    
    def test_load_yaml_config(self):
        """Test loading YAML configuration."""
        config = self.config_loader.load_file(self.yaml_path)
        self.assertEqual(config, self.yaml_config)
        self.assertEqual(config["trading"]["strategy"], "mean_reversion")
        self.assertEqual(config["api"]["key"], "yaml_key")
    
    def test_get_value(self):
        """Test getting specific values from configuration."""
        self.config_loader.load_file(self.json_path)
        self.assertEqual(self.config_loader.get_value("trading")["strategy"], "momentum")
        self.assertEqual(self.config_loader.get_value("non_existent", "default"), "default")
    
    def test_environment_config(self):
        """Test loading environment-specific configuration."""
        # Save current environment
        original_env = os.environ.get('ENV')
        
        try:
            os.environ['ENV'] = 'production'
            config = get_environment_config(self.temp_dir.name)
            self.assertEqual(config["trading"]["strategy"], "production_strategy")
            
            # Test with explicit environment
            config = get_environment_config(self.temp_dir.name, "production")
            self.assertEqual(config["trading"]["strategy"], "production_strategy")
            
            # Test fallback to default
            config = get_environment_config(self.temp_dir.name, "non_existent")
            self.assertNotEqual(config["trading"]["strategy"], "production_strategy")
        finally:
            # Restore original environment
            if original_env:
                os.environ['ENV'] = original_env
            else:
                if 'ENV' in os.environ:
                    del os.environ['ENV']
    
    def test_singleton_pattern(self):
        """Test that ConfigLoader follows the singleton pattern."""
        loader1 = ConfigLoader()
        loader2 = ConfigLoader()
        self.assertIs(loader1, loader2)
        
        # Ensure they share the same configuration
        loader1.load_file(self.json_path)
        self.assertEqual(loader2.get_value("trading")["strategy"], "momentum")
    
    def test_convenience_function(self):
        """Test the convenience function for loading config."""
        config = load_config(self.yaml_path)
        self.assertEqual(config["trading"]["strategy"], "mean_reversion")
    
    def test_file_not_found(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.config_loader.load_file("non_existent_file.json")
    
    def test_invalid_format(self):
        """Test handling of unsupported file formats."""
        invalid_path = os.path.join(self.temp_dir.name, "config.txt")
        with open(invalid_path, 'w') as f:
            f.write("This is not a valid config file")
        
        with self.assertRaises(ValueError):
            self.config_loader.load_file(invalid_path)
    
    def test_schema_validation(self):
        """Test schema validation."""
        # Define a schema for testing
        schema = {
            "type": "object",
            "required": ["trading", "api"],
            "properties": {
                "trading": {
                    "type": "object",
                    "required": ["strategy", "timeframe", "risk_percentage"],
                    "properties": {
                        "strategy": {"type": "string"},
                        "timeframe": {"type": "string"},
                        "risk_percentage": {"type": "number"}
                    }
                },
                "api": {
                    "type": "object",
                    "required": ["key", "secret"],
                    "properties": {
                        "key": {"type": "string"},
                        "secret": {"type": "string"}
                    }
                }
            }
        }
        
        # Valid configuration
        loader_with_schema = ConfigLoader(schema)
        config = loader_with_schema.load_file(self.json_path)
        self.assertEqual(config["trading"]["strategy"], "momentum")
        
        # Invalid configuration (missing required field)
        invalid_config = {
            "trading": {
                "strategy": "momentum"
                # Missing timeframe and risk_percentage
            },
            "api": {
                "key": "test_key",
                "secret": "test_secret"
            }
        }
        invalid_path = os.path.join(self.temp_dir.name, "invalid_config.json")
        with open(invalid_path, 'w') as f:
            json.dump(invalid_config, f)
            
        with self.assertRaises(ValueError):
            loader_with_schema.load_file(invalid_path)
    
    def test_invalid_json(self):
        """Test handling of malformed JSON."""
        invalid_json_path = os.path.join(self.temp_dir.name, "invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("{\"trading\": {\"strategy\": \"momentum\", invalid json")
        
        with self.assertRaises(ValueError):
            self.config_loader.load_file(invalid_json_path)
    
    def test_invalid_yaml(self):
        """Test handling of malformed YAML."""
        invalid_yaml_path = os.path.join(self.temp_dir.name, "invalid.yaml")
        with open(invalid_yaml_path, 'w') as f:
            f.write("trading:\n  strategy: momentum\n  timeframe: 1h\n  risk_percentage: invalid: yaml")
        
        with self.assertRaises(ValueError):
            self.config_loader.load_file(invalid_yaml_path)
    
    def test_merge_configs(self):
        """Test merging configurations."""
        base_config = {
            "trading": {
                "strategy": "momentum",
                "timeframe": "1h",
                "risk_percentage": 2.0
            },
            "api": {
                "key": "base_key",
                "secret": "base_secret"
            }
        }
        
        override_config = {
            "trading": {
                "strategy": "mean_reversion",
                "risk_percentage": 1.5
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        expected_result = {
            "trading": {
                "strategy": "mean_reversion",
                "timeframe": "1h",
                "risk_percentage": 1.5
            },
            "api": {
                "key": "base_key",
                "secret": "base_secret"
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        merged_config = self.config_loader.merge_configs(base_config, override_config)
        self.assertEqual(merged_config, expected_result)


if __name__ == '__main__':
    unittest.main()