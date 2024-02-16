from google.cloud import aiplatform
import kfp
from kfp.v2 import compiler
import numpy as np
from pipeline_definition import pipeline
from config import NOTEBOOK, DIR


try:
    compiler.Compiler().compile(
        pipeline_func = pipeline,
        package_path = f"{NOTEBOOK}.json"
    )
except Exception as e:
    print(f"An exception occurred while compiling pipeline definition json: {str(e)}")
    

