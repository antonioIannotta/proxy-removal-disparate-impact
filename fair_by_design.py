import pandas as pd
from dataset_preprocessing import *
from disparate_impact import DisparateImpact
from proxy_detection import *
from proxy_ops import *

def compute(dataset: pd.DataFrame, protected_attributes: list, confidence_threshold: float) -> pd.DataFrame:
    dataset = fix_protected_attributes(dataset, protected_attributes)
    while DisparateImpact().fairness_evaluation(dataset, protected_attributes) == 'fair':
        proxy_variables = return_proxy_variables(dataset, confidence_threshold)
        dataset = proxy_fixing(dataset, proxy_variables, protected_attributes)
        
    return dataset