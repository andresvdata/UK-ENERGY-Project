# UK-ENERGY-Project
This repository contains the project implementation and analysis for a comprehensive study conducted by UK Power Networks, commissioned by the UK Government, to understand residential energy consumption in large cities, with a particular focus on London. The project aimed to gather data on energy production and consumption through smart meters installed in selected households in London.

The primary objective of this project was to gain insights into the dynamics and patterns of energy consumption in residential areas of London. By analyzing the collected data, the project aimed to identify the characteristics of current energy consumption in households, providing valuable information for the development of strategies and policies to facilitate the transition to clean energy sources.

The repository includes the codebase, data collection methodologies, data analysis techniques, and research findings. This comprehensive collection of resources serves as a valuable reference for researchers, policymakers, and other stakeholders interested in understanding and addressing residential energy consumption in urban areas, with a specific focus on London. The project's ultimate goal is to contribute to global efforts in achieving sustainable and environmentally friendly energy systems.

# Context

Energy is one of the main topics on the <b>UN agenda</b> for the following years, to assure global accessibility and reduce the related generation of pollution. According to the UN, energy currently provides 60% of the greenhouse gas emissions, although 13% of the global population has no access to electricity. For these reasons, countries like the UK are making eorts to create public policies focused on converting their current energy source to clean alternatives. To understand the dynamics of residential energy consumption in large cities, in 2014, the UK Government hired UK Power Networks for a project focused on collecting information about energy production and consumption through smart meters installed in a selected group of London households.

This information is useful to determine the current residential sector energy consumption charac- teristics. For UK Power Networks and the UK Government, it is important to know in detail the patterns of energy consumption in London's households, to create strategies to ease the transition to clean energy sources. ` This project is focused on providing relevant information to the public and private entities, such as the government of the United Kingdom, London authorities, energy suppliers, network operators, researchers, and in general players of the energy market about energy consumption patterns and demand trends of London households to allow them to make better decisions in eciently planning and operation of the electricity distribution networks, improving customer service and adopting of low carbon strategies. Last but not least, this study can be used as a guide for other countries that want to advance in the implementation of alternative energies.

