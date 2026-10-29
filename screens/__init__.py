from .alunos import StudentListScreen
from .alterar_senha import ChangeDemoPasswordScreen
from .configuracao_inicial import InitialSetupScreen
from .cadastro import RegisterStudentScreen
from .cursos import CourseScreen
from .detalhes import StudentDetailScreen
from .editar import EditStudentScreen
from .historico import HistoryScreen
from .home import HomeScreen
from .login import LoginScreen
from .manager import ClassBaseScreenManager

__all__ = [
    "ClassBaseScreenManager",
    "LoginScreen",
    "InitialSetupScreen",
    "ChangeDemoPasswordScreen",
    "HomeScreen",
    "RegisterStudentScreen",
    "StudentListScreen",
    "StudentDetailScreen",
    "EditStudentScreen",
    "CourseScreen",
    "HistoryScreen",
]
