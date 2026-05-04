from django.db import transaction
from .models import Commission, Job, JobApplication
from accounts.models import Profile


@transaction.atomic
def create_commission(*, author: Profile, data: Commission, jobs_data: list[Job]) -> Commission:
    commission = Commission.objects.create(
        **data,
    )
    job_instances = []
    for job in jobs_data:
        print(job.get('role'), job.get('DELETE'))
        if not job or job.get('DELETE'):
            continue
        del job['DELETE']
        job = Job(
            commission=commission,
            **job
        )
        job.full_clean()
        job_instances.append(job)
    Job.objects.bulk_create(job_instances)
    return commission


def apply_to_job(*, applicant: Profile, job: Job) -> bool:
    if not JobApplication.objects.filter(job=job).filter(applicant=applicant).exists() and job.status == Job.OPEN:
        job_application = JobApplication.objects.create(
            applicant=applicant,
            job=job,
        )
        return True
    return False


def sync_commission_status(*, commission: Commission) -> Commission:
    jobs = Job.objects.filter(commission=commission)
    isFull = True
    for job in jobs:
        print(job.status)
        if (job.status != Job.FULL):
            isFull = False
    if isFull:
        commission.status = Commission.FULL
    commission.save()
    return commission


def get_commission_summary(*, commission: Commission) -> dict:
    total_manpower = 0
    open_manpower = 0
    current_manpower = 0
    jobs = Job.objects.filter(commission=commission)
    for job in jobs:
        total_manpower += job.manpower_required
        accepted_job_application = JobApplication.objects.filter(
            job=job, status=JobApplication.ACCEPTED)
        current_manpower += accepted_job_application.count()
    open_manpower = total_manpower - current_manpower
    commission.people_required = total_manpower
    commission.save()
    return {"total_manpower": total_manpower, "open_manpower": open_manpower}
        
        
