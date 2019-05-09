from typing import Optional

import pandas as pd
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from dataops.forms import FIELD_PREFIX, RowForm
from dataops.pandas import db, is_unique_column, store_dataframe
from dataops.sql import get_rows, update_row
from logs.models import Log
from ontask.decorators import get_workflow
from ontask.permissions import is_instructor
from workflow.models import Workflow
from workflow.ops import store_workflow_in_session


@user_passes_test(is_instructor)
@get_workflow(pf_related='columns')
def row_update(
    request: HttpRequest,
    workflow: Optional[Workflow] = None,
) -> HttpResponse:
    """
    Receives a POST request to update a row in the data table
    :param request: Request object with all the data.
    :return:
    """
    # Get the pair key,value to fetch the row from the table
    update_key = request.GET.get('update_key', None)
    update_val = request.GET.get('update_val', None)

    if not update_key or not update_val:
        # Malformed request
        return render(request, 'error.html',
                      {'message': _('Unable to update table row')})

    # Get the rows from the table
    rows = get_rows(
        workflow.get_data_frame_table_name(),
        column_names=workflow.get_column_names(),
        filter_pairs={update_key: update_val},
    )

    row_form = RowForm(request.POST or None,
                       workflow=workflow,
                       initial_values=list(rows[0]))

    if request.method == 'POST' and row_form.is_valid():

        # Create the query to update the row
        set_pairs = {}
        unique_names = workflow.get_unique_columns().values_list('name', flat=True)
        filter_pair = {}
        log_payload = []
        for idx, colname in enumerate(unique_names):
            value = row_form.cleaned_data[FIELD_PREFIX + '%s' % idx]
            set_pairs[colname] = value
            log_payload.append((colname, str(value)))

            if not filter_pair and colname in unique_names:
                filter_pair[colname] = value

        # If there is no unique key, something went wrong.
        if not filter_pair:
            raise Exception(_('Key value not found when updating row'))

        update_row(
            workflow.get_data_frame_table_name(),
            set_pairs=set_pairs,
            filter_pairs=filter_pair)

        # Recompute all the values of the conditions in each of the actions
        # TODO: See if this can be pushed asychronously (probably not)
        for act in workflow.actions.all():
            act.update_n_rows_selected()

        # Log the event
        Log.objects.register(request.user,
                             Log.TABLEROW_UPDATE,
                             workflow,
                             {'id': workflow.id,
                              'name': workflow.name,
                              'new_values': log_payload})

        return redirect('table:display')

    return render(request,
                  'dataops/row_filter.html',
                  {'workflow': workflow,
                   'row_form': row_form,
                   'cancel_url': reverse('table:display')})


@user_passes_test(is_instructor)
@get_workflow(pf_related=['columns', 'actions'])
def row_create(
    request: HttpRequest,
    workflow: Optional[Workflow] = None,
) -> HttpResponse:
    """
    Receives a POST request to create a new row in the data table
    :param request: Request object with all the data.
    :return:
    """
    # If the workflow has no data, the operation should not be allowed
    if workflow.nrows == 0:
        return redirect('dataops:uploadmerge')

    # Create the form
    form = RowForm(request.POST or None, workflow=workflow)

    if request.method == 'POST' and form.is_valid():
        # Create the query to update the row
        columns = workflow.get_columns()
        column_names = [c.name for c in columns]
        field_name = FIELD_PREFIX + '%s'
        row_vals = [form.cleaned_data[field_name % idx]
                    for idx in range(len(columns))]

        # Load the existing df from the db
        df = db.load_table(workflow.get_data_frame_table_name())

        # Perform the row addition in the DF first
        # df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
        # df.append(df2, ignore_index=True)
        new_row = pd.DataFrame([row_vals], columns=column_names)
        df = df.append(new_row, ignore_index=True)

        # Verify that the unique columns remain unique
        for ucol in [c for c in columns.filter(is_key=True)]:
            if not is_unique_column(df[ucol.name]):
                form.add_error(
                    None,
                    _('Repeated value in column {0}. It must be different '
                      'to maintain Key property').format(ucol.name)
                )
                return render(request,
                              'dataops/row_create.html',
                              {'workflow': workflow,
                               'form': form,
                               'cancel_url': reverse('table:display')})

        # Restore the dataframe to the DB
        store_dataframe(df, workflow)

        # Update the session information
        store_workflow_in_session(request, workflow)

        # Recompute all the values of the conditions in each of the actions
        # TODO: Can we do this asynchronously?
        for act in workflow.actions.all():
            act.update_n_rows_selected()

        # Log the event
        log_payload = list(zip(column_names, [str(x) for x in row_vals]))
        Log.objects.register(request.user,
                             Log.TABLEROW_CREATE,
                             workflow,
                             {'id': workflow.id,
                              'name': workflow.name,
                              'new_values': log_payload})

        # Done. Back to the table view
        return redirect('table:display')

    return render(request,
                  'dataops/row_create.html',
                  {'workflow': workflow,
                   'form': form,
                   'cancel_url': reverse('table:display')})
