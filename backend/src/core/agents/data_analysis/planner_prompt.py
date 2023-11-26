PLANNER_PROMPT = {}  # Need requirement, schema
PLANNER_PROMPT[
    "ANOVA"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will have several parts:

Here is the sample project plan if we want to do the ANOVA modeling on a sample dataset:

---

# Step 1: Data Cleaning and Summary

- Detail the data cleaning process, identifying missing values, outliers, and any anomalies in the dataset.
- Outline the generation of a data summary that includes descriptive statistics to understand the central tendency and dispersion.
- Plan to conduct exploratory data analysis (EDA), such as plotting distributions of variables and discovering patterns or relationships.

---

# Step 2: Checking ANOVA Assumptions

- Establish a checklist for the three main assumptions required for ANOVA: normality, homogeneity of variance, and independence.
- Describe the methods to test each assumption, such as Shapiro-Wilk test for normality, Levene's test for equal variances, and design or data collection techniques for independence.
- Plan for potential remedial actions if assumptions are not met, such as data transformation or using non-parametric tests.

---

# Step 3: ANOVA Model Fitting

- Define the process of fitting an ANOVA model to the dataset, including the selection of factors and levels to be tested.
- Describe the criteria for interpreting the ANOVA table results, focusing on F-statistic and p-values.
- Ensure the plan includes the determination of between-group and within-group variabilities.

---

# Step 4: Post Hoc Analysis

- Prepare a scheme for performing post hoc tests in case of a significant ANOVA result, to find out which groups differ.
- Decide on which post hoc test to use (e.g., Tukey, Bonferroni, Scheffé) depending on the study design and the data characteristics.
- Plan for the interpretation of the post hoc tests, understanding the pairwise comparisons and the adjustment for multiple comparisons.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Time Series"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a time series analysis.

Here is the sample project plan if we want to use SARIMA model to model the a sample data:

---

# Step 1: Exploratory Analysis

- Plot the train data.
- Note observations like increasing trend, seasonality, and variance.
- Use Box-Cox transformation to stabilize variance.

---

# Step 2: Model Preparation

- Analysis the seasonal effect and trend effect.
- Ensure time series is stationary by making lag 1 and lag 12 differences.
- Confirm stationarity with Augmented Dickey-Fuller Test.

---

# Step 3: Model Selection

- Examine sample ACF and PACF plots to determine model parameters.
- Use the determined parameters to select a range of candidate models.
- Calculate AICc for each candidate model.
- Choose the model with the smallest AICc as the best model.

---

# Step 4: Model Diagnostic:

- Check residuals of the model to ensure they resemble white noise.
- Validate normality using histogram, qqplot, and Shapiro-Wilks test.
- Confirm model residuals' independence using Box-Pierce, Ljung-Box, and McLeod-Li tests.
- Verify model is stationary and invertible by checking characteristic roots.

---

# Step 5: Forecasting

- Forecast electricity production for the years 1991 to 1995 using the selected SARIMA model.
- Plot the forecasts along with a 95 percentage confidence interval.
- Compare forecasted values with actual test data.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Regression"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a regression analysis.

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Causal Inference"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will have several parts:

Here is the sample project plan if we want to test the causality of a variable:

---

# Step 1: Identification of Variables

- Examine the data schema and project requirements to discern treatment and outcome variables.
- Define each identified variable clearly in the context of the study.
- Ensure variables are in line with the project's causal framework.

---

# Step 2: Control for Confounders

- Identify potential confounders that may influence both the treatment and outcome variables.
- Develop a plan to control for these confounders through statistical methods or study design.
- Justify the choice of methods for confounder control.

---

# Step 3: Selection of Causal Inference Method

- Review causal inference methods that align with the project's data and objectives.
- Choose a method and delineate the process for its implementation, ensuring adherence to its assumptions.
- Prepare to detail each step within the chosen method without the use of code.

---

# Step 4: Sensitivity Analysis

- Plan a sensitivity analysis to test the stability of the causal estimates against assumptions.
- Determine the range of variations for the analysis and the approach to interpret these results.
- Ensure the analysis can identify the conditions under which the causal estimate is valid.

---

# Step 5: Interpretation and Communication

- Layout the procedure for interpreting the calculated causal effect, considering its size, direction, and statistical significance.
- Craft a plan for the effective communication of these findings to both technical and non-technical stakeholders.
- Avoid technical jargon and focus on the implications of the causal relationship.

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""


PLANNER_PROMPT[
    "Non-Parametric"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will be structured into several parts

Here is the sample project plan if we want do a non parametric test for a dataset:

---

# Step 1: Test Selection

- Review the types of data and their distributions to determine the most suitable non-parametric test.
- Consider the sample size, number of samples, and whether the data are paired or independent.
- Document the decision process and justify the selection of the non-parametric test [e.g., data type, distribution].

---

# Step 2: Data Preparation

- Devise a plan for dealing with missing values, such as imputation or exclusion, and justify the chosen method.
- Outline procedures for identifying and handling outliers.
- Confirm that the data meets the assumptions for the chosen non-parametric test [e.g., independence of observations].

---

# Step 3: Test Execution

- Detail the steps to perform the selected non-parametric test without the use of statistical software code.
- Mention the specific test to be used [e.g., Mann-Whitney U test, Wilcoxon signed-rank test, Kruskal-Wallis H test] depending on the data configuration.
- Ensure the execution plan includes all necessary comparisons and groupings as per the project requirements.

---

# Step 4: Results Assessment

- Define the approach to assess the test results, with emphasis on significance levels and p-values.
- Include considerations for interpreting the rank sums or test statistics provided by the non-parametric test.
- Plan to evaluate the strength and direction of the observed effects.

---

# Step 5: Reporting Findings

- Create a blueprint for reporting the results that outlines how findings will be presented.
- Discuss the implications of the test outcomes in the context of the project requirement.
- Ensure the report is understandable and includes all relevant statistical terminology [e.g., significance level, test statistic].

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Dimension Reduction"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will be structured into several parts

Here is the sample project plan if we want do a dimension reduction for a dataset:

---

# Step 1

[Preparation for Dimension Reduction]
- Assess data types across the dataset to determine preprocessing needs.
- Develop a strategy for handling missing values with methods such as imputation or exclusion.
- Standardize or normalize features to ensure uniform scale, essential for many dimension reduction techniques.
- Identify potential issues like multicollinearity or high-dimensionality that could influence the reduction process and plan for ways to address them.

---

# Step 2

[Selection of Dimension Reduction Method]
- Evaluate different dimension reduction methods like PCA or t-SNE against the project requirements, considering the characteristics of the data.
- Determine the project's goals—whether to visualize data, improve computational efficiency, or reduce noise—and select the method that best aligns with these objectives.
- Balance the computational efficiency and the ability to maintain the quality of the information from the original dataset when choosing the method.

---

# Step 3

[Implementation of Dimension Reduction Technique]
- Plan the application of the selected technique to the preprocessed dataset.
- Describe the process to determine the optimal number of dimensions to retain, using methods such as explained variance or model performance.
- Ensure that the dimension reduction technique captures the significant structure of the data while minimizing information loss.

---

# Step 4

[Evaluation of Reduced Data]
- Establish metrics for evaluating the performance of the dimension reduction, such as the proportion of variance retained or reconstruction error.
- Interpret the reduced dimensions in terms of their contribution to variance and the insights they provide into the data structure.
- Formulate a plan for how to utilize the reduced data in future stages of the project, considering any adjustments that may be necessary based on the evaluation.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Linear Regression"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a linear regression analysis.

Here is the linear regression project plan if we want to use Multiple or Single Linear Regression model to model the a sample data:

---

# Step 1: Data Understanding and Preparation

- Load and explore the dataset to identify preliminary trends and relationships.
- Display the scatter plot between the response variable and the regressor. Also show the distribution of each variable. And use boxplot to check the outliers.
- Address missing values and prepare the data for modeling, ensuring it meets the requirements for a robust linear regression analysis.

---

# Step 2: Building the Linear Regression Model

- Establish an initial model, selecting appropriate predictor(s) and the response variable based on your topic.
- Assess the model's initial performance, identifying significant predictors and their corresponding coefficients.

---

# Step 3: Model Validation and Assumption Checking

- If applicable, refine the model using methods like stepwise regression or criterion-based selection for a multivariate approach.
- Usually use QQ plot, "residuals vs fitted value" plot and "residuals vs. leverage" plot to check of linear regression assumptions, ensuring linearity, independence, homoscedasticity, and normality of residuals.  Apply remedial measures if any violations are detected.

---

# Step 4: Diagnostics and Influential Observations

- Examine the model for issues like multicollinearity (in a multivariate context) and influential outliers that could skew results, using diagnostic measures and plots.
- Adjust the model as necessary to mitigate issues identified during diagnostics, enhancing its reliability and accuracy.
- Do not do any prediction

---

# Step 5: Model Interpretation and Predictions

- Clearly interpret the final model outcomes, explaining what the coefficients imply in a real-world context related to your topic.
- Discuss the model's predictive capabilities and how they can be practically applied in decision-making scenarios.
- Make sure use the press statistic to show the validate the predictive ability of the model.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Basic Chi-Square test"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will do basic chi-square test.

Here is the basic chi-square test if we want to use do basic chi-square test base on the data:

---

# Step 1: Data Understanding and Preparation

- Load and explore the dataset to identify preliminary trends and relationships.
- Display the scatter plot between the response variable and the regressor. Also show the distribution of each variable. And use boxplot to check the outliers.
- Address missing values and prepare the data for modeling, ensuring it meets the requirements for a robust linear regression analysis.

---

# Step 2: Formulate Hypotheses

- Define your null hypothesis (H0) and alternative hypothesis (Ha) specific to your t-test analysis:H0: There is no association between the two categorical variables (independence).Ha: There is an association between the two categorical variables.

---

# Step 3: Perform the Chi-Square Test (Do it by coding)

- Construct a contingency table of frequencies from your data.
- Calculate the expected frequencies for each cell of the table.
- Choose the appropriate chi-square test based on your data and assumptions (e.g., chi-square test of independence).
- Calculate the chi-square statistic, degrees of freedom, and the p-value.
- Discuss the practical implications of the observed association (or lack thereof) between the categories.
- Offer evidence-based recommendations or insights based on the chi-square results, especially concerning any potential causal relationships or predictive insights.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Basic t-test"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a basic t-test.

Here is the basic t-test project plan if we want to use basic t-test base on the sample data:

---

# Step 1: Data Understanding and Preparation

- Load and explore the dataset to identify preliminary trends and relationships.
- Display the scatter plot between the response variable and the regressor. Also show the distribution of each variable. And use boxplot to check the outliers.
- Address missing values and prepare the data for modeling, ensuring it meets the requirements for a robust linear regression analysis.

---

# Step 2: Formulate Hypotheses

- Define your null hypothesis (H0) and alternative hypothesis (Ha) specific to your t-test analysis:H0: There is no significant difference between the means of Group A and Group B.Ha: There is a significant difference between the means of Group A and Group B.

---

# Step 3: Perform the T-Test

- Choose the appropriate type of t-test based on your data and assumptions (e.g., independent samples t-test for comparing two separate groups).
- Calculate the t-statistic and degrees of freedom.
- Determine the critical t-value based on your chosen significance level (e.g., α = 0.05).
- Calculate the p-value associated with the t-statistic.
- Discuss the practical implications of the observed differences (or lack thereof) between the two groups.
- Offer evidence-based recommendations or insights based on the t-test results.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Logistic Regression"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

---

# Step 1: Data Understanding and Preparation

- Descriptive Statistics: Obtain measures such as mean, median, standard deviation, minimum, and maximum to provide insights into each variable's central tendency and variability. Remember, distincation continous variables and categorical variables. They should use different appropriate method.
- Categorical Data Handling:: Identify categorical variables in the dataset.Convert categorical variables into dummy variables or use other appropriate encoding methods. Ensure to avoid the dummy variable trap by dropping one level if necessary.Merge the encoded columns back into the dataset and drop the original categorical columns.
- Data Visualization: Utilize histograms to understand the distributions for all variables, scatter plots to observe bivariate relationships for continous variables, and boxplots for quartile analysis and outlier detection for continous variables.
- Missing Data Analysis: Address any missing values, considering techniques from simple listwise deletion to more advanced methods like multiple imputation.

---

# Step 2: Diagnostic

- Multicollinearity Check: Employ VIF or correlation matrices. If VIFs exceed 10, consider strategies to mitigate multicollinearity, such as removing variables or applying ridge regression.
- Logistic regression does not require a linear relationship between the dependent and independent variables.  Second, the error terms (residuals) do not need to be normally distributed.  Third, homoscedasticity is not required.  Finally, the dependent variable in logistic regression is not measured on an interval or ratio scale.

---

# Step 3: Model Fitting

- Logistic Regression Modeling: Apply logistic regression, specifying the response variable and predictors. Rely on maximum likelihood estimation (MLE) for coefficient predictions.
- Model Specification: Consider including interaction terms if hypothesized and ensure all first-order terms are present. Utilize likelihood ratio tests to compare models.
- Statistical Significance: Examine p-values and confidence intervals of each coefficient. Typically, a p-value below 0.05 suggests a significant relationship.

---

Step 4: Model Refinement and Validation
- Stepwise Regression: Balance model fit and complexity. Use AIC and BIC as guiding metrics. AIC & BIC Interpretation: Align with study objectives. If predictive accuracy is essential, lean towards AIC; for explanatory power, consider BIC.
- Model Diagnostics: Use the Hosmer-Lemeshow Test aiming for a p-value above 0.05.
- Residual Analysis: Examine residuals for randomness. Patterns could suggest model inadequacies or omitted variables.
- Influential Points: Identify observations with significant influence using DFBETAS and Cook's distance metrics.
---

# Step 5: Model Interpretation and Predictions

- Odds Ratio: Convert logistic regression coefficients to odds ratios, interpreting them within the data's context.
- Predictive Accuracy: Review the model's ability to forecast outcomes holistically.
- Model Performance Metrics: Evaluate using the ROC Curve, ensuring a balance between sensitivity and specificity.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Time Series ARIMA"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a time series.

Here is the linear regression project plan if we want to use timeseries arima model to do analysis

---

# Step 1: Exploratory Analysis

- Plot the original time series data of petroleum consumption.
- Observe the trends, seasonality, and variance in the data.
- Highlight the importance of making the data stationary for time series modeling.
- Apply various transformations like log, inverse, square root, inverse square root, and Box-Cox to stabilize the variance.
- Determine which transformation makes the data most stationary; in the provided report, the log transformation was found to be effective.


---

# Step 2: Model Preparation

- Analyze the seasonal and trend effects present in the data.
- Make the time series stationary by implementing transformations such as lag 1 and lag 12 differencing.
- Verify the stationarity of the time series using the Augmented Dickey-Fuller Test.


---

# Step 3:  Model Selection

- Analyze the Auto-Correlation Function (ACF) and Partial Auto-Correlation Function (PACF) plots to deduce potential model parameters.
- Based on the observed parameters, propose a set of candidate ARIMA models.
- Calculate the Akaike Information Criterion (AIC) for each model.
- Select the model with the smallest AIC as the best model for further analysis.


---

# Step 4:  Model Diagnostic

- Evaluate the residuals of the selected model to ensure they appear as white noise.
- Validate the normality of residuals using tools like histograms, Q-Q plots, and the Shapiro-Wilks test.
- Confirm the independence of the model residuals using tests such as Box-Pierce, Ljung-Box, and McLeod-Li.
- Ensure the model is both stationary and invertible by checking its characteristic roots.


---

#Step 5: Forecasting

- Use the finalized ARIMA model to forecast petroleum consumption for the desired future period.
- Visualize the forecasts and include a 95% confidence interval to understand the uncertainty associated with predictions.
- Compare the forecasted data with the actual data (if available) to gauge the model's accuracy.


---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Time Series SARIMA"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema: {data_schema}

My project will have several steps, and it will be a time series.

Here is the linear regression project plan if we want to use timeseries arima model to do analysis

---

# Step 1: Exploratory Analysis

- Plot the original time series data of petroleum consumption.
- Observe the trends, seasonality, and variance in the data.
- Highlight the importance of making the data stationary for time series modeling.
- Apply various transformations like log, inverse, square root, inverse square root, and Box-Cox to stabilize the variance.
- Determine which transformation makes the data most stationary; in the provided report, the log transformation was found to be effective.


---

# Step 2: Model Preparation

- Analyze the seasonal and trend effects present in the data.
- Make the time series stationary by implementing transformations such as lag 1 and lag 12 differencing.
- Verify the stationarity of the time series using the Augmented Dickey-Fuller Test.


---

# Step 3:  Model Selection

- Analyze the Auto-Correlation Function (ACF) and Partial Auto-Correlation Function (PACF) plots to deduce potential model parameters.
- Based on the observed parameters, propose a set of candidate ARIMA models.
- Calculate the Akaike Information Criterion (AIC) for each model.
- Select the model with the smallest AIC as the best model for further analysis.


---

# Step 4:  Model Diagnostic

- Evaluate the residuals of the selected model to ensure they appear as white noise.
- Validate the normality of residuals using tools like histograms, Q-Q plots, and the Shapiro-Wilks test.
- Confirm the independence of the model residuals using tests such as Box-Pierce, Ljung-Box, and McLeod-Li.
- Ensure the model is both stationary and invertible by checking its characteristic roots.


---

#Step 5: Forecasting

- Use the finalized ARIMA model to forecast petroleum consumption for the desired future period.
- Visualize the forecasts and include a 95% confidence interval to understand the uncertainty associated with predictions.
- Compare the forecasted data with the actual data (if available) to gauge the model's accuracy.


---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "One-Way ANOVA"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will have several steps.

Here is the sample one-way ANOVA project plan

---

# Step 1

[Data Preparation and Exploration]
- Inspect the data to ensure it fits the criteria for a One-Way ANOVA, focusing on one categorical independent variable and one continuous dependent variable.
- Handle any missing or outlier data points that could affect the ANOVA results, considering methods like imputation or removal.
- Perform exploratory data analysis to understand the distribution of the dependent variable within each group defined by the independent variable.

---

# Step 2

[Assumption Verification]
- Verify the assumptions of One-Way ANOVA, which are the independence of observations, homogeneity of variances (assessed by Levene's test or similar), and normality within groups (checked by Q-Q plots or normality tests).
- Plan remedial actions if any of the assumptions are not met, such as data transformation or the use of a non-parametric equivalent if the normality assumption is violated.

---

# Step 3

[ANOVA Model Fitting]
- Detail the process of fitting the ANOVA model, defining the null and alternative hypotheses.
- Include steps for calculating the F-statistic and corresponding p-value to assess the main effect of the categorical variable on the dependent variable.
- Ensure the documentation of the between-group and within-group variability for a thorough analysis.

---

# Step 4

[Post Hoc Testing and Interpretation]
- If the ANOVA indicates significant differences, plan for post hoc testing to determine which specific groups differ from each other.
- Choose appropriate post hoc tests (e.g., Tukey's HSD, Bonferroni correction) depending on the data and project requirements.
- Interpret the results, providing a clear understanding of the differences between group means and their relevance to the project objectives.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""

PLANNER_PROMPT[
    "Two-Way ANOVA"
] = """
Here is my project requirement: {project_requirement}

Here is my data schema:
{data_schema}

My project will have several steps.

Here is a sample plan for two-way ANOVA analysis on a sample dataset

---

# Step 1

[Data Preparation and Exploration]
- Validate that the dataset contains at least two categorical independent variables (factors) and one continuous dependent variable, suitable for Two-Way ANOVA.
- Tackle any missing values or outliers that may influence the analysis, choosing appropriate strategies to manage these data issues.
- Conduct exploratory data analysis to discern the distribution of the dependent variable across the levels of each factor and their interaction.

---

# Step 2

[Assumption Verification]
- Confirm the assumptions of Two-Way ANOVA, emphasizing the independence of observations, homogeneity of variances (which can be checked by Hartley's test), and the normality of the data within the groups (which can be assessed using Q-Q plots or statistical tests for normality).
- Plan for alternative approaches or data transformations if the assumptions are violated, which might include rank transformations or the adoption of a non-parametric approach.

---

# Step 3

[Model Fitting and Interaction Assessment]
- Elaborate on the procedure for fitting the Two-Way ANOVA model, including formulating the null hypotheses for main effects and interaction effects.
- Describe the process for computing the F-statistics for both the main and interaction effects and the interpretation of the resulting p-values.
- Emphasize the need to partition the variability into components attributable to each factor and their interaction.

---

# Step 4

[Post Hoc Analysis and Results Interpretation]
- Prepare for post hoc comparisons in case of significant main or interaction effects, selecting suitable multiple comparison procedures that adjust for familywise error rate, such as Tukey's test.
- Lay out the steps for interpreting the interaction plots and the main effects to understand the nature of the relationships between the variables.
- Contextualize the ANOVA findings within the project's framework, explaining the practical significance of the observed statistical effects.

---

Now you need to help me plan what's the specific plan of each part of the project. Please don't include any code, just the plan in text. Your output should be this format:

---

# Step i

plan for step i

---

Please only output the plan of each step.

"""
