class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'User not correct password'


class TokenExpired(Exception):
    detail = 'Token has expired'


class TokenNotCorrect(Exception):
    detail = 'Token is not correct'


class TaskNotFoundException(Exception):
    detail = 'Task is not found'


class TasksNotFoundException(Exception):
    detail = 'Tasks is not found'


class TaskStatusNotCorrect(Exception):
    detail = 'Status of task is not correct'


class CategoryNotFoundException(Exception):
    detail = 'Category is not found'


class UsersCategoryNameShouldBeUniqueException(Exception):
    detail = 'User category names should be unique'
