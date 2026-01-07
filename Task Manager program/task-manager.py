from tabulate import tabulate
from datetime import datetime
import os


class User:
    def __init__(self, user_name, password, tasks=None):
        self.user_name = user_name
        self.password = password

        # Each user gets their own independent task list
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_task_list(self):
        return self.tasks

    def __str__(self):
        return (
            f"{'User:':<10} {self.user_name}\n"
            f"{'Password:':<10} {self.password}\n"
            f"{'Tasks:':<10} {self.tasks}\n"
            f"----------------------------------"
        )

# users         -> list of User objects
# user_list     -> user data read from user.txt
# task_list     -> task data read from tasks.txt
# deleted_tasks -> keeps deleted tasks for possible future recovery
# user_tasks    -> maps username to list of their tasks


users = []
user_list = []
task_list = []
deleted_tasks = []
user_tasks = {}
task_found = False


def read_user_data(users, user_list, task_list, user_tasks):

    try:
        with open("user.txt", "r+", encoding="utf-8") as user_file:

            for i in user_file:
                # Strip leading spaces after commas
                user_line = [j.lstrip() for j in i.split(",")]
                user_list.append(user_line)

        with open("tasks.txt", "r+", encoding="utf-8") as task_file:

            for i in task_file:
                task_line = [j.strip() for j in i.split(",")]
                task_list.append(task_line)

        with open("user.txt", "a+", encoding="utf-8") as u_file:
            # Ensure files always end with a newline
            u_file.write("\n")

        with open("tasks.txt", "a+", encoding="utf-8") as t_file:
            # Ensure files always end with a newline
            t_file.write("\n")

    except FileNotFoundError:
        print("The file does not exist. Please check the file path and try "
              "again.")

    user_tasks[user_list[0][0]] = []

    for i in range(len(user_list)):
        for j in range(len(task_list)):
            if task_list[j][0] == user_list[i][0]:
                user_tasks[user_list[i][0]].append(task_list[j])

    for i in user_list:
        for j, k in user_tasks.items():
            user = User(i[0], i[1], k)
            users.append(user)


def reg_user(users, new_user, password):
    user = User(new_user, password)
    users.append(user)

    try:
        with open("user.txt", "a+", encoding="utf-8") as file:
            file.write(f"{new_user}, {password}\n")
            print(f"\n{new_user} successfully registered and added to "
                  f"user.txt")

    except FileNotFoundError:
        print("The file does not exist. Please check the file path and try "
              "again.")


def add_task(users, new_user, task):
    user_found = False
    for i in users:
        if i.user_name == new_user:
            user_found = True
            i.tasks.append(task)
    if user_found:
        task_line = (",").join(task)
        try:
            with open("tasks.txt", "a+", encoding="utf-8") as file:
                file.write(f"{task_line}\n")
                print("\nTask successfully added to task.txt")

        except FileNotFoundError:
            print("The file does not exist. Please check the file path and "
                  "try again.")
    else:
        print("\nUser was not found, cannot add task - please register user")


