import pandas as pd


def fix_protected_attributes(dataset: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    for protected_attribute in sensitive_attributes:
            mean_protected_attribute = dataset[protected_attribute].mean()
            for index, row in dataset.iterrows():
                if row[protected_attribute] > mean_protected_attribute:
                    row[protected_attribute] = 1
                else:
                    row[protected_attribute] = 0
            
    return dataset

#def _return_unique_values_for_attribute(attribute, dataset: pd.DataFrame):
#        unique_values = []
#        for value in dataset[attribute].values:
#            if value not in unique_values:
#                unique_values.append(value)
#            else:
#                continue

#        return unique_values