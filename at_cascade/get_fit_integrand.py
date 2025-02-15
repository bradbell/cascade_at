# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: University of Washington <https://www.washington.edu>
# SPDX-FileContributor: 2021-24 Bradley M. Bell
# ----------------------------------------------------------------------------
'''
{xrst_begin get_fit_integrand}

Determine the Set of Integrands in Data Table
#############################################

Prototype
*********
{xrst_literal ,
   # BEGIN_DEF, END_DEF
   # BEGIN_RETURN, END_RETURN
}

fit_or_root
***********
This :ref:`fit_or_root_class-name` object has open connections
for the node we are fitting.

fit_integrand
*************
The return value *fit_integrand* is a python set of integrand_id
that appear in the data table in the *fit_database*.
Furthermore there is a row in the data table
where each such integrand_id is not held out.

{xrst_end get_fit_integrand}
'''
# ----------------------------------------------------------------------------
import sys
import dismod_at
import at_cascade
# ----------------------------------------------------------------------------
#
# BEGIN_DEF
# at_cascade.get_fit_integrand
def get_fit_integrand(fit_or_root) :
   assert type(fit_or_root) == at_cascade.fit_or_root_class
   # END_DEF
   #
   # data_table
   data_table = fit_or_root.get_table('data')
   #
   # fit_integrand
   fit_integrand = set()
   for row in data_table :
      if row['hold_out'] == 0 :
         fit_integrand.add( row['integrand_id'] )
   #
   # BEGIN_RETURN
   # ...
   assert type(fit_integrand) == set
   return fit_integrand
   # END_RETURN
