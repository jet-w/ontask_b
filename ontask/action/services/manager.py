# -*- coding: utf-8 -*-

"""Base class for CRUD manager for actions."""

from typing import Any, Dict, Optional, Type

from django import http
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.utils.translation import ugettext

from ontask import models, tasks
from ontask.core import SessionPayload


class ActionManagerBase(object):
    """Base class to provide the service for the run views."""

    def _create_log_event(
        self,
        user,
        action: models.Action,
        payload: Optional[Dict] = None,
        log_item: Optional[models.Log] = None,
    ):
        if not log_item and self.log_event:
            log_item = action.log(
                user,
                **payload)

        return log_item

    def __init__(
        self,
        form_class: Optional[Type[forms.Form]] = None,
        log_event: Optional[str] = None,
    ):
        """Assign and initialize the main service parameters."""
        self.form_class = form_class
        self.template = 'action/run_done.html'
        self.log_event = log_event

    def process_request(
        self,
        operation_type: str,
        request: http.HttpRequest,
        action: models.Action,
        prev_url: str,
    ) -> http.HttpResponse:
        """Process a request (GET or POST)."""
        payload = SessionPayload(
            request.session,
            initial_values={
                'action_id': action.id,
                'operation_type': operation_type,
                'prev_url': prev_url,
                'post_url': reverse('action:run_done')})

        form = self.form_class(
            request.POST or None,
            columns=action.workflow.columns.filter(is_key=True),
            action=action,
            form_info=payload)

        if request.method == 'POST' and form.is_valid():
            return self.process_post(request, action, payload)

        # Render the form
        return render(
            request,
            self.template,
            {'action': action,
             'num_msgs': action.get_rows_selected(),
             'form': form,
             'valuerange': range(2)})

    def process_post(
        self,
        request: http.HttpRequest,
        action: models.Action,
        payload: SessionPayload,
    ) -> http.HttpResponse:
        """Process the VALID POST request."""
        if payload.get('confirm_items'):
            # Add information to the session object to execute the next pages
            payload['button_label'] = ugettext('Send')
            payload['valuerange'] = 2
            payload['step'] = 2
            payload.store_in_session(request.session)

            return redirect('action:item_filter')

        # Go straight to the final step.
        return self.process_request_done(
            request,
            workflow=action.workflow,
            payload=payload,
            action=action)

    def process_request_done(
        self,
        request: http.HttpRequest,
        workflow: models.Workflow,
        payload: SessionPayload,
        action: Optional[models.Action] = None,
    ):
        """Finish processing the request after item selection."""
        # Get the information from the payload
        if not action:
            action = workflow.actions.filter(pk=payload['action_id']).first()
            if not action:
                return redirect('home')

        log_item = self._create_log_event(
            request.user,
            action,
            payload.get_store())

        tasks.execute_operation.delay(
            action.action_type,
            user_id=request.user.id,
            log_id=log_item.id,
            workflow_id=workflow.id,
            action_id=action.id if action else None,
            payload=payload.get_store())

        # Reset object to carry action info throughout dialogs
        SessionPayload.flush(request.session)

        # Successful processing.
        return render(
            request,
            'action/run_done.html',
            {'log_id': log_item.id, 'download': payload['export_wf']})

    def execute_operation(
        self,
        user,
        workflow: Optional[models.Workflow] = None,
        action: Optional[models.Action] = None,
        payload: Optional[Dict] = None,
        log_item: Optional[models.Log] = None,
    ):
        """Run the action."""
        del user, action, payload
        raise Exception('Incorrect invocation of run method.')