import requests
import datetime
import json
import sys

url = 'http://loadbalancer-1146583039.us-east-1.elb.amazonaws.com/tasks/'


def get_all_tasks():
    response = requests.get(url=url + 'all_tasks')
    if (response.status_code == 200 or response.status_code == 201):
        print('Here are all your tasks: {0}'.format(response.text))
    else:
        print('ERROR!')


def get_task_by_id():
    task_id = str(input("Which task do you want to get? (insert id): "))
    response = requests.get(url=url + '{0}'.format(task_id))
    if (response.status_code == 200 or response.status_code == 201):
        print('Task {0}: {1}'.format(task_id, response.text))
    else:
        print('ERROR!')


def create_task():
    json = {
        "title": str(input("Title: ")),
        "pub_date": str(datetime.datetime.now()),
        "description": str(input("Description: "))
    }
    response = requests.post(url=url + 'create_task', json=json)
    if (response.status_code == 200 or response.status_code == 201):
        print('Task created: {0}'.format(response.text))
    else:
        print('ERROR!')
        print(response.text)
        print(response.status_code)


def update_task_title():
    task_id = str(input("Which task do you want to update? (insert id): "))
    json = {
        "title": str(input("Title: ")),
    }
    response = requests.put(url=url + 'update_task_title/{0}'.format(task_id), json=json)
    if (response.status_code == 200 or response.status_code == 201):
        print('Updated task {0} title to: {1}'.format(task_id, response.text))
    else:
        print('ERROR!')


def update_task_pub_date():
    task_id = str(input("Which task do you want to update? (insert id): "))
    json = {
        "pub_date": str(datetime.datetime.now())
    }
    response = requests.put(url=url + 'update_task_pub_date/{0}'.format(task_id), json=json)
    if (response.status_code == 200 or response.status_code == 201):
        print('Updated task {0} publication date to: {1}'.format(task_id, response.text))
    else:
        print('ERROR!')


def update_task_description():
    task_id = str(input("Which task do you want to update? (insert id): "))
    json = {
        "description": str(input("Description: "))
    }
    response = requests.put(url=url + 'update_task_description/{0}'.format(task_id), json=json)
    if (response.status_code == 200 or response.status_code == 201):
        print('Updated task {0} description to: {1}'.format(task_id, response.text))
    else:
        print('ERROR!')


def delete_task_by_id():
    task_id = str(input("Which task do you want to delete? (insert id): "))
    response = requests.delete(url=url + 'delete_task/{0}'.format(task_id))
    if (response.status_code == 200 or response.status_code == 201):
        print('Deleted task {0}'.format(task_id))
    else:
        print('ERROR!')


def delete_all_tasks():
    response =  requests.delete(url=url + 'delete_all_tasks')
    if (response.status_code == 200 or response.status_code == 201):
        print('Deleted all tasks')
    else:
        print('ERROR!')
                

# GET_ALL   -> get_all_tasks
# GET_1     -> get_task_by_id
# CREATE    -> create_task
# UPDATE_T  -> update_task_title
# UPDATE_P  -> update_task_pub_date
# UPDATE_D  -> update_task_description
# DELETE_1  -> delete_task_by_id
# DELETE_ALL-> delete_all_tasks


def main():

    command = sys.argv[1]

    if command == 'GET_ALL': 
        print("Loading...")
        get_all_tasks()
    elif command == 'GET_1':
        print("Loading...")
        get_task_by_id()
    elif command == 'CREATE':
        print("Loading...")
        create_task()
    elif command == 'UPDATE_T':
        print("Loading...")
        update_task_title()
    elif command == 'UPDATE_P':
        print("Loading...")
        update_task_pub_date()
    elif command == 'UPDATE_D':
        print("Loading...")
        update_task_description()
    elif command == 'DELETE_1':
        print("Loading...")
        delete_task_by_id()
    elif command == 'DELETE_ALL':
        print("Loading...")
        delete_all_tasks()
    else:
        print("Invalid command, please try again! \n   GET_ALL: get all tasks \n   GET_1: get task by id \n   CREATE: create new task \n   UPDATE_T: update task title \n   UPDATE_P: update task publication date \n   UPDATE_D: update task description \n   DELETE_1: delete task by id \n   DELETE_ALL: delete all tasks")

    return 0


if __name__ == '__main__':
    main()