# Software_Engineering

## Introduction

This repository is for the Software Engineering course at the NanKai University. The course is held by Prof. Xu. The course is about the basics of software engineering and the development of a software project in a team.

The project is the final assignment of the course. The project is a intelligent operation and maintenance system that using Django as the web framework combined with large language model to provide the user with the best solution to the problem.

User can input the code and ask the system to generate the cell test case for the code. And users can click the "submit and test" button to testing the code based on the test cases. If the code is correct, the result will be "pass!", otherwise it will output the error message.

### Team Members

Our team member including:

- Mingxu Zhang: Undergraduate student at NanKai University, major in Computer Science and Technology. [Email](2113615@mail.nankai.edu.cn). 

- Huicheng Zhang: Undergraduate student at NanKai University, major in Computer Science and Technology. [Email](2112241@mail.nankai.edu.cn)

- Duanjun Qi: Undergraduate student at NanKai University, major in Information Security. [Email](2110697@mail.nankai.edu.cn)

- Fuzheng Ye: Undergraduate student at NanKai University, major in Information Security. [Email](2113203@mail.nankai.edu.cn)

### Starting the Project

To start the project, you need to install the Django and other dependencies. You can install the dependencies by running the following command:

```bash
git clone https://github.com/mingxuZhang2/Software_Engineering.git
cd Software_Engineering
pip install -r requirements.txt
```

Open the code\_submission app and find the view.py file, then filling your openai api key in the following code:

```python
openai.api_key = ''
```

After filling the Key, you can start the project by running the following command:

```bash
python manage.py runserver
```

After running the command, you can open the browser and visit the following URL:

```
http://127.0.0.1:8000/
```
