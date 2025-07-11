import logging
from typing import Dict, Any
from datetime import datetime
from modules.data_loader import load_data
from modules.trading_logic import TradingLogic
from modules.config_loader import load_config
from modules.dataframe_transformer import transform_dataframes

def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_system(config: Dict[str, Any]) -> None:
    """Initialize system based on configuration."""
    logging.info("Initializing system...")
    # Add any additional initialization steps here

def run_trading_system(config: Dict[str, Any]) -> None:
    """Main function to run the trading system."""
    try:
        # Load data
        df = load_data(config['data_file'])
        df2 = load_data(config['secondary_data_file']) if 'secondary_data_file' in config else None

        # Initialize trading logic
        trading_logic = TradingLogic(config['symbol'])

        # Run the trading simulation
        start_time = datetime.now()
        logging.info(f"Starting trading simulation at {start_time}")
        
        trades = trading_logic.masterframe(df, df2)
        
        end_time = datetime.now()
        logging.info(f"Finished trading simulation at {end_time}")
        logging.info(f"Total execution time: {end_time - start_time}")

        # Process and log results
        total_trades = len(trades)
        total_pnl = sum(trade['pnl'] for trade in trades if 'pnl' in trade)
        win_rate = sum(1 for trade in trades if 'pnl' in trade and trade['pnl'] > 0) / total_trades if total_trades > 0 else 0

        logging.info(f"Total trades: {total_trades}")
        logging.info(f"Total P&L: {total_pnl:.2f}")
        logging.info(f"Win rate: {win_rate:.2%}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    # Set up logging
    setup_logging()

    try:
        # Load configuration
        config = load_config('config.yaml')

        # Initialize system
        initialize_system(config)

        # Run trading system
        run_trading_system(config)

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        exit(1)

    logging.info("Trading system execution completed successfully.")