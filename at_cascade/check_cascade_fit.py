# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-21 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# -----------------------------------------------------------------------------
'''
{xsrst_begin check_cascade_fit}

Check the Cascade Results for a Node
####################################

Syntax
******
{xsrst_file
    # BEGIN syntax
    # END syntax
}

rate_true
*********
This argument can't be ``None`` and
is a function with the following syntax
```
rate = rate_true(rate_name, a, t, n, c)
```
The argument *rate_name* is one of the following:
:ref:`glossary.iota`,
:ref:`glossary.rho`,
:ref:`glossary.chi`, or
:ref:`glossary.omega`.
The argument *a* ( *t* ) is the age ( time ) at which we
are evaluating the rate.
The argument *n* is the :ref:`glossary.node_name` for the
node where we are evaluating the rate.
The argument *c* is a list of covariate values
in the same order as the covariate table.
The result *rate* is the corresponding value for the rate.

all_node_database
*****************
is a python string specifying the location of the
:ref:`all_node_db<all_node_db>`
relative to the current working directory.
This argument can't be ``None``.

fit_node_database
*****************
is a python string specifying the location of a
dismod_at database relative to the current working directory.
It is a :ref:`glossary.fit_node_database` with the
extra properties listed under
:ref:`dismod.db<cascade_fit_node.output_dismod_db>`
in the cascade_fit_node documentation.

{xsrst_end check_cascade_fit}
'''
# ----------------------------------------------------------------------------
import math
import dismod_at
import at_cascade
# ----------------------------------------------------------------------------
def table_name2id(tables, tbl_name, row_name) :
    col_name = f'{tbl_name}_name'
    for (row_id, row) in enumerate(tables[tbl_name]) :
        if row[col_name] == row_name :
            return row_id
    msg = f"Can't find {col_name} = {row_name} in table {tbl_name}"
    assert False, msg
# ----------------------------------------------------------------------------
def check_cascade_fit(
# BEGIN syntax
# at_cascade.check_cascade_fit(
            rate_true         = None,
            all_node_database = None,
            fit_node_database = None
# )
# END syntax
) :
    # connection
    new        = False
    connection = dismod_at.create_connection(all_node_database, new)
    #
    # all_cov_reference_table
    all_cov_reference_table = dismod_at.get_table_dict(
        connection, 'all_cov_reference'
    )
    connection.close()
    #
    # connection
    new        = False
    connection = dismod_at.create_connection(fit_node_database, new)
    #
    # tables
    tables = dict()
    for name in [
        'avgint',
        'age',
        'covariate',
        'time',
        'integrand',
        'node',
        'predict',
        'c_predict_fit_var',
    ] :
        tables[name] = dismod_at.get_table_dict(connection, name)
    connection.close()
    #
    # n_covariate n_avgint, n_predict, n_sample
    n_covariate = len(tables['covariate'])
    n_avgint    = len(tables['avgint'])
    n_predict   = len(tables['predict'])
    n_sample    = int( n_predict / n_avgint )
    #
    assert n_avgint == len( tables['c_predict_fit_var'] )
    assert n_predict % n_avgint == 0
    #
    # fit_node_id
    fit_node_name = at_cascade.get_parent_node( fit_node_database )
    fit_node_id   = table_name2id(tables, 'node', fit_node_name)
    #
    # cov_reference
    cov_reference_list = n_covariate * [ None ]
    for row in all_cov_reference_table :
        if row['node_id'] == fit_node_id :
            covariate_id = row['covariate_id']
            cov_reference_list[covariate_id] = row['reference']
    for reference in cov_reference_list :
        not reference is None
    #
    # rate_fun
    rate_fun = dict()
    rate_fun['iota'] = lambda a, t :  \
            rate_true('iota', a, t, fit_node_name, cov_reference_list)
    rate_fun['rho'] = lambda a, t :  \
            rate_true('rho', a, t, fit_node_name, cov_reference_list)
    rate_fun['chi'] = lambda a, t :  \
            rate_true('chi', a, t, fit_node_name, cov_reference_list)
    rate_fun['omega'] = lambda a, t :  \
            rate_true('omega', a, t, fit_node_name, cov_reference_list)
    #
    # sumsq
    sumsq = n_avgint * [0.0]
    #
    # predict_id, predict_row
    for (predict_id, predict_row) in enumerate( tables['predict'] ) :
        #
        # avgint_row
        avgint_id  = predict_row['avgint_id']
        avgint_row = tables['avgint'][avgint_id]
        assert avgint_id == predict_id % n_avgint
        #
        # sample_index
        sample_index = predict_row['sample_index']
        assert sample_index * n_avgint + avgint_id == predict_id
        #
        # integrand_name
        integrand_id = avgint_row['integrand_id']
        integrand_name = tables['integrand'][integrand_id]['integrand_name']
        #
        # node_name
        node_id   = avgint_row['node_id']
        node_name = tables['node'][node_id]['node_name']
        assert node_name == fit_node_name
        #
        # avg_integrand
        avg_integrand = tables['c_predict_fit_var'][avgint_id]['avg_integrand']
        #
        # sample_value
        sample_value = predict_row['avg_integrand']
        #
        # sumsq
        sumsq[avgint_id] += (sample_value - avg_integrand)**2
    #
    # avgint_id, row
    for (avgint_id, row) in enumerate(tables['c_predict_fit_var']) :
        assert avgint_id == row['avgint_id']
        #
        # avgint_row
        avgint_row = tables['avgint'][avgint_id]
        #
        # integrand_name
        integrand_id   = avgint_row['integrand_id']
        integrand_name = tables['integrand'][integrand_id]['integrand_name']
        #
        # age
        age = avgint_row['age_lower']
        assert age == avgint_row['age_upper']
        #
        # time
        time = avgint_row['time_lower']
        assert time == avgint_row['time_upper']
        #
        # avg_integrand
        avg_integrand = row['avg_integrand']
        #
        # sample_std
        sample_std = math.sqrt( sumsq[avgint_id] )
        #
        # check_value
        grid        = { 'age' : [age], 'time' : [time] }
        abs_tol     = 1e-6
        check_value = dismod_at.average_integrand(
            rate_fun, integrand_name, grid, abs_tol
        )
        #
        # check
        error       = check_value - avg_integrand
        rel_error   = 1.0 - avg_integrand / check_value
        # print(age, rel_error, error, sample_std)
        assert abs(rel_error) < 1e-1
        assert abs(error) < 2.0 * sample_std
