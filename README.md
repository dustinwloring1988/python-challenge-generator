# Python Challenge Generator

This Python script generates coding challenges using the GROQ API. It fetches challenges from the API, processes the data, and saves them to a YAML file. The challenges include a title, description, difficulty level, example usage, template code, solution, and test cases.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/dustinwloring1988/python-challenge-generator.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Set up your GROQ API key by creating a `.env` file in the project directory and adding the following line:

```
GROQ_API_KEY=YOUR_API_KEY_HERE
```

2. Run the Python script:

```bash
python main.py
```

3. Follow the prompts to generate coding challenges. You can specify the number of challenges to generate.

4. The generated challenges will be saved to a YAML file named `challenges.yaml` in the project directory.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```
