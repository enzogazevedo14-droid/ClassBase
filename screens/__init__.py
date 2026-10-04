from .alunos import StudentListScreen
from .cadastro import COURSES, RegisterStudentScreen
from .editar import EditStudentScreen
from .home import HomeScreen
from .login import LoginScreen
from .manager import ClassBaseScreenManager

__all__ = [
    "ClassBaseScreenManager",
    "LoginScreen",
    "HomeScreen",
    "RegisterStudentScreen",
    "StudentListScreen",
    "EditStudentScreen",
    "COURSES",
]
