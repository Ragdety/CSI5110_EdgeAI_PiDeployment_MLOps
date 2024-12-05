@echo off
:: Edge Impulse Configuration
set EI_PROJECT_ID=567506
set EI_API_KEY=ei_74764e196dffd7ac778c73d51270c38289b018887fcc473cf948004e148dda93
set DEPLOY_TYPE=zip

:: Step 1: Setup
python main.py setup --project_id %EI_PROJECT_ID% --api_key %EI_API_KEY% --deploy_type %DEPLOY_TYPE%
if %errorlevel% neq 0 (
    echo Setup failed.
    exit /b %errorlevel%
)
echo Setup completed.

:: Step 2: Build
for /f "tokens=2 delims=:" %%A in ('python main.py build ^| findstr "Job ID"') do set JOB_ID=%%A
set JOB_ID=%JOB_ID: =%

if not defined JOB_ID (
    echo Failed to retrieve Job ID.
    exit /b 1
)
echo Build started. Job ID: %JOB_ID%

:: Step 3: Wait for Job Completion
python main.py wait_for_job_completion --job_id %JOB_ID%
if %errorlevel% neq 0 (
    echo Job completion check failed.
    exit /b %errorlevel%
)
echo Job %JOB_ID% completed successfully.

:: Step 4: Deploy
python main.py deploy_model
if %errorlevel% neq 0 (
    echo Model deployment failed.
    exit /b %errorlevel%
)
echo Model deployed and downloaded successfully.