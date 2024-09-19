# Semen Mokrov

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

from encapsulator import Encapsulator

# The sl was chosen as a standard of the industry
SIGNIFICANT_LEVEL = 0.05


# The function reduces datasets to the same length after their preprocessing for the correct operation of statistical tests
def make_datasets_same_length(user_dataset, expert_dataset):
    min_length = min(len(user_dataset), len(expert_dataset))

    return user_dataset[:min_length], expert_dataset[:min_length]


# The function is removing emissions from dataset by the interquartile range method
def emissions_removal(dataset):
    mean = np.mean(dataset)
    std = np.std(dataset)

    k = 2
    lower_bound = max(0, mean - k * std)
    upper_bound = mean + k * std

    return dataset[(dataset >= lower_bound) & (dataset <= upper_bound)]


# The function is normalizing the data
def normalize_data(dataset):
    return (dataset - np.min(dataset)) / (np.max(dataset) - np.min(dataset))


# Combined function
def prepare_dataset(dataset):
    normalized_dataset = normalize_data(dataset)
    cleared_data = emissions_removal(normalized_dataset)

    return cleared_data


# The function that calculate
def calculate_the_growth(user_dataset, expert_dataset):
    user_avg = user_dataset.mean()
    expert_avg = expert_dataset.mean()

    return (user_avg - expert_avg) / user_avg


# The function prove hypothesis H0: "The data is normally distributed"
# H1 then "The data is not normally distributed"
# I used Shapiro-Wilk’s W test for the proving
def check_normality(dataset):
    test, pvalue = stats.shapiro(dataset)

    print(f"The result of the p-value when checking the normality: {pvalue}")

    return pvalue >= SIGNIFICANT_LEVEL


# The function prove hypothesis H0: "The variances of the datasets are the same."
# H1 then "The variances of the datasets are different"
def check_variance_uniform(user_dataset, expert_dataset):
    test, pvalue = stats.levene(user_dataset, expert_dataset)

    print(f"The result of the p-value when checking the variance uniform: {pvalue}")

    return pvalue >= SIGNIFICANT_LEVEL


# In our case, data obtained from a single source can be considered paired
# We cannot use parameterized tests if the conditions are not met
# Within the framework of this function, we are trying to determine whether our hypothesis can be confirmed statistically adequately under current conditions
# The test "Wilcoxon signed-rank test" is used for that situation
def get_p_statistical_adequacy_non_parametrised(user_dataset, expert_dataset):
    # pvalue is one-sided, because the data is paired
    test, pvalue = stats.wilcoxon(user_dataset, expert_dataset, alternative="less")

    return pvalue


# The same function with t-test dependent that is used when we can fit to the parametrized conditions
def get_p_statistical_adequacy_parametrised(user_dataset, expert_dataset):
    test, pvalue = stats.ttest_rel(user_dataset, expert_dataset)

    print(f"The result of the p-value when checking the normal distribution: {pvalue}")

    # pvalue is one-sided, because the data is paired
    return pvalue / 2


def plot_the_distribution_density(user_dataset, expert_dataset):
    plt.figure(figsize=(8, 6))
    sns.kdeplot(user_dataset, label="Good user reviews", color="blue", fill=True)
    sns.kdeplot(expert_dataset, label="Good expert reviews", color="red", fill=True)

    plt.title('Distribution density')
    plt.legend()
    plt.show()


# When writing the code, I relied on the following article:
# https://towardsdatascience.com/hypothesis-testing-with-python-step-by-step-hands-on-tutorial-with-practical-examples-e805975ea96e
encapsulator = Encapsulator()

user_avg_box_office_dataset = prepare_dataset(encapsulator.get_user_reviews_box_office_dataset())
expert_avg_box_office_dataset = prepare_dataset(encapsulator.get_expert_reviews_box_office_dataset())

user_avg_box_office_dataset, expert_avg_box_office_dataset = make_datasets_same_length(user_avg_box_office_dataset,
                                                                                       expert_avg_box_office_dataset)

growth = calculate_the_growth(user_avg_box_office_dataset, expert_avg_box_office_dataset)

is_normal_distribution = check_normality(user_avg_box_office_dataset) and check_normality(expert_avg_box_office_dataset)

print(f"Both distributions are normal" if is_normal_distribution else "The distribution are not normal")

is_variance_uniform = check_variance_uniform(user_avg_box_office_dataset, expert_avg_box_office_dataset)

print(
    f"The variances of the distributions are approximately equal" if is_variance_uniform else "The variances of the distributions are different")

if is_normal_distribution and is_variance_uniform:
    result_p = get_p_statistical_adequacy_parametrised(user_avg_box_office_dataset,
                                                       expert_avg_box_office_dataset)
else:
    result_p = get_p_statistical_adequacy_non_parametrised(user_avg_box_office_dataset,
                                                           expert_avg_box_office_dataset)

print(f"Result p-value is {result_p}")

print(
    "The results of comparison the average of both datasets is applicable" if result_p >= SIGNIFICANT_LEVEL else "The results of comparison are not applicable")

plot_the_distribution_density(user_avg_box_office_dataset, expert_avg_box_office_dataset)