# Datafolio
![image](https://github.com/andresvdata/UK-ENERGY-Project/blob/main/final%20Reports/SmartEnerx%20Datafolio%20-%20Team%2094.svg)

# Final Presentation

[![Final Presentation](https://img.youtube.com/vi/Nfx-dNObHsw/0.jpg)](https://www.youtube.com/watch?v=Nfx-dNObHsw)

# [Exploratory Data Analysis](notebooks/EDA/uk_energy.ipynb)
<b>[EDA](notebooks/EDA/uk_energy.ipynb)</b> was used to analyze and investigate data sets and summarize the main characteristics of this project, data visualization methods were employed .
# Modeling
The Prophet Forecasting model
Prophet is a time series forecasting model that is based on an additive model approach, where non-linear trends are fit with three main model components:  
* Growth (or trend) g(t)
* Seasonality s(t)
* Holidays h(t)
* Error term is included to represent any changes which are not accommodated by the model [^1]  

One can tune the trend and seasonality hyperparameters to fit the model as well as possible, changing its value using cross-validation. The forecasting is phrased as a curve-fitting task, with time as the only regressor, so the model is univariate.
These components are combined in the following equation:
```
y(t) = g(t) + s(t) + h(t) + 𝝐t
```
This formulation is similar to a `generalized additive model (GAM)`, a class of regression models with potentially non-linear smoothers applied to the regressors, that has the advantage of being flexible, accurate, fast to implement, and interpretable parameters[^2]. In this case, Prophet has some advantages compared to other time series models, such as its capacity to handle seasonal variations, missing data, and outliers.  
This model is an open-source tool provided by `Facebook Inc.` through the prophet package, available in `Python` and `R`

## ![Implementation Prophet Forecasting model](notebooks/Model/Prophet model Report.ipynb)
The modeling process can be divided into three main steps: data preparation, hyperparameter tuning and fitting of the model, and cross-validation and forecasting.  
In this case, the model was implemented using the aggregated daily energy consumption data and the national UK holidays data. For the hyperparameter tuning and the `cross-validation`, the dataset was automatically split into training and testing periods on a rolling basis, according to a defined train period and a forecasting horizon, which were established as 540 and 180 days. For that reason, the data used to perform the forecasting later will be included into the training set, since random samples cannot be used in time series.
Fitting the model is a very straightforward process but some key hyperparameters were adjusted to optimize the model performance. We perform an iterative process to select which of all the hyperparameters were most likely to be tuned by comparing the `MAPE` obtained by adjusting each individual hyperparameter  with a baseline MAPE with a standard fitted model. The most relevant hyperparameters were the type of trend, its flexibility or the seasonality and its strength, so its values were optimized using the grid search method.
After the hyperparameter tuning and the after cross-validation we obtained the best performing model, which exhibits a MAPE of 1.357%. This model was  used for the forecasting and the comparison with the other time series models.

## Prophet model by Category
For a more in-depth analysis, the same procedure was applied to the aggregated data by `ACORN
categories`, obtaining the corresponding metrics and forecast. This gave us insights of the behavior
that the daily energy consumption has across the distinct `ACORN groups` and its impact on the
performance of the model. Some of the fitted models are presented to compare their predicted values
to the observations
![image](https://github.com/user-attachments/assets/912035e1-04dc-4f80-a6bc-39be05651552)

| **Category**             | **MSE** | **MAE** | **MAPE** |
|--------------------------|---------|---------|----------|
| Comfortable Communities  | 0.45     | 0.17     | 1.90     |
| Rising Prosperity        | 1.4    | 0.31    | 3.02     |
| Affluent Achievers       | 2.48    | 0.45    | 3.01     |
| Financially Stretched    | 0.5    | 0.19    | 2.17     |
| Not Private Households   | 45.78    | 1.89    | 15.06    |
| Urban Adversity          | 0.15    | 0.10    | 1.41     |


Both metrics and the plots show us a generally good response of the model across the diferent
categories, with a `MAPE` in a range of 1% - 2.5%. However, in particular the `Not Private Households`
category shows a poor performance due to the high variation across the period, it makes harder to
take the accuracy of the predictions.
It's possible to see that the energy demand will increase in the upcoming years, and die to the
average energy growth demand will increase at the seasons stands approximately 4% (according to the
prophet model), compared with previous years and it won't be signifcantly diferent, so the number
of departments, categories and commercial growth over the median will be more.  

Finally, computing the variable's importance for doing the classification in the model, we identifed
that the most important variables were: season, and population. We'd like to clarify that all the
information was summarized just to have a general overview and take to most of the performance out
of the model, to clear the bigger picture, and to stay tuned with the changes. It was also summed up
to prevent the model to be over fitted.

# [Final Report](final Reports/Analysis of residential energy consumption in London.pdf)

The final report presented in the project was the ![following link](https://github.com/andresvdata/UK-ENERGY-Project/blob/main/final%20Reports/Analysis%20of%20residential%20energy%20consumption%20in%20London.pdf)

## ![Dashboard](final Reports/Dashboard User Guide.pdf)
The final presentation involved the creation of a Dashboard using Dash
![image](https://github.com/user-attachments/assets/ed6967cb-71ac-4475-8b63-7291a7984ef1)
### Features
* Interactive Visualizations: Users can interact with various charts and graphs to gain insights into energy data.
* Data Exploration: Users can filter and explore different datasets related to energy consumption, generation, and emissions.
* User-Friendly Interface: Designed with an intuitive user interface for easy navigation.
### Technologies Used
* **Python:** The main programming language for the backend.
* **Dash:** A web framework for building interactive web applications in Python.
* **Pandas:** For data manipulation and analysis.
* **Plotly:** For creating interactive visualizations.
### Code Structure
* app.py: The main application file that initializes the dashboard and defines the layout and callbacks.
* data/: Directory containing datasets used for visualizations.
* assets/: Directory for CSS and JS files for custom styling and functionality.

# Additional Files
[Guide for user to use the final Dashboard](final Reports/Dashboard User Guide.pdf)
