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


# @transaction.atomic
# def update():