def view_all_tasks(users):
    headers = ["ID", "User", "Task Title", "Description", "Start", "End",
               "Completed"]
    rows = []
    ID = 1

    for user in users:
        for task in user.tasks:
            rows.append([
                ID,
                task[0],
                task[1],
                task[2],
                task[3],
                task[4],
                task[5]
            ])
            ID += 1

    print("\nTasks for the whole team:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def view_mine(users, user_name, ID=0):
    headers = ["ID", "Task Title", "Description", "Start", "End",
               "Completed"]
    rows = []
    task_found = False

    # Find the current logged-in user
    current_user = None
    for user in users:
        if user.user_name == user_name:
            current_user = user
            break

    if not current_user:
        print("User not found")
        return False

    if ID == 0:
        for index, task in enumerate(current_user.tasks, start=1):
            rows.append([
                index,
                task[1],
                task[2],
                task[3],
                task[4],
                task[5]
            ])

        print("\nYour tasks:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return False

    if 1 <= ID <= len(current_user.tasks):
        task = current_user.tasks[ID - 1]
        rows.append([
            ID,
            task[1],
            task[2],
            task[3],
            task[4],
            task[5]
        ])
        print("\nChosen task:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        task_found = True
    else:
        print(f"\nTask with ID {ID} was not found")

    return task_found


def view_completed(users):
    headers = ["ID", "User", "Task Title", "Description", "Start", "End",
               "Completed"]
    rows = []
    ID = 1

    for user in users:
        for task in user.tasks:
            if task[5] == "Yes":
                rows.append([
                    ID,
                    task[0],
                    task[1],
                    task[2],
                    task[3],
                    task[4],
                    task[5]
                ])
                ID += 1

    print("\nCompleted tasks: ")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def delete_task(users, deleted_tasks, ID):
    is_deleted = False

    for user in users:
        for index, task in enumerate(user.tasks, start=1):
            if index == ID:
                deleted_tasks.append(task)
                user.tasks.remove(task)
                is_deleted = True
                break

    if is_deleted:
        print("\nTask successfully deleted")
    else:
        print(f"\nTask with ID: {ID} was not found")


def update_tasks_file(users):
    try:
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for user in users:
                for task in user.tasks:
                    file.write(",".join(task) + "\n")
    except FileNotFoundError:
        print("tasks.txt not found")


def authenticate(users, user_name, password):
    for user in users:
        if user.user_name == user_name and user.password == password:
            return user
    return None


def is_overdue(task):
    if task[5] == "Yes":
        return False

    due_date = datetime.strptime(task[3], "%d %b %Y")
    return due_date < datetime.now()


def generate_task_overview(users):
    all_tasks = [task for user in users for task in user.tasks]

    total_tasks = len(all_tasks)
    completed = sum(1 for task in all_tasks if task[5] == "Yes")
    incomplete = total_tasks - completed
    overdue = sum(1 for task in all_tasks if is_overdue(task))

    incomplete_perct = (incomplete / total_tasks * 100) if total_tasks else 0
    overdue_perct = (overdue / total_tasks * 100) if total_tasks else 0

    with open("task_overview.txt", "w") as file:
        file.write("TASK OVERVIEW REPORT\n")
        file.write("-" * 25 + "\n")
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed}\n")
        file.write(f"Uncompleted tasks: {incomplete}\n")
        file.write(f"Overdue uncompleted tasks: {overdue}\n")
        file.write(f"Percentage incomplete: {incomplete_perct:.2f}%\n")
        file.write(f"Percentage overdue: {overdue_perct:.2f}%\n")


def generate_user_overview(users):
    all_tasks = [task for user in users for task in user.tasks]
    total_tasks = len(all_tasks)
    total_users = len(users)

    with open("user_overview.txt", "w") as file:
        file.write("USER OVERVIEW REPORT\n")
        file.write("-" * 25 + "\n")
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n\n")

        for user in users:
            user_tasks = user.tasks
            user_total = len(user_tasks)

            completed = sum(1 for task in user_tasks if task[5] == "Yes")
            incomplete = user_total - completed
            overdue = sum(1 for task in user_tasks if is_overdue(task))

            if total_tasks > 0:
                assigned_perct = (user_total / total_tasks) * 100
            else:
                assigned_perct = 0

            if user_total > 0:
                completed_perct = (completed / user_total) * 100
                incomplete_perct = (incomplete / user_total) * 100
                overdue_perct = (overdue / user_total) * 100
            else:
                completed_perct = 0
                incomplete_perct = 0
                overdue_perct = 0

            file.write(f"User: {user.user_name}\n")
            file.write(f"Total tasks assigned: {user_total}\n")
            file.write(f"% of all tasks assigned: {assigned_perct:.2f}%\n")
            file.write(f"% completed: {completed_perct:.2f}%\n")
            file.write(f"% incomplete: {incomplete_perct:.2f}%\n")
            file.write(f"% overdue: {overdue_perct:.2f}%\n")
            file.write("-" * 25 + "\n")


def check_report_files(users):
    # Checks whether the files are created if not it creates them
    if not (os.path.exists("task_overview.txt") and os.path.exists
            ("user_overview.txt")):
        generate_task_overview(users)
        generate_user_overview(users)


def display_report(file_name, title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)

    try:
        with open(file_name, "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("Report file not found.")


def display_statistics(users):
    check_report_files(users)

    display_report("task_overview.txt", "TASK OVERVIEW")
    display_report("user_overview.txt", "USER OVERVIEW")


# Displays when the user is admin
def admin_menu():
    choice = input("\nSelect one of the following options:\n"
                   f"{'r':<3} - register a user\n"
                   f"{'a':<3} - add task\n"
                   f"{'va':<3} - view all tasks\n"
                   f"{'vm':<3} - view my tasks\n"
                   f"{'vc':<3} - view completed tasks\n"
                   f"{'del':<3} - delete tasks\n"
                   f"{'ds':<3} - display statistics\n"
                   f"{'gr':<3} - generate reports\n"
                   f"{'e':<3} - exit\n").upper()
    return choice


def menu():
    choice = input("\nSelect one of the following options:\n"
                   f"{'a':<2} - add task\n"
                   f"{'va':<2} - view all tasks\n"
                   f"{'vm':<2} - view my tasks\n"
                   f"{'vc':<2} - view completed tasks\n"
                   f"{'e':<2} - exit\n").upper()
    return choice


read_user_data(users, user_list, task_list, user_tasks)

choice = input("Select one of the following options:\n"
               "l - login\n"
               "e - exit\n").upper()

while choice != "E":
    if choice == "L":
        attempts = 0
        current_user = None

        while attempts < 5 and not current_user:
            user_name = input("\nEnter your user name: ")
            password = input("Enter your password: ")

            current_user = authenticate(users, user_name, password)
            if not current_user:
                print("Incorrect username and/or password")
                attempts += 1

            if attempts == 5:
                print("Too many attempts, returning to main menu")
                break

            print("\nYou have successfully logged in")
            if user_name == "admin":
                choice = admin_menu()
            else:
                choice = menu()

            while choice != "E":
                if choice == "R":
                    if user_name != "admin":
                        print("Only admin may register new users")
                    else:
                        while True:
                            user_exists = False
                            new_user = input("\nPlease enter username of the "
                                             "user: ")
                            for i in users:
                                if i.user_name == new_user:
                                    user_exists = True
                                    break
                            if user_exists:
                                print("Username already exists, use "
                                      "another name")
                            else:
                                break

                        while True:
                            new_password = input("Please enter password of"
                                                 " the user: ")
                            password_check = input("Confirm password: ")

                            if new_password == password_check:
                                reg_user(users, new_user, new_password)

                                break
                            else:
                                print("\nPasswords don't match please try "
                                      "again")

                elif choice == "A":
                    line = ""
                    print("\nPlease enter the following details:")

                    while True:
                        user_exists = False
                        new_user = input("username of the user the task "
                                         "will be assigned to: ")
                        for i in users:
                            if i.user_name == new_user:
                                user_exists = True
                                break
                        if user_exists:
                            line += new_user

                            title = input("Title of the task: ")
                            line += "," + title

                            description = input("Description of the "
                                                "task: ")
                            line += "," + description

                            start = datetime.now().strftime("%d %b %Y")
                            line += "," + start

                            end = input("Due date of the task: ")
                            line += "," + end

                            completed = "No"
                            line += "," + completed

                            task = line.split(",")
                            add_task(users, new_user, task)
                            break

                        else:
                            print("User does not exist, please try "
                                  "another username")

                elif choice == "VA":
                    view_all_tasks(users)

                elif choice == "VM":
                    current_user = None
                    for user in users:
                        if user.user_name == user_name:
                            current_user = user
                            break

                    view_mine(users, user_name)

                    while True:
                        select = input("Do you want to select a task (Y/N): "
                                       ).upper()
                        if select != "Y":
                            break

                        try:
                            ID = int(input(
                                "Insert ID of task you want to select "
                                "(-1 to return): "
                            ))

                            if ID == -1:
                                break

                            task_index = ID - 1

                            if task_index < 0 or task_index >= \
                                    len(current_user.tasks):
                                print("Invalid task ID")
                                continue

                            task = current_user.tasks[task_index]

                            complete_edit = input(
                                "Mark task as complete (C) or edit (E): "
                            ).upper()

                            if complete_edit == "C":
                                if task[5] == "Yes":
                                    print("Task already completed")
                                else:
                                    task[5] = "Yes"
                                    update_tasks_file(users)
                                    print("Task marked as complete")

                            elif complete_edit == "E":
                                if task[5] == "Yes":
                                    print("Completed tasks cannot be edited")
                                    continue

                                edit_username = input("Edit user? (Y/N): "
                                                      ).upper()
                                if edit_username == "Y":
                                    new_username = input("Insert new username:"
                                                         " ")
                                    task[0] = new_username

                                edit_date = input("Edit due date? (Y/N): "
                                                  ).upper()
                                if edit_date == "Y":
                                    new_date = input("Insert new due date: ")
                                    task[4] = new_date

                                update_tasks_file(users)
                                print("Task successfully edited")

                            else:
                                print("Invalid option, choose C or E")

                            view_mine(users, user_name)

                        except ValueError:
                            print("Invalid input, please enter a number")

                elif choice == "VC":
                    view_completed(users)

                elif choice == "DEL":
                    if user_name != "admin":
                        print("Only admin may delete tasks")
                    else:
                        view_all_tasks(users)
                        while True:
                            try:
                                ID = int(input("Insert ID of task you want to "
                                               "delete: "))
                                break
                            except ValueError:
                                print("Invalid input, please isert digit")
                        delete_task(users, deleted_tasks, ID)

                        update_tasks_file(users)

                elif choice == "DS":
                    if user_name != "admin":
                        print("Only admin may view statistics")
                    else:
                        display_statistics(users)

                elif choice == "GR":
                    if user_name != "admin":
                        print("Only admin may generate reports")
                    else:
                        generate_task_overview(users)
                        generate_user_overview(users)
                        print("Reports generated successfully.")

                else:
                    print("\nInvalid input, please select from the "
                          "menu provided")

                if user_name == "admin":
                    choice = admin_menu()
                else:
                    choice = menu()

    else:
        print("Invalid input, please select from the menu "
              "provided")

    choice = input("\nSelect one of the following options:\n"
                   "l - login\n"
                   "e - exit\n").upper()
