---
title: Open Redact
emoji: 🔒
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# open-redact

open-redact is an open source api to help anonymize pdf. This can be used can be used to redact names and other identifiable information from resume before review to create a more equitable hiring process.

Today open-redact supports the following redactions
*People's names
*email address

## Configuration
This package uses [Microsoft Presidio](https://microsoft.github.io/presidio/) to detect personally identifiable information (PII). Presidio combines regex-based recognizers (for entities such as email addresses) with a spaCy named entity recognition model (for entities such as people's names).

By default the spaCy model is `en_core_web_lg`, pinned in `requirements.txt`. You can swap in a smaller model to make development easier, a larger model for more accuracy, or a model for another language. Check out https://spacy.io/models/en for English options.

To use a different model, update the pinned model in `requirements.txt` and configure Presidio's NLP engine accordingly (see the [Presidio customization docs](https://microsoft.github.io/presidio/analyzer/customizing_nlp_models/)). The default model is loaded automatically by the `AnalyzerEngine` in `app/main/sensitive_text_check.py`.

## Installation

Clone from source and build an image using the included docker file

```bash
 docker build --tag openredact:python .
```
If not using the image, install dependencies (including the spaCy model) with
```bash
pip install -r requirements.txt
```

## Usage

When up and running the system auto generates swagger documentation which can be viewed at http://127.0.0.1:8000/docs#/ where the address and port should be updated for your deployment.

![Screenshot of documentation](https://github.com/cjensen506/open-redact/blob/collateral/open_redact_docs.png)

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
