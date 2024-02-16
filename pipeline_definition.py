import kfp
from kfp.v2 import compiler
from google_cloud_pipeline_components.v1.dataset import TabularDatasetCreateOp
from google_cloud_pipeline_components.v1.automl.training_job import AutoMLTabularTrainingJobRunOp
from google_cloud_pipeline_components.v1.endpoint import EndpointCreateOp, ModelDeployOp
from config import NOTEBOOK, VERSION, URI

@kfp.dsl.pipeline(
    name = f'kfp-{NOTEBOOK}-{VERSION}',
    pipeline_root = URI+'/'+str(VERSION)+'/kfp/'
)
def pipeline(
    project: str,
    dataname: str,
    display_name: str,
    deploy_machine: str,
    bq_source: str,
    var_target: str,
    var_omit: str,
    features: dict,
    labels: dict,
    optimization_prediction_type: str,
    budget_milli_node_hours: int,
    optimization_objective: str
):
    
    # dataset
    dataset = TabularDatasetCreateOp(
        project = project,
        display_name = display_name,
        bq_source = bq_source,
        labels = labels
    )
    
    # training
    model = AutoMLTabularTrainingJobRunOp(
        project = project,
        display_name = display_name,
        optimization_prediction_type = optimization_prediction_type,
        optimization_objective = optimization_objective,
        budget_milli_node_hours = budget_milli_node_hours,
        disable_early_stopping=False,
        column_specs = features,
        dataset = dataset.outputs['dataset'],
        target_column = var_target,
        training_fraction_split = 0.8,
        validation_fraction_split = 0.1,
        test_fraction_split = 0.1,
        labels = labels
    )
    
    # Endpoint: Creation
    endpoint = EndpointCreateOp(
        project = project,
        display_name = display_name,
        labels = labels
    )
    
    # Endpoint: Deployment of Model
    deployment = ModelDeployOp(
        model = model.outputs["model"],
        endpoint = endpoint.outputs["endpoint"],
        dedicated_resources_min_replica_count = 1,
        dedicated_resources_max_replica_count = 1,
        traffic_split = {"0": 100},
        dedicated_resources_machine_type= deploy_machine
    )
