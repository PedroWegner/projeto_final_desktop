from PyQt5 import uic, QtWidgets
from departamento.views import UtilDepartamento


class TelaDisciplina(UtilDepartamento):
    def __init__(self, disciplina=None, usuario_logado=None):
        super().__init__()
        self.view = None
        self.disciplina = disciplina
        self.usuario_logado = usuario_logado
        self.dict_disciplina = None
        self.dicionario_disciplina()

    def dicionario_disciplina(self):
        comando_sql = f"SELECT DeDi.id, DeDi.disciplina, DeDi.cod_disciplina, DeDi.departamento_id, DeDi.professor_id, " \
                      f"PePe.nome, PePe.sobrenome " \
                      f"FROM departamento_disciplina DeDi " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DeDi.professor_id = DePr.id " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON PePe.id = DePr.pessoa_id " \
                      f"WHERE disciplina='{self.disciplina}'"
        disciplina = self.conexao.executa_fetchone(comando_sql=comando_sql)
        self.dict_disciplina = {
            'id_disciplina': disciplina[0],
            'disciplina': disciplina[1],
            'cod_disciplina': disciplina[2],
            'dep_disciplina': disciplina[3],
            'prof_disciplina': disciplina[4],
            'nome_prof': disciplina[5],
            'sobrenome_prof': disciplina[6],
        }


class TelaDisciplinaProfessor(TelaDisciplina):
    def __init__(self, disciplina=None, usuario_logado=None):
        super().__init__(disciplina=disciplina, usuario_logado=usuario_logado)
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_disciplina.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.disciplina_label.setText(self.disciplina)
        self.alunos_matriculados()
        self.view.bem_vindo.setText(
            f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")

    def alunos_matriculados(self):
        self.view.alunos_matriculados.clear()
        comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                      f"FROM departamento_aluno_disciplina DeAlDi " \
                      f"INNER JOIN departamento_aluno DeAl " \
                      f"ON DeAlDi.aluno_id = DeAl.id " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DeAl.pessoa_id = PePe.id " \
                      f"WHERE DeAlDi.disciplina_id={self.dict_disciplina['id_disciplina']};"
        alunos_matriculados = self.conexao.select_all(comando_sql=comando_sql)
        for aluno in alunos_matriculados:
            self.view.alunos_matriculados.addItem(f"{aluno[0]} {aluno[1]}")


class TelaDisciplinaAluno(TelaDisciplina):
    def __init__(self, disciplina=None, usuario_logado=None):
        super().__init__(disciplina=disciplina, usuario_logado=usuario_logado)
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_disciplina_aluno.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.disciplina_label.setText(f"Bem-vindo {self.usuario_logado['nome_pessoa']} "
                                           f"{self.usuario_logado['sobrenome_pessoa']} à disciplina '{self.dict_disciplina['disciplina']}'")
        self.view.prof_label.setText(f"Seu professor é {self.dict_disciplina['nome_prof']} {self.dict_disciplina['sobrenome_prof']}")

