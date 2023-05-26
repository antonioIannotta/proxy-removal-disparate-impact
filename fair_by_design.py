import pandas as pd
from dataset_preprocessing import *
from disparate_impact import DisparateImpact
from proxy_detection import *
from proxy_ops import *

def compute(dataset: pd.DataFrame, protected_attributes: list, confidence_threshold: float) -> pd.DataFrame:
    dataset = fix_protected_attributes(dataset, protected_attributes)
    while DisparateImpact().fairness_evaluation(dataset, protected_attributes) == 'unfair':
        dataset = proxy_fixing(dataset, protected_attributes)
        print(dataset)
        
    return dataset