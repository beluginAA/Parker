from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import api_id, api_hash

class Parcer:

    def __init__(self):
        self.amountOfSkill = {}
        self.valueOfSalary = {}
        self.amountOfVacancions = 0
        self.client = TelegramClient('test_tg', api_id, api_hash)
        self.client.start()

    def _get_dialogs(self) -> list[str]:
        dialogs = self.client.get_dialogs() 
        for dialog in dialogs:
            if dialog.title == 'getmatch: бот с IT-вакансиями':
                messages = self.client.iter_messages(dialog)
                break
        return messages

    def _get_info(self, vacancy: str, salary = '', stack = '') -> list[str]:
        information = vacancy.text.split('\n')
        if len(information) > 5:
            for iter in information:
                if 'на руки' in iter:
                    salary = iter
                elif 'Стек' in iter:
                    stack = iter
                    break
        if salary == '':
            salary = 'Вакансия без зарплаты'
        return salary, stack

    def _get_salary(self, string:str) -> int:
        for deli in ['₽', '€', '$']:
            if deli in string:
                delimiter = ' ' + deli 
        amount = string.split(delimiter)[0]
        if '—‍' in amount:
            left, right = [int(number.replace(' ', '').replace('\\u*d', '').replace("≈", "")) for number in amount.split(' —‍ ')]
            salary = int((left+right)/2)
        else:
            salary = int(amount.replace("от ", "").replace(" ", "").replace("≈ ", ""))
        return salary
    
    def _get_stack(self, string:str) -> list[str]:
        array = string.replace('**Стек**: ', '').replace('.', '').split(', ')
        exceptions = ['CI/CD', 'TCP/IP']
        correctArray = []
        for iter in array:
            iter = iter.lstrip().rstrip()
            if iter in ['NET 31/6', 'NET']:
                correctArray.append('NET 3.1/6')
            elif iter in ['Gitlab CI', 'CD', 'CI', 'GitLab CI']:
                correctArray.append('CI/CD')
            elif iter == 'Unix Shell':
                correctArray.append('Bash')
            elif iter in ['Ubuntu', 'Ubuntu', 'Debian', 'Astra Linux', 'CentOS', 'Debian GNU', 'Linux Kernel', 'RedHat', 'Rocky Linux', 'UNIX', 'Unix']:
                correctArray.append('Linux')
            elif iter in ['Docker Compose', 'Docker Swarm', 'Dockerfile']:
                correctArray.append('Docker')
            elif iter == 'VMware':
                correctArray.append('VMWare')
            elif iter == 'Cosmos DB':
                correctArray.append('CosmosDB')
            elif iter == 'Victoria Metrics':
                correctArray.append('VictoriaMetrics')
            elif iter == 'Saltstack':
                correctArray.append('SaltStack')
            elif iter == 'Redis Cluster':
                correctArray.append('Redis')
            elif iter == 'REST':
                correctArray.append('REST API')
            elif iter == 'Logtash':
                correctArray.append('Logstash')
            elif iter == 'Nodejs':
                correctArray.append('NodeJS')
            elif iter == 'OSI Model':
                correctArray.append('OSI')
            elif iter == 'HaProxy':
                correctArray.append('HAProxy')
            elif iter in ['ngnix', 'NGINX', 'nginx']:
                correctArray.append('Nginx')
            elif iter == 'OpenSeach':
                correctArray.append('OpenSearch')
            elif iter == 'postfix':
                correctArray.append('Postfix')
            elif iter == 'QEMU-KVM':
                correctArray.append('QEMU')
            elif iter == 'skopeo':
                correctArray.append('Skopeo')
            elif iter in ['Powershell', 'Shell']:
                correctArray.append('PowerShell')
            elif iter == 'pgSQL':
                correctArray.append('PostgreSQL')
            elif iter == 'K8s':
                correctArray.append('Kubernetes')
            elif iter == 'FirewallD':
                correctArray.append('Firewall')
            elif iter == 'JDK':
                correctArray.append('Java')
            elif iter == 'IPsec':
                correctArray.append('IPS')
            elif iter == 'Flux CD':
                correctArray.append('Flux')
            elif iter in ['Hashicorp Vault', 'Hashicorp Vault']:
                correctArray.append('HashiСorp Vault')
            elif iter == 'VMware ESXi':
                correctArray.append('VMWare ESXi')
            elif iter == 'HTTPS':
                correctArray.append('HTTP')
            elif iter in ['Helmfile', 'Help Desk']:
                correctArray.append('Helm')
            elif iter == 'YandexCloud':
                correctArray.append('Yandex Cloud')
            elif iter in ['MS SQL', 'Microsoft Server']:
                correctArray.append('Microsoft SQL Server')
            elif iter == 'Xen':
                correctArray.append('XenDesktop')
            elif iter == 'MLFlow':
                correctArray.append('MLflow')
            elif iter in ['TCP', 'IPv4']:
                correctArray.append('TCP/IP')
            elif iter == 'Airflow':
                correctArray.append('AirFlow')
            elif iter == 'ArgoCD':
                correctArray.append('Argo CD')
            elif iter == 'Buildkite':
                correctArray.append('Buildkit')
            elif iter == 'Burp':
                correctArray.append('Burp Suite')
            elif iter == 'Github Actions':
                correctArray.append('GitHub Actions')
            elif iter == 'Gitlab':
                correctArray.append('GitLab')
            elif iter == 'Golang':
                correctArray.append('Go')
            elif iter == 'Green':
                correctArray.append('Greenplum')
            elif iter in ['TerraForm', 'TerraForm']:
                correctArray.append('Terraform')
            elif iter == 'Apache Kafka':
                correctArray.append('Kafka')
            elif iter in ['tcpdump', 'vSphere', 'vSphere']:
                correctArray.append(iter[0].upper() + iter[1:])
            elif ('/' not in iter) or (iter in exceptions):
                correctArray.append(iter)
            else:
                iter = [skill.lstrip().rstrip() for skill in iter.split('/')]
                correctArray.extend(iter)
        return correctArray
    
    def _get_value(self, stack: list[str], salary:int) -> dict[str:int]:
        if salary != 'Вакансия без зарплаты':
            self.valueOfSalary.setdefault(salary, [])
            self.valueOfSalary[salary].extend(stack)
        for skill in stack:
            # resultStack[skill] = cost
            self.amountOfSkill.setdefault(skill, 0)
            self.amountOfSkill[skill] += 1
        # return stack
    
    @staticmethod
    def _update_last_vacancy(lastVacancy: str) -> None:
        config_file = "last_vacancy.py"
        lastVacancy = lastVacancy.text

        with open(config_file, "r") as file:
            lines = file.readlines()
            updated_lines = []
    
            for line in lines:
                if "lastVacancy" not in line:
                    updated_lines.append(line)
                else:
                    updated_lines.append(f"lastVacancy = \'''{lastVacancy}\'''\n")
                    break

        with open(config_file, "w") as file:
            file.writelines(updated_lines)

    def _get_last_vacancy(self, messages: list[str]) -> None:
        for message in messages:
            self._update_last_vacancy(message)
            break
    

