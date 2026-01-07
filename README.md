# Task-Manager-Operations-Process-Tracking-Tool-Python-
## Project Overview

This project is a Python-based task tracking and reporting system built to support day-to-day operational workflows in a small business or operations team. The application focuses on task allocation, monitoring, completion tracking, and performance reporting, all of which are core responsibilities in junior analyst and operations roles.

The system simulates real-world operational processes such as workload distribution, SLA monitoring, overdue task identification, and management reporting using structured data stored in text files.

## Operational Use Case

In many operations environments, tasks are manually tracked using spreadsheets or emails. This project demonstrates how those processes can be standardised, automated, and analysed using Python.

The tool enables:

Clear ownership of tasks

Visibility into completed and outstanding work

Identification of overdue items

Generation of management-ready operational reports

## Key Functional Capabilities
### User & Access Control

Login authentication using stored credentials

Role-based access control:

Admin users manage users and reports

Standard users manage and view assigned work

Centralised user data stored in user.txt

### Task Allocation & Monitoring

Assign tasks to users with due dates and descriptions

Automatically capture task assignment dates

Track task completion status

View:

All operational tasks

Tasks assigned to the current user

Completed tasks (admin view)

Delete incorrect or obsolete tasks (admin only)

### Operational Reporting & Analysis

Automated generation of operational reports:

Task volume and completion rates

Outstanding and overdue task tracking

Workload distribution per user

Reports generated as text files for easy review or export:

task_overview.txt

user_overview.txt

On-demand display of statistics in a clear, readable format

## Metrics Tracked

The application calculates and reports key operational KPIs, including:

Total tasks created

Completion vs non-completion rates

Overdue task percentages

Task allocation distribution per user

Individual user productivity indicators

## Technical Design & Structure

The program is modular and structured using clearly defined functions:

reg_user() – User onboarding (admin only)

add_task() – Task creation

view_all() – Full task list

view_mine() – User-specific task view

view_completed() – Completed task monitoring

delete_task() – Data cleanup and task removal

generate_report() – KPI and operational report generation

display_statistics() – Management-style summary output
