# open-redact
resume redaction api

To run call
```
uvicorn app.main.main:app --reload
```

To install Spacy.io, reccomend you use en_core_web_sm well developing
```buildoutcfg
python -m spacy download en_core_web_trf
```

In dev environment you can view documentation at http://127.0.0.1:8000/docs#/