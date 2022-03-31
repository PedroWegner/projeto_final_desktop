from banco_dados.model import ConexaoBD
from PyQt5.QtWidgets import QLineEdit, QFileDialog
from pessoa.model import Usuario, Pessoa, Endereco
import bcrypt
import os
import shutil


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
            print('input dep')
            print(e)

    def input_lingua(self, input=None):
        try:
            input.clear()
            comando_sql = "SELECT * FROM departamento_lingua"
            linguas = self.conexao.select_all(comando_sql=comando_sql)
            for lingua in linguas:
                input.addItem(lingua[1])
        except Exception as e:
            print('input lingua')
            print(e)

    def input_nivel(self, input=None):
        try:
            input.clear()
            comando_sql = "SELECT * FROM departamento_nivellingua"
            niveis = self.conexao.select_all(comando_sql=comando_sql)
            for nivel in niveis:
                input.addItem(nivel[1])
        except Exception as e:
            print('input nivel')
            print(e)

    def input_modulo(self, input=None):
        input.clear()
        comando_sql = "SELECT DeMo.cod_modulo, DeMo.modulo, DeLi.lingua " \
                      "FROM departamento_modulo DeMo " \
                      "INNER JOIN departamento_lingua DeLi " \
                      "ON DeMo.lingua_id = DeLi.id;"
        modulos = self.conexao.select_all(comando_sql=comando_sql)
        for modulo in modulos:
            input.addItem(f'{modulo[0]} - {modulo[1]}, {modulo[2]}')

    def input_aluno(self, input=None):
        try:
            input.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_aluno DeAl " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DeAl.pessoa_id = PePe.id;"
            alunos = self.conexao.select_all(comando_sql=comando_sql)
            for aluno in alunos:
                input.addItem(f'{aluno[0]} {aluno[1]}')
        except Exception as e:
            print(e)

    def input_professor(self, input=None):
        try:
            input.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_professor DePr " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DePr.pessoa_id = PePe.id "
            professores = self.conexao.select_all(comando_sql=comando_sql)
            for professor in professores:
                input.addItem(f'{professor[0]} {professor[1]}')
        except Exception as e:
            print('input prof')
            print(e)

    def input_professor_modulo(self, input=None, nome=None, sobrenome=None):
        input.clear()
        comando_sql = f"SELECT DeNiLi.valor_nivel, DePr.lingua_id, DePr.id " \
                      f"FROM departamento_nivellingua DeNiLi " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DePr.nivel_id = DeNiLi.id " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DePr.pessoa_id = PePe.id " \
                      f"WHERE PePe.nome='{nome}' AND PePe.sobrenome='{sobrenome}'"
        dados = self.conexao.executa_fetchone(comando_sql=comando_sql)
        nivel_professor = dados[0]
        lingua_professor = dados[1]
        id_professor = dados[2]

        comando_sql = f"SELECT DeMo.modulo, DeLi.lingua " \
                      f"FROM departamento_modulo DeMo " \
                      f"INNER JOIN departamento_nivellingua DeNiLi " \
                      f"ON DeMo.nivel_id = DeNiLi.id " \
                      f"INNER JOIN departamento_lingua DeLi " \
                      f"ON DeLi.id = DeMo.lingua_id " \
                      f"WHERE DeNiLi.valor_nivel <= {nivel_professor} AND lingua_id = {lingua_professor} " \
                      f"AND NOT EXISTS (SELECT * " \
                      f"FROM departamento_professor_modulo DePrMo " \
                      f"WHERE DeMo.id = DePrMo.modulo_id AND DePrMo.professor_id={id_professor});"
        modulos = self.conexao.select_all(comando_sql=comando_sql)
        for modulo in modulos:
            input.addItem(f'{modulo[0]} - {modulo[1]}')

    def input_aluno_modulo(self, input=None, nome=None, sobrenome=None):
        input.clear()
        comando_sql = f"SELECT DeAl.id " \
                      f"FROM departamento_aluno DeAl " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DeAl.pessoa_id = PePe.id " \
                      f"WHERE PePe.nome='{nome}' AND PePe.sobrenome='{sobrenome}'"
        id_aluno = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
        comando_sql = f"SELECT DeMo.modulo, DeLi.lingua " \
                      f"FROM departamento_modulo DeMo " \
                      f"INNER JOIN departamento_lingua DeLi " \
                      f"ON DeMo.lingua_id = DeLi.id " \
                      f"WHERE NOT EXISTS (SELECT * " \
                      f"FROM departamento_aluno_modulo DeAlMo " \
                      f"WHERE DeMo.id = DeAlMo.modulo_id AND DeAlMo.aluno_id={id_aluno});"
        modulos = self.conexao.select_all(comando_sql=comando_sql)
        for modulo in modulos:
            input.addItem(f"{modulo[0]} - {modulo[1]}")

    def input_genero(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM pessoa_genero"
        generos = self.conexao.select_all(comando_sql)
        for genero in generos:
            input.addItem(genero[1])

    def input_estado_civil(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM pessoa_estadocivil"
        estados_civil = self.conexao.select_all(comando_sql)
        for estado_civil in estados_civil:
            input.addItem(estado_civil[1])

    def input_estado(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM pessoa_estado"
        estados = self.conexao.select_all(comando_sql)
        for estado in estados:
            input.addItem(estado[1])

    def input_tipo_endereco(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM pessoa_tipoendereco"
        tipos_endereco = self.conexao.select_all(comando_sql)
        for tipo_endereco in tipos_endereco:
            input.addItem(tipo_endereco[1])
    # FIM DOS INPUTS #

    # FUNCOES LIMPA DE CAMPO #
    def limpa_pessoa(self, rua=None, numero=None, bairro=None, cep=None, cidade=None, nome=None, sobrenome=None,
                     data_nasc=None, cpf=None, celular=None):
        rua.clear()
        numero.clear()
        bairro.clear()
        cep.clear()
        cidade.clear()
        nome.clear()
        sobrenome.clear()
        data_nasc.clear()
        celular.clear()
        if cpf:
            cpf.clear()

    # FIM FUNCOES LIMPA DE CAMPO #

    # FUNCOES GLOBAIS #

    # DADOS
    def att_dados(self, input_nome=None, input_sobrenome=None, input_data_nasc=None, input_genero=None,
                       input_estado_civil=None, input_rua=None,
                       input_numero=None, input_bairro=None, input_cep=None, input_cidade=None, input_estado=None,
                       input_tipo_end=None):
        try:
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
        except Exception as e:
            print(e)


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

#         # FIM SENHA #

    def arquivo(self, input=None):
        diretorio, extensao = os.path.splitext(input.displayText())
        nome_arquivo = diretorio.split('/')[-1]
        return nome_arquivo + extensao

    def copia_arquivo(self, dict=None, input=None):
        caminho_ano = fr"C:\Users\pedro\Desktop\Trabalho Final Senai\trabalho_final_web\media\{dict['pasta_especifica']}\{dict['ano']}"
        caminho_mes = fr"C:\Users\pedro\Desktop\Trabalho Final Senai\trabalho_final_web\media\{dict['pasta_especifica']}\{dict['ano']}\{dict['mes']}"

        if not os.path.isdir(caminho_ano):
            os.mkdir(caminho_ano)

        if not os.path.isdir(caminho_mes):
            os.mkdir(caminho_mes)

        caminho_antigo = input.displayText()
        caminho_novo = os.path.join(caminho_mes, dict['arquivo']) # AQUI POSSO ALTERAR COMO ESSE ARQUIVO SERA SALVO!!!!!
        shutil.copy(caminho_antigo, caminho_novo)

    def seleciona_arquivo(self, input=None):
        try:
            arquivo, _ = QFileDialog.getOpenFileName(
                parent=self.menu_stacked,
                caption='Abrir arquivo',
                directory=r'C:\Users\pedro\Desktop'
            )

            input.setText(arquivo)
        except Exception as e:
            print(e)
#
#
class DadosPessoa(MenuBase):
    def __init__(self, usuario_logado=None):
        super().__init__(usuario_logado=usuario_logado)
#
#     # CONTRUTORES DE TELA #
    def att_dados_construtor(self):
        try:
            self.input_estado(input=self.att_dados_input_estado)
            self.input_genero(input=self.att_dados_input_genero)
            self.input_estado_civil(input=self.att_dados_input_estado_civil)
            self.input_tipo_endereco(input=self.att_dados_input_tipo_end)
        except Exception as e:
            print(e)
#     # FIM CONTRUTORES DE TELA #
#
#     # FUNCOES DE TELA #
#     # ATT DADOS #
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

#     # FIM ATT DADOS #
#
#     # SENHA #
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

#     # FIM FUNCOES DE TELA #
#
#     # FUNCOES DE LIMPA CAMPO #
    def limpa_att_senha(self):
        self.att_senha_input_senha_antiga.clear()
        self.att_senha_input_verifica_1.clear()
        self.att_senha_input_verifica_2.clear()

    def limpa_att_dados(self):
        try:
            self.limpa_pessoa(
                rua=self.att_dados_input_rua,
                numero=self.att_dados_input_numero,
                bairro=self.att_dados_input_bairro,
                cep=self.att_dados_input_cep,
                cidade=self.att_dados_input_cidade,
                nome=self.att_dados_input_nome,
                sobrenome=self.att_dados_input_sobrenome,
                data_nasc=self.att_dados_input_data_nasc,
                celular=self.att_dados_input_celular,
            )
        except Exception as e:
            print(e)
    # FIM FUNCOES DE LIMPA CAMPO #

if __name__ == '__main__':
    pass
