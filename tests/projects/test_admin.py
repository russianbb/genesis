from unittest.mock import Mock, patch

import pytest
from projects.admin import send_initial_email
from projects.models import ProjectCompany

pytestmark = pytest.mark.django_db


@patch("projects.admin.send_project_initial_email.apply_async")
def test_send_initial_email(mock_async, project_company):
    queryset = ProjectCompany.objects.all()

    send_initial_email(Mock(), Mock(), queryset)

    mock_async.assert_called_once_with(
        kwargs={
            "project_id": project_company.project.id,
            "company_id": project_company.company.id,
        }
    )
