# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-21 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# -----------------------------------------------------------------------------
import os
import csv
import at_cascade.ihme
#
# -----------------------------------------------------------------------------
#
# write_node_tables()
# all_mtall_table_file, mtall_index_table_file, omega_age_table_file,
# omega_time_table_file.
def write_mtall_tables() :
    #
    # global constants
    age_group_inp_file      = at_cascade.ihme.age_group_inp_file
    mtall_inp_file          = at_cascade.ihme.mtall_inp_file
    all_mtall_table_file    = at_cascade.ihme.all_mtall_table_file
    mtall_index_table_file  = at_cascade.ihme.mtall_index_table_file
    omega_age_table_file    = at_cascade.ihme.omega_age_table_file
    omega_time_table_file   = at_cascade.ihme.omega_time_table_file
    sex_info_dict           = at_cascade.ihme.sex_info_dict
    #
    # output_file_list
    output_file_list = [
        all_mtall_table_file,
        mtall_index_table_file,
        omega_age_table_file,
        omega_time_table_file,
    ]
    #
    # done
    done = True
    for file in output_file_list :
        done = done and os.path.exists(file)
    if done :
        print( f'Using existing mtall_tables:')
        for file in output_file_list :
            print( file )
        return
    else :
        print( f'Createing mtall_tables:')
        for file in output_file_list :
            print( file )
    #
    # age_group_id_set, age_group_id_dict
    age_group_id_table = at_cascade.ihme.get_age_group_id_table()
    age_group_id_set   = set()
    age_group_id_dict  = dict()
    for row in age_group_id_table :
        age_group_id = row[ 'age_group_id' ]
        age_group_id_set.add( age_group_id )
        age_group_id_dict[age_group_id] = row
    #
    # sex_id2split_reference_id
    sex_id2split_reference_id = dict()
    for sex_name in sex_info_dict :
        sex_id             = sex_info_dict[sex_name]['sex_id']
        split_reference_id = sex_info_dict[sex_name]['split_reference_id']
        sex_id2split_reference_id[sex_id] = split_reference_id
    #
    # location_id2node_id
    file_ptr            = open(at_cascade.ihme.node_table_file)
    reader              = csv.DictReader(file_ptr)
    location_id2node_id = dict()
    node_id             = 0
    for row in reader :
        assert node_id == int( row['node_id'] )
        location_id = int( row['location_id'] )
        location_id2node_id[location_id] = node_id
        node_id += 1
    file_ptr.close()
    #
    # mtall_dict, age_group_id_subset
    file_ptr            = open(mtall_inp_file)
    reader              = csv.DictReader(file_ptr)
    mtall_dict          = dict()
    age_group_id_subset = set()
    for row in reader :
        age_group_id = int( row['age_group_id'] )
        if age_group_id in age_group_id_set :
            #
            # age_group_id_set
            age_group_id_subset.add( age_group_id )
            #
            # mtall_dict
            location_id  = int( row['location_id'] )
            sex_id       = int( row['sex_id'] )
            year_id      = int( row['year_id'] )
            mean         = float( row['mean'] )
            if location_id not in mtall_dict :
                mtall_dict[location_id] = dict()
            if sex_id not in mtall_dict[location_id] :
                mtall_dict[location_id][sex_id] = dict()
            if year_id not in mtall_dict[location_id][sex_id] :
                mtall_dict[location_id][sex_id][year_id] = dict()
            if age_group_id in mtall_dict[location_id][sex_id][year_id] :
                msg  = f'file = {mtall_inp_file}, with '
                msg += f'location_id = {location_id}, '
                msg += f'sex_id = {sex_id}, and '
                msg += f'year_id = {year_id}.\n'
                msg += f'The age_group_id {age_group_id} '
                msg += 'appears more than once.'
                assert False, msg
            mtall_dict[location_id][sex_id][year_id][age_group_id] = mean
    #
    # age_group_id_set
    previous_location_id      = None
    previous_sex_id           = None
    previous_year_id          = None
    previous_age_group_id_set = None
    for location_id in mtall_dict :
        for sex_id in mtall_dict[location_id] :
            for year_id in mtall_dict[location_id][sex_id] :
                keys = mtall_dict[location_id][sex_id][year_id].keys()
                age_group_id_set = set(keys)
                if previous_age_group_id_set != age_group_id_set \
                and previous_age_group_id_set is not None :
                    msg  = f'file = {mtall_inp_file}, '
                    msg += f'location_id = {location_id}, '
                    msg += f'sex_id = {sex_id}, '
                    msg += f'year_id = {year_id}, '
                    msg += f'age_group_id_set =\n{age_group_set}\n'
                    msg += f'location_id = {previous_location_id}, '
                    msg += f'sex_id = {previous_sex_id}, '
                    msg += f'year_id = {previous_year_id}, '
                    msg += f'age_group_id_set =\n {previous_age_group_set}'
                    assert False, msg
                previous_location_id      = location_id
                previous_sex_id           = sex_id
                previous_year_id          = year_id
                previous_age_group_id_set = age_group_id_set
    assert age_group_id_set == age_group_id_subset
    #
    #
    # check year_id_set
    previous_location_id = None
    previous_sex_id      = None
    previous_year_id_set = None
    for location_id in mtall_dict :
        for sex_id in mtall_dict[location_id] :
            keys = mtall_dict[location_id][sex_id].keys()
            year_id_set = set( keys )
            if previous_year_id_set != year_id_set \
            and previous_year_id_set is not None :
                msg  = f'file = {mtall_inp_file}, '
                msg += f'location_id = {location_id}, '
                msg += f'sex_id = {sex_id}, '
                msg += f'year_id_set =\n{year_id_set}\n'
                msg += f'location_id = {previous_location_id}, '
                msg += f'sex_id = {previous_sex_id}, '
                msg += f'year_id_set = {previous_year_id_set}, '
                assert False, msg
            previous_location_id      = location_id
            previous_sex_id           = sex_id
            previous_year_id_set      = year_id_set
    #
    # year_id_list
    year_id_list = sorted( year_id_set )
    #
    # age_group_id_list
    fun = lambda age_group_id : age_group_id_dict[age_group_id]['age_mid']
    age_group_id_list = sorted( age_group_id_set, key = fun )
    #
    # omega_age_table
    omega_age_table  = list()
    for age_group_id in age_group_id_list :
        age_mid = age_group_id_dict[age_group_id]['age_mid']
        # used so can match after converting to ascii and back
        age_mid = round(age_mid, at_cascade.ihme.age_grid_n_digits)
        row = {
            'age_group_id' : age_group_id,
            'age'          : age_mid,
        }
        omega_age_table.append( row )
    #
    # omega_time_table
    omega_time_table  = list()
    for year_id in year_id_list :
        time = year_id + 0.5
        row = { 'time' : time }
        omega_time_table.append( row )
    #
    # all_mtall_table
    # mtall_index_table
    all_mtall_table   = list()
    mtall_index_table = list()
    all_mtall_id      = 0
    for location_id in mtall_dict :
        node_id = location_id2node_id[location_id]
        for sex_id in mtall_dict[location_id] :
            split_reference_id = sex_id2split_reference_id[sex_id]
            row = {
                'all_mtall_id'       : all_mtall_id,
                'node_id'            : node_id,
                'split_reference_id' : split_reference_id
            }
            mtall_index_table.append(row)
            for year_id in year_id_list :
                for age_group_id in age_group_id_list :
                    all_mtall_value = \
                        mtall_dict[location_id][sex_id][year_id][age_group_id]
                    row = { 'all_mtall_value' : all_mtall_value }
                    all_mtall_table.append(row)
                    all_mtall_id += 1
    #
    # all_mtall_table_file
    at_cascade.ihme.write_csv(all_mtall_table_file, all_mtall_table)
    #
    # mtall_index_table_file
    at_cascade.ihme.write_csv(mtall_index_table_file, mtall_index_table)
    #
    # omega_age_table_file
    at_cascade.ihme.write_csv(omega_age_table_file, omega_age_table)
    #
    # omega_time_table_file
    at_cascade.ihme.write_csv(omega_time_table_file, omega_time_table)
