import jenkins
import xmltodict

from dto.Job import Job
from dto.JobParameter import JobParameter
from service.config import config

PARAM_CHOICES = 'choices'

PARAM_NAME = 'name'

con = jenkins.Jenkins(url=config.get('jenkins', 'url'),
                      username=config.get('jenkins', 'username'),
                      password=config.get('jenkins', 'password'))


async def run_job_dto(job: Job):
    job_name = job.name
    params = job.params
    jenkins_params = {}
    for param in params:
        jenkins_params[param.name] = param.value

    return con.build_job(job_name, jenkins_params)


def list_jobs():
    #TODO Add a proper list jobs method, using con.get_jobs(). For now this mock-up will do the trick
    return ["Backend performance tests", "makefile", "GiteaSync"]


def get_job_config(job_name: str):
    job_xml_config = con.get_job_config(job_name)
    job_json_config = xmltodict.parse(job_xml_config)

    job = Job(job_json_config['flow-definition']['description'], [])
    try:
        params = []
        parameters_json = job_json_config['flow-definition']['properties']['hudson.model.ParametersDefinitionProperty'][
            'parameterDefinitions']
        for param_json in parameters_json.get('hudson.model.ChoiceParameterDefinition', []):
            param = create_choice_parameter(param_json)
            params.append(param)
        for param_json in parameters_json.get('hudson.model.TextParameterDefinition', []):
            param = create_text_parameter(param_json)
            params.append(param)
        job.params = params
    except KeyError:
        print("Error getting parameters for job - maybe it's not parametrized")

    return job


def create_text_parameter(parameter_json):
    param = JobParameter(parameter_json[PARAM_NAME], 'String', parameter_json['defaultValue'], [])
    return param


def create_choice_parameter(parameter_json):
    param = JobParameter(parameter_json[PARAM_NAME], 'Choice', parameter_json[PARAM_CHOICES]['a']['string'][0],
                         parameter_json[PARAM_CHOICES]['a']['string'])
    return param
