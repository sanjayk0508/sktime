"""Meta Transformers module

This module has meta-transformers that is build using the pre-existing
transformers as building blocks.
"""
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.compose import ColumnTransformer as skColumnTransformer
from sklearn.utils.validation import check_is_fitted

from sktime.transformers.base import BaseTransformer
from sktime.utils.data_container import concat_nested_arrays
from sktime.utils.data_container import tabularize, detabularize, get_time_index
from sktime.utils.validation.forecasting import check_is_fitted_in_transform
from sktime.utils.validation.supervised import validate_X

__author__ = ["Markus Löning", "Sajay Ganesh"]
__all__ = ['ColumnTransformer',
           'RowwiseTransformer',
           'Tabularizer',
           'Tabulariser',
           'ColumnConcatenator']


class ColumnTransformer(skColumnTransformer):
    """
    Applies transformers to columns of an array or pandas DataFrame. Simply takes the column transformer from sklearn
    and adds capability to handle pandas dataframe.

    This estimator allows different columns or column subsets of the input
    to be transformed separately and the features generated by each transformer
    will be concatenated to form a single feature space.
    This is useful for heterogeneous or columnar data, to combine several
    feature extraction mechanisms or transformations into a single transformer.

    Parameters
    ----------
    transformers : list of tuples
        List of (name, transformer, column(s)) tuples specifying the
        transformer objects to be applied to subsets of the data.
        name : string
            Like in Pipeline and FeatureUnion, this allows the transformer and
            its parameters to be set using ``set_params`` and searched in grid
            search.
        transformer : estimator or {'passthrough', 'drop'}
            Estimator must support `fit` and `transform`. Special-cased
            strings 'drop' and 'passthrough' are accepted as well, to
            indicate to drop the columns or to pass them through untransformed,
            respectively.
        column(s) : str or int, array-like of string or int, slice, boolean mask array or callable
            Indexes the data on its second axis. Integers are interpreted as
            positional columns, while strings can reference DataFrame columns
            by name.  A scalar string or int should be used where
            ``transformer`` expects X to be a 1d array-like (vector),
            otherwise a 2d array will be passed to the transformer.
            A callable is passed the input data `X` and can return any of the
            above.
    remainder : {'drop', 'passthrough'} or estimator, default 'drop'
        By default, only the specified columns in `transformers` are
        transformed and combined in the output, and the non-specified
        columns are dropped. (default of ``'drop'``).
        By specifying ``remainder='passthrough'``, all remaining columns that
        were not specified in `transformers` will be automatically passed
        through. This subset of columns is concatenated with the output of
        the transformers.
        By setting ``remainder`` to be an estimator, the remaining
        non-specified columns will use the ``remainder`` estimator. The
        estimator must support `fit` and `transform`.
    sparse_threshold : float, default = 0.3
        If the output of the different transfromers contains sparse matrices,
        these will be stacked as a sparse matrix if the overall density is
        lower than this value. Use ``sparse_threshold=0`` to always return
        dense.  When the transformed output consists of all dense data, the
        stacked result will be dense, and this keyword will be ignored.
    n_jobs : int or None, optional (default=None)
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
    transformer_weights : dict, optional
        Multiplicative weights for features per transformer. The output of the
        transformer is multiplied by these weights. Keys are transformer names,
        values the weights.
    preserve_dataframe : boolean
        If True, pandas dataframe is returned.
        If False, numpy array is returned.


    Attributes
    ----------
    transformers_ : list
        The collection of fitted transformers as tuples of
        (name, fitted_transformer, column). `fitted_transformer` can be an
        estimator, 'drop', or 'passthrough'. In case there were no columns
        selected, this will be the unfitted transformer.
        If there are remaining columns, the final element is a tuple of the
        form:
        ('remainder', transformer, remaining_columns) corresponding to the
        ``remainder`` parameter. If there are remaining columns, then
        ``len(transformers_)==len(transformers)+1``, otherwise
        ``len(transformers_)==len(transformers)``.
    named_transformers_ : Bunch object, a dictionary with attribute access
        Read-only attribute to access any transformer by given name.
        Keys are transformer names and values are the fitted transformer
        objects.
    sparse_output_ : bool
        Boolean flag indicating wether the output of ``transform`` is a
        sparse matrix or a dense numpy array, which depends on the output
        of the individual transformers and the `sparse_threshold` keyword.
    """

    def __init__(
            self,
            transformers,
            remainder="drop",
            sparse_threshold=0.3,
            n_jobs=1,
            transformer_weights=None,
            preserve_dataframe=True,
    ):

        self.preserve_dataframe = preserve_dataframe
        super(ColumnTransformer, self).__init__(
            transformers=transformers,
            remainder=remainder,
            sparse_threshold=sparse_threshold,
            n_jobs=n_jobs,
            transformer_weights=transformer_weights,
        )

    def _hstack(self, Xs):
        """
        Stacks X horizontally.

        Supports input types (X): list of numpy arrays, sparse arrays and DataFrames
        """
        types = set(type(X) for X in Xs)

        if self.sparse_output_:
            return sparse.hstack(Xs).tocsr()
        if self.preserve_dataframe and (pd.Series in types or pd.DataFrame in types):
            return pd.concat(Xs, axis="columns")
        return np.hstack(Xs)

    def _validate_output(self, result):
        """
        Ensure that the output of each transformer is 2D. Otherwise
        hstack can raise an error or produce incorrect results.

        Output can also be a pd.Series which is actually a 1D
        """
        names = [name for name, _, _, _ in self._iter(fitted=True,
                                                      replace_strings=True)]
        for Xs, name in zip(result, names):
            if not (getattr(Xs, 'ndim', 0) == 2 or isinstance(Xs, pd.Series)):
                raise ValueError(
                    "The output of the '{0}' transformer should be 2D (scipy " "matrix, array, or pandas DataFrame).".format(
                        name))


