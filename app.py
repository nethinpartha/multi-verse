# Python Django
# Test a Django project on multiple versions of Python.
trigger:
- master
pool:
 vmImage: ‘ubuntu-latest’
strategy:
 matrix:
 Python35:
 PYTHON_VERSION: ‘3.5’
 Python36:
 PYTHON_VERSION: ‘3.6’
 Python37:
 PYTHON_VERSION: ‘3.7’
 maxParallel: 3
steps:
- task: UsePythonVersion@0
 inputs:
 versionSpec: ‘$(PYTHON_VERSION)’
 architecture: ‘x64’
- task: PythonScript@0
 displayName: ‘Export project path’
 inputs:
 scriptSource: ‘inline’
 script: |
 “““Search all subdirectories for `manage.py`.”””
 from glob import iglob
 from os import path
 # Python >= 3.5
 manage_py = next(iglob(path.join(‘**’, ‘manage.py’), recursive=True), None)
 if not manage_py:
 raise SystemExit(‘Could not find a Django project’)
 project_location = path.dirname(path.abspath(manage_py))
 print(‘Found Django project in’, project_location)
 print(‘##vso[task.setvariable variable=projectRoot]{}’.format(project_location))
- script: |
 python -m pip install — upgrade pip setuptools wheel
 pip install -r requirements.txt
 pip install unittest-xml-reporting
 displayName: ‘Install prerequisites’
# Pytest Unit Test with Coverage
- script: |
 pushd ‘$(projectRoot)’
 pip install pytest pytest-azurepipelines pytest-cov
 pytest -v — cov — cov-report=xml
 displayName: “Pytest Unit Test with Coverage”
 continueOnError: False
- task: PublishTestResults@2
 inputs:
 testResultsFiles: “**/test-*.xml”
 testRunTitle: ‘Python $(PYTHON_VERSION)’
 condition: succeededOrFailed()
