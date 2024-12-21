from datetime import date, timedelta

from celery_app import app
from comercial.models import Company
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Project, ProjectCompany


@app.task(bind=True)
def send_project_initial_email(self, project_id, company_id):
    project = Project.objects.get(pk=project_id)
    company = Company.objects.get(pk=company_id)

    email_attachment = (
        f"static/attachments/{project.date_display_dash} - {project.category}.pdf"
    )
    if company.system == "siagri":
        email_attachment = f"static/attachments/{project.date_display_dash} - {project.category} siagri.pdf"  # noqa: E501

    deadline = date.today() + timedelta(days=6)
    if deadline.isoweekday() in [6, 7]:
        ajust_days = 8 - deadline.isoweekday()
        deadline += timedelta(days=ajust_days)

    context = {"project": project, "deadline": deadline}

    template = project.initial_email_template
    html_content = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject=f"{str(project)} :: {company.company_name}",
        body=html_content,
        from_email=project.email_from,
        to=company.email_to,
        cc=company.email_cc,
    )

    email.attach_alternative(html_content, "text/html")
    email.attach_file(email_attachment)
    email.send()


@app.task(bind=True)
def send_project_initial_email_custom_cutoff(self, project_company_id):
    project_company = ProjectCompany.objects.select_related("project", "company").get(
        pk=project_company_id
    )
    project = project_company.project
    company = project_company.company

    email_attachment = (
        f"static/attachments/{project.date_display_dash} - {project.category}.pdf"
    )

    context = {
        "project": project,
        "deadline": project_company.deadline,
        "cutoff": project_company.cutoff,
    }

    template = project.initial_email_template_custom_cutoff
    html_content = render_to_string(template, context)

    subject = (
        f"{project_company.cutoff.strftime('%d/%m/%Y')} - "
        f"{project.get_category_display()} :: {company.company_name}"
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=project.email_from,
        to=company.email_to,
        cc=company.email_cc,
    )

    email.attach_alternative(html_content, "text/html")
    email.attach_file(email_attachment)
    email.send()