class RowwiseTransformer(BaseTransformer):
    """A convenience wrapper for row-wise transformers to apply transformation to all rows.

    This estimator allows to create a transformer that works on all rows from a passed transformer that works on a
    single row. This is useful for applying transformers to the time-series in the rows.

    Parameters
    ----------
    transformer : estimator
        An estimator that can work on a row (i.e. a univariate time-series in form of a numpy array or pandas Series.
        must support `fit` and `transform`
    """

    def __init__(self, transformer):
        self.transformer = transformer

    def fit(self, X, y=None):
        """
        Empty fit function that does nothing.

        Parameters
        ----------
        X : 1D array-like, pandas Series, shape (n_samples, 1)
            The training input samples. Shoould not be a DataFrame.
        y : None, as it is transformer on X

        Returns
        -------
        self : object
            Returns self.
        """
        validate_X(X)

        # fitting - this transformer needs no fitting
        self.is_fitted_ = True
        return self

    def transform(self, X):
        """
        Apply the `fit_transform()` method of the per-row transformer repeatedly
        on each row.

        Parameters
        ----------
        X : 1D array-like, pandas Series, shape (n_samples, 1)
            The training input samples. Shoould not be a DataFrame.

        Returns
        -------
        T : 1D array-like, pandas Series, shape (n_samples, ...)
            The transformed data
        """
        # check the validity of input

        validate_X(X)
        check_is_fitted(self, 'is_fitted_')

        # 1st attempt: try and exceptt, but sometimes breaks in other cases than excepted ValueError
        # Works on single column, but on multiple columns only if columns have equal-length series.
        # try:
        #     Xt = X.apply(self.transformer.fit_transform)
        #
        # # Otherwise call apply on each column separately.
        # except ValueError as e:
        #     if str(e) == 'arrays must all be same length':
        #         Xt = pd.concat([pd.Series(col.apply(self.transformer.fit_transform)) for _, col in X.items()], axis=1)
        #     else:
        #         raise

        # 2nd attempt: always iterate over columns, but column is not 2d and thus breaks if transformer expects 2d input
        # Xt = pd.concat([pd.Series(col.apply(self.transformer.fit_transform))
        #                 for _, col in X.items()], axis=1)

        # 3rd attempt: explicit for-loops, most robust but slow
        cols_t = []
        for c in range(X.shape[1]):  # loop over columns
            col = X.iloc[:, c]
            rows_t = []
            for row in col:  # loop over rows in each column
                row_2d = pd.DataFrame(row)  # convert into 2d dataframe
                row_t = self.transformer.fit_transform(row_2d)  # apply transform
                rows_t.append(row_t)  # append transformed rows
            cols_t.append(rows_t)  # append transformed columns

        # if series-to-series transform, flatten transformed series
        Xt = concat_nested_arrays(cols_t)  # concatenate transformed columns

        # tabularise/unnest series-to-primitive transforms
        xt = Xt.iloc[0, 0]
        if isinstance(xt, (pd.Series, np.ndarray)) and len(xt) == 1:
            Xt = tabularize(Xt)
        return Xt


