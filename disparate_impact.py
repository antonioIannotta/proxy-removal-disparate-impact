import pandas as pd

class DisparateImpact:

    # This method check the disparate impact for each sensitive attributes in the dataset and returns a dataframe in
    # which a column is the series of attributes and a column is the disparate impact value for each attribute
    def check(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        This method check the disparate impact for each sensitive attributes in the dataset and returns a dataframe in
        which a column is the series of attributes and a column is the disparate impact value for each attribute
        Args:
            dataset: pd.DataFrame

        Returns:
            pd.Dataframe
        """
        sensitive_attributes = self.return_sensitive_attributes(dataset)
        normalized_dataset = self.columns_normalization_max_min(dataset, sensitive_attributes)
        return self.return_disparate_impact(normalized_dataset, sensitive_attributes)

    # This method evaluates the fairness starting from the result of the check method.
    def fairness_evaluation(self, bias_analysis_dataframe: pd.DataFrame):
        return_value = 'unfair'
        for value in bias_analysis_dataframe['Disparate Impact'].values:
            if value < 0.80 or value > 1.25:
                return_value = 'unfair'
            else:
                return_value = 'fair'

        return return_value

    # This method returns the sensitive attributes into the dataframe.
    # (Only in this previous have been considered sensitive attributes the ones with only 2 possible values)
    def return_sensitive_attributes(self, dataset: pd.DataFrame):
        sensitive_attributes = []
        print(dataset.columns)
        for attr in dataset.columns[:len(dataset.columns) - 1]:
            unique_values = self.return_unique_values_for_attribute(attr, dataset)
            if len(unique_values) == 2:
                sensitive_attributes.append(attr)
            else:
                continue

        return sensitive_attributes

    # This method return the value that each attribute can have.
    def return_unique_values_for_attribute(self, attribute, dataset: pd.DataFrame):
        print(dataset)
        unique_values = []
        for value in dataset[attribute][1:].values:
            if value not in unique_values:
                unique_values.append(value)
            else:
                continue

        return unique_values

    # This method takes the sensitive attributes and returns a dataset in which the values of each sensitive attribute is
    # either 1 or 0
    def columns_normalization_max_min(self, dataset: pd.DataFrame, sensitive_attributes) -> pd.DataFrame:
        for attribute in sensitive_attributes:
            unique_values = self.return_unique_values_for_attribute(attribute, dataset)
            dataset[attribute].replace({max(unique_values): 1, min(unique_values): 0}, inplace=True)

        return dataset

    # This method return the dataframe (can be viewed as a report) of disparate impact
    def return_disparate_impact(self, dataset: pd.DataFrame, sensitive_attributes) -> pd.DataFrame:
        attribute_series = pd.Series(sensitive_attributes)
        disparate_impact_array = []
        for attribute in sensitive_attributes:
            unprivileged_probability = self.compute_disparate_impact(dataset, attribute, 0,
                                                                     dataset.columns[len(dataset.columns) - 1], 1)
            privileged_probability = self.compute_disparate_impact(dataset, attribute, 1,
                                                                   dataset.columns[len(dataset.columns) - 1], 1)
            disparate_impact = unprivileged_probability / privileged_probability
            disparate_impact_array.append(disparate_impact)

        disparate_impact_series = pd.Series(np.array(disparate_impact_array))
        disparate_impact_dataframe = pd.DataFrame(
            {"Attribute": attribute_series, "Disparate Impact": disparate_impact_series})
        return disparate_impact_dataframe

    # This method compute the disparate impact for a specific attribute
    def compute_disparate_impact(self, dataset: pd.DataFrame, attribute, attribute_value, output_column, output_value):
        attribute_columns_data = dataset[dataset[attribute] == attribute_value]
        return len(attribute_columns_data[attribute_columns_data[output_column] == output_value]) / len(
            attribute_columns_data)