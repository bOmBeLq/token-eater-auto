# You are a programming agent.

# Regular prompt (updating specs)
Every time you receive a prompt, you must transform it into a list of requirements.
Then store requirements in `.md` file. eg. /specs/core/project.md
Decide yourself where to put the file, just make sure it's under /specs directory.
Every time you must decide on the spec file location get list of all existing spec files and consider if perhaps they could be reorganized.

# Question prompt
When asked a question think 
# Writing tests

Whenever told to "Write tests":
Check /specs/**.md files for changes using git (uncommited changes).
For each spec file create/update/regenerate test file, written in python+pytest.

Example prompt:
Create for me backend application with authentication.
Should result in asking as many questions as needed eg.
What technology should the application be written in?
What version of PHP should be used?
Should the application be dockerized?
Should it have registration or only predefined users?
Do you have list of users?

Should result in something like:
specs/core/docker.md
---
compose.yaml file should exist /
file should contain app image definition with:
image: php8.5-latest
ports: 80:80

Dockerfile file should exist in /
Dockerfile file should contain FROM php:8.5-fpm

specs/core/symfony.md
---
symfony application should be bootstraped
bin/console should prove symfony application works

specs/authentiaction/login.md
specs/authentiaction/register.md

Then also tests should exist:
specs/core/docker.py
specs/core/symfony.py
specs/authentiaction/login.py
specs/authentiaction/register.py

each having real python tests that test whatever requirements from .md file are met.

# Implementation
When told to "implement specs" or "implement" check current git status and see what are changes in specs/* files.
Then generate/update code according to specs.
Then run all tests and make sure they pass.
If tests don't pass pass then keep working until you make them pass.
You can modify specs/*.py files but make sure they cover all requirements from specs/*.md files.
If during developement you notice that to make things work you should modify specs/*.md files then you are allowed to modify them only after confirmation.

# Info
specs catalog is for you source of truth for the project, browse files located there to understand the system