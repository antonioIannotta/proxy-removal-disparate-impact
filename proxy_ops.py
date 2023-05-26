import pandas as pd
from proxy_detection import return_proxy_variables

def return_proxy_protected_attribute_df(proxy_variables_df: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    """This method returns a dataframe containing the proxy variables for each sensitive attribute

    Args:
        proxy_variables_df (pd.DataFrame): _description_
        sensitive_attributes (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    sensitive_antecedent = []
    sensitive_consequent = []
    for index, proxy_row in proxy_variables_df.iterrows():
        for consequent in proxy_row['Consequent']:
            for sensitive_attribute in sensitive_attributes:
                if str(consequent).startswith(sensitive_attribute):
                    sensitive_antecedent.append(proxy_row['Antecedent'])
                    sensitive_consequent.append(consequent)

    dataframe = pd.DataFrame(
        {'Antecedent': pd.Series(sensitive_antecedent), 'Consequent': pd.Series(sensitive_consequent)})

    return dataframe


def proxy_fixing(original_dataset: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    """This method returns a dataset with proxy variables fixed in the original dataset

    Args:
        original_dataset (pd.DataFrame): _description_
        proxy_variables (pd.DataFrame): _description_
        sensitive_attributes (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    proxy_variables = return_proxy_variables(original_dataset, 0.8)
    dataset = original_dataset
    proxy_variables_for_sensitive_attributes = return_proxy_protected_attribute_df(proxy_variables,
                                                                                    sensitive_attributes)
    
    for index, row in proxy_variables_for_sensitive_attributes.iterrows():
        for antecedent in row['Antecedent']:
            consequent = row['Consequent']
                
            disparate_impact_value = _compute_disparate_impact_for_proxy(antecedent, consequent,
                                                                         original_dataset)
            if not 0.8 < disparate_impact_value < 1.25:
                dataset = _remove_proxy_from_dataset(original_dataset, antecedent)
                    
            else:
                continue

    return dataset


def _compute_disparate_impact_for_proxy(antecedent, consequent,
                                        original_dataset: pd.DataFrame) -> float:
    proxy = antecedent.split(' = ')[0]
    print(type(proxy))
    proxy_value = int(antecedent.split(' = ')[1])
    protected_column = consequent.split(' = ')[0]
    protected_value = int(consequent.split(' = ')[1])

    unprivileged_probability = _compute_disparate_impact(original_dataset, proxy, proxy_value, protected_column,
                                                         protected_value, False)
    privileged_probability = _compute_disparate_impact(original_dataset, proxy, proxy_value, protected_column,
                                                       protected_value, True)
    
    if unprivileged_probability == 0.0:
        return 0.0
    else:
        return unprivileged_probability / privileged_probability


def _compute_disparate_impact(dataset: pd.DataFrame, proxy, proxy_value, protected_column, protected_value,
                              privileged_group: bool) -> float:
    
    if privileged_group is True:
        proxy_columns_data = dataset[dataset[proxy] == proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)
    else:
        proxy_columns_data = dataset[dataset[proxy] != proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)


def _remove_proxy_from_dataset(original_dataset: pd.DataFrame, antecedent: str) -> pd.DataFrame:
    """This function removes the proxy columns from the original dataset

    Args:
        original_dataset (pd.DataFrame): _description_
        antecedent_row (pd.Series): _description_

    Returns:
        pd.DataFrame: _description_
    """
    dataset = original_dataset.drop(columns=[antecedent.split(' = ')[0]], axis=1, inplace=False)

    return dataset


def _proxy_format_to_column(row: pd.Series) -> list:
    """This function converts the information related to the proxy into the column name

    Args:
        row (pd.Series): _description_

    Returns:
        list: _description_
    """
    result = []
    for element in row:
        result.append(element.split(' = ')[0])

    return result


def _return_list_from_row(row: pd.Series):
    result = []
    if len(row) == 1:
        result.append(row)
    else:
        for element in row:
            result.append(element)

    return result
