REGION = 'us-central1'
NOTEBOOK = 'model3_notebook'
VERSION  = '05'
BQ_DATASET = 'model3'
BQ_TABLE = 'model3_training'
BUCKET = "aureus-bucket"
URI = f"gs://{BUCKET}/models/{NOTEBOOK}/{VERSION}"
DIR = f"temp/{NOTEBOOK}"
