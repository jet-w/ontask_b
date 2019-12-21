# Generated by Django 2.2.8 on 2019-12-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0019_auto_20191221_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='name',
            field=models.CharField(choices=[('action_clone', 'Action cloned'), ('action_create', 'Action created'), ('action_delete', 'Action deleted'), ('download_zip_action', 'Download a ZIP with one file per text'), ('action_email_notify', 'Notification email sent'), ('action_email_read', 'Email read'), ('action_email_sent', 'Emails sent'), ('action_import', 'Action imported'), ('action_json_sent', 'Emails sent'), ('action_list_email_sent', 'Email with data list sent'), ('question_add', 'Question added'), ('question_toggle_changes', 'Question toggle changes'), ('action_rubric_criterion_add', 'Add a rubric criterion'), ('action_rubric_criterion_edit', 'Edit rubric criterion'), ('action_rubric_criterion_delete', 'Delete rubric criterion'), ('action_rubriccell_edit', 'Rubric cell edit'), ('action_rubric_loa_edit', 'Rubric level of attainment edit'), ('action_run_personalized_canvas_email', 'Execute scheduled canvas email action'), ('action_run_personalized_email', 'Execute scheduled email action'), ('action_run_personalized_json', 'Execute scheduled JSON action'), ('action_run_json_list', 'Execute scheduled JSON list action'), ('action_run_email_list', 'Execute scheduled send list action'), ('action_run_rubric_text', 'Execute personalized rubric text'), ('action_zip', 'Create a zip with personalized content'), ('action_serve_toggled', 'Action URL toggled'), ('action_served_execute', 'Action served'), ('survey_input', 'Survey data input'), ('action_update', 'Action updated'), ('athena_connection_clone', 'Athena connection cloned'), ('athena_connection_create', 'Athena connection created'), ('athena_connection_delete', 'Athena connection deleted'), ('athena_connection_edit', 'Athena connection updated'), ('athena_connection_toggle', 'Athena connection toggled'), ('column_add', 'Column added'), ('column_add_formula', 'Column with formula created'), ('column_add_random', 'Column with random values created'), ('column_clone', 'Column cloned'), ('column_delete', 'Column deleted'), ('column_edit', 'Column edited'), ('column_restrict', 'Column restricted'), ('condition_clone', 'Condition cloned'), ('condition_create', 'Condition created'), ('condition_delete', 'Condition deleted'), ('condition_update', 'Condition updated'), ('plugin_create', 'Plugin created'), ('plugin_delete', 'Plugin deleted'), ('plugin_execute', 'Plugin executed'), ('plugin_update', 'Plugin updated'), ('schedule_create', 'Create scheduled operation'), ('schedule_edit', 'Edit scheduled operation'), ('schedule_delete', 'Delete scheduled operation'), ('sql_connection_clone', 'SQL connection cloned'), ('sql_connection_create', 'SQL connection created'), ('sql_connection_delete', 'SQL connection deleted'), ('sql_connection_edit', 'SQL connection updated'), ('sql_connection_toggle', 'SQL connection toggled'), ('view_create', 'Table view created'), ('view_edit', 'Table view edited'), ('view_delete', 'Table view deleted'), ('view_clone', 'Table view cloned'), ('workflow_attribute_create', 'New attribute in workflow'), ('workflow_attribute_update', 'Attributes updated in workflow'), ('workflow_attribute_delete', 'Attribute deleted'), ('workflow_clone', 'Workflow cloned'), ('workflow_create', 'Workflow created'), ('workflow_data_failedmerge', 'Failed data merge into workflow'), ('workflow_data_flush', 'Workflow data flushed'), ('tablerow_create', 'Table row created'), ('tablerow_update', 'Table row updated'), ('workflow_athena_data_upload', 'Data uploaded to workflow'), ('workflow_csv_data_upload', 'Upload Data from CSV File'), ('workflow_excel_data_upload', 'Upload Data from Excel Sheet'), ('workflow_gsheet_data_upload', 'Upload Data from Google Sheet'), ('workflow_se_data_upload', 'Upload Data from S3 CSV source'), ('workflow_sql_data_upload', 'Upload Data from SQL source'), ('workflow_delete', 'Workflow deleted'), ('workflow_import', 'Import workflow'), ('workflow_increase_track_count', 'Increase workflow track count.'), ('workflow_share_add', 'User share added'), ('workflow_share_delete', 'User share deleted'), ('workflow_star', 'Toggle workflow star'), ('workflow_update', 'Workflow updated'), ('workflow_update_lusers', 'Update list of workflow users')], max_length=1024),
        ),
    ]
