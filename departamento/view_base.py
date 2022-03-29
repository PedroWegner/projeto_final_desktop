from banco_dados.model import ConexaoBD
from PyQt5.QtWidgets import QLineEdit
from pessoa.model import Usuario, Pessoa, Endereco
import bcrypt


class MenuBase:
    def __init__(self, usuario_logado=None):
        self.conexao = ConexaoBD()
        self.usuario_logado = usuario_logado

    # FUNCOES INPUTS #
    def input_departamento(self, input=None):
        try:
            input.clear()
            comando_sql = "SELECT * FROM departamento_departamento"
            departamentos = self.conexao.select_all(comando_sql=comando_sql)
            for departamento in departamentos:
                input.addItem(departamento[1])
        except Exception as e:
            print(e)

    def input_turno(self, input=None):
        try:
            comando_sql = "SELECT * FROM departamento_turno"
            turnos = self.conexao.select_all(comando_sql=comando_sql)
            for turno in turnos:
                input.addItem(turno[1])
        except Exception as e:
            print(e)

    def input_professor(self, input=None, input_dep=None):
        try:
            input.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_departamento DeDe " \
                          f"INNER JOIN departamento_professor_departamento DePrDe " \
                          f"ON DeDe.id = DePrDe.departamento_id " \
                          f"INNER JOIN departamento_professor DePr " \
                          f"ON DePr.id = DePrDe.professor_id " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DePr.pessoa_id = PePe.id " \
                          f"WHERE DeDe.departamento='{input_dep.currentText()}';"
            professores = self.conexao.select_all(comando_sql=comando_sql)
            for professor in professores:
                input.addItem(f'{professor[0]} {professor[1]}')
        except Exception as e:
            print(e)

    def input_curso(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM departamento_curso"
        cursos = self.conexao.select_all(comando_sql=comando_sql)
        for curso in cursos:
            input.addItem(curso[1])

    def input_titulo(self, input=None):
        comando_sql = "SELECT * FROM departamento_tituloprofessor"
        titulos = self.conexao.select_all(comando_sql=comando_sql)
        for titulo in titulos:
            input.addItem(titulo[1])

    def input_genero(self, input=None):
        comando_sql = "SELECT * FROM pessoa_genero"
        generos = self.conexao.select_all(comando_sql)
        for genero in generos:
            input.addItem(genero[1])

    def input_estado_civil(self, input=None):
        comando_sql = "SELECT * FROM pessoa_estadocivil"
        estados_civil = self.conexao.select_all(comando_sql)
        for estado_civil in estados_civil:
            input.addItem(estado_civil[1])

    def input_estado(self, input=None):
        comando_sql = "SELECT * FROM pessoa_estado"
        estados = self.conexao.select_all(comando_sql)
        for estado in estados:
            input.addItem(estado[1])

    def input_tipo_endereco(self, input=None):
        comando_sql = "SELECT * FROM pessoa_tipoendereco"
        tipos_endereco = self.conexao.select_all(comando_sql)
        for tipo_endereco in tipos_endereco:
            input.addItem(tipo_endereco[1])

    def input_disciplinas(self, input=None):
        input.clear()
        comando_sql = f"SELECT DeDi.disciplina " \
                      f"FROM departamento_disciplina DeDi " \
                      f"WHERE NOT EXISTS (" \
                      f"SELECT * " \
                      f"FROM departamento_aluno_disciplina DeAlDi " \
                      f"WHERE DeDi.id = DeAlDi.disciplina_id AND DeAlDi.aluno_id={self.usuario_logado['id_aluno']}" \
                      f")"
        print(comando_sql)
        disciplinas = self.conexao.select_all(comando_sql=comando_sql)
        for disciplina in disciplinas:
            input.addItem(disciplina[0])

    # FIM DOS INPUTS #

    # FUNCOES LIMPA DE CAMPO #
    def limpa_pessoa(self, rua=None, numero=None, bairro=None, cep=None, cidade=None, nome=None, sobrenome=None,
                     data_nasc=None, cpf=None):
        rua.clear()
        numero.clear()
        bairro.clear()
        cep.clear()
        cidade.clear()
        nome.clear()
        sobrenome.clear()
        data_nasc.clear()
        if cpf:
            cpf.clear()

    # FIM FUNCOES LIMPA DE CAMPO #

    # FUNCOES GLOBAIS #

    # DADOS
    def att_dados(self, input_nome=None, input_sobrenome=None, input_data_nasc=None, input_genero=None,
                       input_estado_civil=None, input_rua=None,
                       input_numero=None, input_bairro=None, input_cep=None, input_cidade=None, input_estado=None,
                       input_tipo_end=None):
        pessoa = Pessoa()
        pessoa.id = self.usuario_logado['id_pessoa']
        pessoa.atualiza_pessoa(
            nome=input_nome.displayText(),
            sobrenome=input_sobrenome.displayText(),
            data_nascimento=input_data_nasc.displayText(),
            genero=input_genero.currentText(),
            estado_civil=input_estado_civil.currentText(),
            endereco=Endereco(
                rua=input_rua.displayText(),
                numero=input_numero.displayText(),
                bairro=input_bairro.displayText(),
                cep=input_cep.displayText(),
                cidade=input_cidade.displayText(),
                estado=input_estado.currentText(),
                tipo_endereco=input_tipo_end.currentText(),
            )
        )
        self.usuario_logado['nome_pessoa'] = input_nome.displayText()
        self.usuario_logado['sobrenome_pessoa'] = input_sobrenome.displayText()
        self.usuario_logado['data_nasc_pessoa'] = input_data_nasc.displayText()


    # FIM DADOS

    # SENHA
    def visualizar_senha(self, tupla_senha=None):
        try:
            for campo in tupla_senha:
                campo.setEchoMode(QLineEdit.Normal)
        except Exception as e:
            print(e)


    def atualizar_senha(self, input_senha_antiga=None, input_senha_nova_1=None, input_senha_nova_2=None):
        comando_sql = f"SELECT senha FROM pessoa_usuario WHERE usuario='{self.usuario_logado['usuario']}'"
        senha_criptografada = None
        senha_antiga = input_senha_antiga.text()
        senha_nova_1 = input_senha_nova_1.text()
        senha_nova_2 = input_senha_nova_2.text()

        try:
            senha_criptografada = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
        except:
            print('deu erro')
            return

        if bcrypt.checkpw(senha_antiga.encode('utf-8'), senha_criptografada.encode('utf-8')):
            if senha_nova_1 == senha_nova_2:
                usuario = Usuario()
                usuario.id = self.usuario_logado['id_usuario']
                usuario.atualiza_senha(senha_nova=senha_nova_1)
            else:
                print("Senhas incompativeis")  # AQUI QUE FAZ UM TROÇO PARA FALAR QUE DEU ERRADO!

        # FIM SENHA #


class DadosPessoa(MenuBase):
    def __init__(self, usuario_logado=None):
        super().__init__(usuario_logado=usuario_logado)

    # CONTRUTORES DE TELA #
    def att_dados_construtor(self):
        try:
            self.input_estado(input=self.att_dados_input_estado)
            self.input_genero(input=self.att_dados_input_genero)
            self.input_estado_civil(input=self.att_dados_input_estado_civil)
            self.input_tipo_endereco(input=self.att_dados_input_tipo_end)
        except Exception as e:
            print(e)
    # FIM CONTRUTORES DE TELA #

    # FUNCOES DE TELA #
    # ATT DADOS #
    def att_dados(self):
        super().att_dados(
            input_nome=self.att_dados_input_nome,
            input_sobrenome=self.att_dados_input_sobrenome,
            input_data_nasc=self.att_dados_input_data_nasc,
            input_genero=self.att_dados_input_genero,
            input_estado_civil=self.att_dados_input_estado_civil,
            input_rua=self.att_dados_input_rua,
            input_numero=self.att_dados_input_numero,
            input_bairro=self.att_dados_input_bairro,
            input_cep=self.att_dados_input_cep,
            input_cidade=self.att_dados_input_cidade,
            input_estado=self.att_dados_input_estado,
            input_tipo_end=self.att_dados_input_tipo_end,
        )

    # FIM ATT DADOS #

    # SENHA #
    def visualizar_senha(self):
        super().visualizar_senha(
            (
                self.att_senha_input_senha_antiga,
                self.att_senha_input_verifica_1,
                self.att_senha_input_verifica_2,
            )
        )

    def atualizar_senha(self):
        super().atualizar_senha(
            input_senha_antiga=self.att_senha_input_senha_antiga,
            input_senha_nova_1=self.att_senha_input_verifica_1,
            input_senha_nova_2=self.att_senha_input_verifica_2,
        )

    # FIM FUNCOES DE TELA #

    # FUNCOES DE LIMPA CAMPO #
    def limpa_att_senha(self):
        self.att_senha_input_senha_antiga.clear()
        self.att_senha_input_verifica_1.clear()
        self.att_senha_input_verifica_2.clear()

    def limpa_att_dados(self):
        self.limpa_pessoa(
            rua=self.att_dados_input_rua,
            numero=self.att_dados_input_numero,
            bairro=self.att_dados_input_bairro,
            cep=self.att_dados_input_cep,
            cidade=self.att_dados_input_cidade,
            nome=self.att_dados_input_nome,
            sobrenome=self.att_dados_input_sobrenome,
            data_nasc=self.att_dados_input_data_nasc,
        )
    # FIM FUNCOES DE LIMPA CAMPO #

if __name__ == '__main__':
    pass
