from .models import DeployProject


def create_deploy_project_service(config_file, commit_hash=None):
    return DeployProject.objects.create(config_file=config_file, commit_hash=commit_hash)


def update_project_status_service(deploy_id, status, recommendations, commit_hash=None):
    deploy_project = DeployProject.objects.get(id=deploy_id)
    deploy_project.status = status
    deploy_project.recommendations = recommendations
    deploy_project.commit_hash = commit_hash
    deploy_project.save()
    return deploy_project
