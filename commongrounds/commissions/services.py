from django.db import transaction
from .models import Commission, Job


@transaction.atomic
def create_commission(*, author: dict, data: dict, jobs_data: list[dict]) -> Commission:
    commission = Commission.objects.create(
        **data,
        maker=author
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

def sync_commission_status(*, commission: dict) -> Commission:
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

