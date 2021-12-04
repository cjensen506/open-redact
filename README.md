# open-redact

open-redact is an open source api to help anonymize pdf. This can be used can be used to redact names and other identifiable information from resume before review to create a more equitable hiring process.

Today open-redact supports the following redactions
*People's names
*email address

## Configuration
This package uses a spacy.io named entity recognition model. By default it is set to their en_core_web_lg model, but you can choose a smaller model to make development easier or a larger model for more performance. You can also select models for other languages. Check out https://spacy.io/models/en for English options.

2 places need to be edited to use a different model.
Inside the dockerfile the following line should be edited to install the model of your choice.
```dockerfile
RUN python -m spacy download en_core_web_lg
```

Inside app/main/sensitive_text_check.py the following line should be edited to install the model of your choice.
```python
nlp = spacy.load("en_core_web_lg")
```

## Installation

Clone from source and build an image using the included docker file

```bash
 docker build --tag openredact:python .
```
If not using image be sure manually install your named entity recognition model with the following
```bash
python -m spacy download en_core_web_lg
```

## Usage

When up and running the system auto generates swagger documentation which can be viewed at http://127.0.0.1:8000/docs#/ where the address and port should be updated for your deployment.


## Testing
From root run the following command to execute all unit tests
```bash
python -m pytest .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
