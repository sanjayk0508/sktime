.. _glossary:

Glossary of Common Terms
========================

The glossary below defines common terms and API elements used throughout
sktime.

.. note::

    The glossary is under development. Important terms are still missing.
    Please create a pull request if you want to add one.


.. glossary::
    :sorted:

    Scitype
        See :term:`scientific type`.

    Scientific type
        A class or object type to denote a category of objects defined by a
        common interface and data scientific purpose. For example, "forecaster"
        or "classifier".

    Forecasting
        A learning task focused on prediction future values of a time series. For more details, see the :ref:`user_guide_introduction`.

    Time series
         Data where the :term:`variable` measurements are ordered over time or an index indicating the position of an observation in the sequence of values.

    Time series classification
        A learning task focused on using the patterns across instances between the time series and a categorical target variable.

    Time series regression
        A learning task focused on using the patterns across instances between the time series and a continuous target variable.

    Time series clustering
        A learning task focused on discovering groups consisting of instances with similar time series.

    Time series annotation
        A learning task focused on labeling the timepoints of a time series. This includes the related tasks of outlier detection, anomaly detection, change point detection and segmentation.

    Panel time series
        A form of time series data where the same time series are observed observed for multiple observational units. The observed series may consist of :term:`univariate time series` or
        :term:`multivariate time series`. Accordingly, the data varies across time, observational unit and series (i.e. variables).

    Univariate time series
        A single time series. While univariate analysis often only uses information contained in the series itself,
        univariate time series regression and forecasting can also include :term:`exogenous` data.

    Multivariate time series
        Multiple time series. Typically observed for the same observational unit. Multivariate time series
        is typically used to refer to cases where the series evolve together over time. This is related, but different than the cases where
        a :term:`univariate time series` is dependent on :term:`exogenous` data.

    Endogenous
        Within a learning task endogenous variables are determined by exogenous variables or past timepoints of the variable itself. Also referred to
        as the dependent variable or target.

    Exogenous
        Within a learning task exogenous variables are external factors whose pattern of impact on tasks' endogenous variables must be learned.
        Also referred to as independent variables or features.

    Reduction
        Reduction refers to decomposing a given learning task into simpler tasks that can be composed to create a solution to the original task.
        In sktime reduction is used to allow one learning task to be adapted as a solution for an alternative task.

    Variable
        Refers to some measurement of interest. Variables may be cross-sectional (e.g. time-invariant measurements like a patient's place of birth) or
        :term:`time series`.

    Timepoint
        The point in time that an observation is made. A time point may represent an exact point in time (a timestamp),
        a timeperiod (e.g. minutes, hours or days), or simply an index indicating the position of an observation in the sequence of values.

    Instance
        A member of the set of entities being studied and which an ML practitioner wishes to generalize. For example,
        patients, chemical process runs, machines, countries, etc. May also be referred to as samples, examples, observations or records
        depending on the discipline and context.

    Trend
        When data shows a long-term increase or decrease, this is referred to as a trend. Trends can also be non-linear.

    Seasonality
        When a :term:`time series` is affected by seasonal characteristics such as the time of year or the day of the week, it is called a seasonal pattern.
        The duration of a season is always fixed and known.

    Tabular
        Is a setting where each :term:`timepoint` of the :term:`univariate time series` being measured for each instance are treated as features and
        stored as a primitive data type in the DataFrame’s cells. E.g., there are N :term:`instances <instance>` of time series and each has T
        :term:`timepoints <timepoint>`, this would yield a pandas DataFrame with shape (N, T): N rows, T columns.

    Framework
        A collection of related and reusable software design templates that practitioners can copy and fill in.
        Frameworks emphasize design reuse.
        They capture common software design decisions within a given application domain and distill them into reusable design templates.
        This reduces the design decision they must take, allowing them to focus on application specifics.
        Not only can practitioners write software faster as a result, but applications will have a similar structure.
        Frameworks often offer additional functionality like :term:`toolboxes`.
        Compare with :term:`toolbox` and :term:`application`.

    Toolbox
        A collection of related and reusable functionality that practitioners can import to write applications.
        Toolboxes emphasize code reuse.
        Compare with :term:`framework` and :term:`application`.

    Application
        A single-purpose piece of code that practitioners write to solve a particular applied problem.
        Compare with :term:`toolbox` and :term:`framework`.

    Bagging: 
        A technique in ensemble learning where multiple models are trained on different subsets of the training data, with each 
        model having an equal vote in the final prediction.

    Cross-validation: 
        A technique used to estimate the performance of a predictive model. The data is split into multiple folds, with the 
        model trained on a subset of the folds and tested on the remaining fold. This process is repeated for all possible combinations of training and testing folds, and the performance metrics are averaged.

    Ensemble learning: 
        A technique in which multiple models are combined to improve the overall performance of a predictive model.

    Feature extraction: 
        A technique used to extract useful information from raw data. In time series analysis, this may involve transforming the 
        data to a frequency domain, decomposing the signal into components, or extracting statistical features.

    Generalization: 
        The ability of a predictive model to perform well on unseen data. A model that overfits to the training data may not 
        generalize well, while a model that underfits may not capture the underlying patterns in the data.

    Hyperparameter: 
        A parameter of a machine learning model that is set before training and affects the model's performance. Examples 
        include the learning rate in a neural network, the number of trees in a random forest, or the regularization parameter in a linear model.

    Model selection: 
        The process of selecting the best machine learning model for a given task. This may involve comparing the performance 
        of different models on a validation set, or using techniques like grid search to find the best hyperparameters for a given model.

    Resampling: 
        A technique used to address imbalanced datasets or to create more training data. Examples include oversampling, where 
        the minority class is oversampled to balance the class distribution, or bootstrap resampling, where multiple datasets are created by randomly sampling with replacement from the original data.

    Time series decomposition: 
        A technique used to separate a time series into its underlying components, such as trend, seasonality, and noise. 
        This can be useful for understanding the patterns in the data and for modeling each component separately.
