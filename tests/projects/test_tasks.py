from datetime import date
from unittest.mock import patch

import pytest
from django.template.loader import render_to_string
from freezegun import freeze_time
from projects.tasks import send_project_initial_email

pytestmark = pytest.mark.django_db


@freeze_time("1988-02-01")
@patch("projects.tasks.EmailMultiAlternatives")
def test_send_project_initial_email(mock_email, project_company):
    company = project_company.company
    project = project_company.project

    send_project_initial_email(project.id, company.id)

    expected_context = {"project": project, "deadline": date(1988, 2, 8)}
    expected_html_content = render_to_string(
        project.initial_email_template, expected_context
    )

    mock_email.assert_called_once_with(
        subject="31/01/1988 - Circularização de Estoque :: Rep Jabuti",
        body=expected_html_content,
        from_email=project.email_from,
        to=company.email_to,
        cc=company.email_cc,
    )
    mock_email.return_value.attach_alternative.assert_called_once()
    mock_email.return_value.attach_file.assert_called_once()
    mock_email.return_value.send.assert_called_once()
