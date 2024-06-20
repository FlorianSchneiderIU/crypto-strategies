# Crypto Trading Strategies Demo

This project demonstrates different strategies for crypto trading. It includes separate strategy classes and a backtesting framework.

## Project Structure

```
crypto-trading-strategies-demo
├── strategies
├── utils
├── main.py
├── requirements.txt
└── README.md
```

## File Descriptions

- `strategies/*.py`: This file contains the implementation of a strategy class, which represents a strategy for crypto trading. It may have methods and properties specific to this strategy.

- `utils/common_utils.py`: This file contains utility functions that are commonly used across the project. It may contain functions for data processing, calculations, or any other utility functions required by the strategies or backtesting framework.

- `main.py`: This file is the entry point of the application. It may contain code to instantiate the strategies, configure the backtester, and run the backtesting process.

- `requirements.txt`: This file lists the dependencies required by the project. It specifies the Python packages and their versions that need to be installed for the project to run successfully.

## Usage

1. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```
2. Adjust the strategies to evaluate in `main.py`.
3. Run the backtesting process by executing the `main.py` file.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).