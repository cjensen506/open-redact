# open-redact

open-redact is an open source api to help anonymize pdf. This can be used can be used to redact names and other identifiable information from resume before review to create a more equitable hiring process. 

## Installation

Clone from source and build an image using the included docker file

```bash
 docker build --tag openredact:python .
```

## Usage

When up and running the system auto generates swagger documentation which can be viewed at http://127.0.0.1:8000/docs#/ where the address and port should be updated for your deployment.


## Testing

```bash
python -m pytest .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)