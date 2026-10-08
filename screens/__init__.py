from .alunos import StudentListScreen
from .cadastro import RegisterStudentScreen
from .cursos import CourseScreen
from .detalhes import StudentDetailScreen
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
    "StudentDetailScreen",
    "EditStudentScreen",
    "CourseScreen",
]
