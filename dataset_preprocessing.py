import pandas as pd


def fix_protected_attributes(dataset: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    for protected_attribute in sensitive_attributes:
        if _return_unique_values_for_attribute(protected_attribute, dataset) == 2:
            dataset[dataset[protected_attribute] == dataset[protected_attribute].max()] = 1
            dataset[dataset[protected_attribute] == dataset[protected_attribute].min()] = 0
        else:
            mean_protected_attribute = dataset[protected_attribute].mean()
            dataset[dataset[protected_attribute] >= mean_protected_attribute] = 1
            dataset[dataset[protected_attribute] < mean_protected_attribute] = 0
            
    return dataset

def _return_unique_values_for_attribute(self, attribute, dataset: pd.DataFrame):
        unique_values = []
        for value in dataset[attribute][1:].values:
            if value not in unique_values:
                unique_values.append(value)
            else:
                continue

        return unique_values