class Tabularizer(BaseTransformer):
    """
    A transformer that turns time series/panel data into tabular data.

    This estimator converts nested pandas dataframe containing time-series/panel data with numpy arrays or pandas Series in
    dataframe cells into a tabular pandas dataframe with only primitives in cells. This is useful for transforming
    time-series/panel data into a format that is accepted by standard validation learning algorithms (as in sklearn).

    Parameters
    ----------
    check_input: bool, optional (default=True)
        When set to ``True``, inputs will be validated, otherwise inputs are assumed to be valid
        and no checks are performed. Use with caution.
    """

    # TODO: allow to keep column names, but unclear how to handle multivariate data

    def __init__(self, check_input=True):
        self.check_input = check_input

    def transform(self, X, y=None):
        """Transform nested pandas dataframe into tabular dataframe.

        Parameters
        ----------
        X : pandas DataFrame
            Nested dataframe with pandas series or numpy arrays in cells.
        y : array-like, optional (default=None)

        Returns
        -------
        Xt : pandas DataFrame
            Transformed dataframe with only primitives in cells.
        """

        if self.check_input:
            validate_X(X)

        self._columns = X.columns
        self._index = X.index
        self._time_index = get_time_index(X)

        Xt = tabularize(X)
        return Xt

    def inverse_transform(self, X, y=None):
        """Transform tabular pandas dataframe into nested dataframe.

        Parameters
        ----------
        X : pandas DataFrame
            Tabular dataframe with primitives in cells.
        y : array-like, optional (default=None)

        Returns
        -------
        Xt : pandas DataFrame
            Transformed dataframe with series in cells.
        """

        check_is_fitted_in_transform(self, '_time_index')

        # TODO check if for each column, all rows have equal-index series
        if self.check_input:
            validate_X(X)

        Xit = detabularize(X, index=self._index, time_index=self._time_index)
        return Xit


Tabulariser = Tabularizer


class ColumnConcatenator(BaseTransformer):
    """Transformer that concatenates multivariate time series/panel data into long univiariate time series/panel
        data by simply concatenating times series in time.
    """

    def transform(self, X, y=None):
        """Concatenate multivariate time series/panel data into long univiariate time series/panel
        data by simply concatenating times series in time.

        Parameters
        ----------
        X : nested pandas DataFrame of shape [n_samples, n_features]
            Nested dataframe with time-series in cells.

        Returns
        -------
        Xt : pandas DataFrame
          Transformed pandas DataFrame with same number of rows and single column
        """

        check_is_fitted(self, 'is_fitted_')

        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"Expected input is a pandas DataFrame, but found {type(X)}")

        Xt = detabularize(tabularize(X))
        return Xt
