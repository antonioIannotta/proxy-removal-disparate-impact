import pandas as pd

def return_proxy_protected_attribute_df(proxy_variables_df: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    """This method returns a dataframe containing the proxy variables for each sensitive attribute

    Args:
        proxy_variables_df (pd.DataFrame): _description_
        sensitive_attributes (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    sensitive_antecedent =  []
    sensitive_consequent = []
    for index, proxy_row in proxy_variables_df.iterrows():
        for consequent in proxy_row['Consequent']:
            for sensitive_attribute in sensitive_attributes:
                if sensitive_attribute in consequent:
                    sensitive_antecedent.append(proxy_row['Antecedent'])
                    sensitive_consequent.append(consequent)
    return pd.DataFrame({'Antecedent': pd.Series(sensitive_antecedent), 'Consequent': pd.Series(sensitive_consequent)})


def proxy_fixing(original_dataset: pd.DataFrame, proxy_variables: pd.DataFrame, sensitive_attributes: list) -> pd.DataFrame:
    """This method returns a dataset with proxy variables fixed in the original dataset

    Args:
        original_dataset (pd.DataFrame): _description_
        proxy_variables (pd.DataFrame): _description_
        sensitive_attributes (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    proxy_variables_for_sensitive_attributes = return_proxy_protected_attribute_df(proxy_variables, sensitive_attributes)
    for index, row in proxy_variables_for_sensitive_attributes.iterrows():
        disparate_impact_value = _compute_disparate_impact_for_proxy(row['Antecedent'], row['Consequent'], original_dataset)
        if 0.8 <= disparate_impact_value <= 1.25:
            original_dataset = _remove_proxy_from_dataset(original_dataset, row['Antecedent'])
        
        
def _compute_disparate_impact_for_proxy(antecedent_row: pd.Series, consequent_row: pd.Series, original_dataset: pd.DataFrame) -> float:
    pass


def _remove_proxy_from_dataset(original_dataset: pd.DataFrame, antecedent_row: pd.Series) -> pd.DataFrame:
    """This function removes the proxy columns from the original dataset

    Args:
        original_dataset (pd.DataFrame): _description_
        antecedent_row (pd.Series): _description_

    Returns:
        pd.DataFrame: _description_
    """
    columns = _proxy_format_to_column(antecedent_row)
    for column in columns:
        original_dataset.drop(column, axis=1, inplace=True)
        
    return original_dataset


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