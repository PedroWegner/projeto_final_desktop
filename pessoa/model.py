"""
DOCUMENTAR
"""
from banco_dados.model import ConexaoBD
from datetime import datetime
import bcrypt
import re


class InformacaoErrada(Exception):
    def __init__(self, messagem):
        super().__init__(messagem)


class PessoaUtil(object):
    def __init__(self):
        self.conexao = ConexaoBD()


class TipoEndereco(object):
    def __init__(self, tipo_endereco=None):
        self.id = None
        self.tipo_endereco = tipo_endereco


class Estado(object):
    def __init__(self, estado=None):
        self.id = None
        self.estado = estado


class TipoPerfil(object):
    def __init__(self, tipo_perfil=None):
        self.id = None
        self.tipo_perfil = tipo_perfil


class Endereco(PessoaUtil, object):
    def __init__(self, rua=None, numero=None, bairro=None, cep=None, cidade=None,
                 tipo_endereco=None, estado=None):
        super().__init__()
        self.restricao_endereco()
        self.id = None
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade
        self.tipo_endereco = tipo_endereco
        self.estado = estado

    def restricao_endereco(self):
        print("estou na restrição do endereço")

    def cadastrar_endereco(self):
        # self.checa_validade()
        comando_sql = "INSERT INTO pessoa_endereco (rua, numero, bairro, cep, cidade, estado_id, tipo_endereco_id) VALUES" \
                      "(%s, %s, %s, %s , %s, %s , %s)"
        tupla = (
            self.rua,
            self.numero,
            self.bairro,
            self.cep,
            self.cidade,
            self.conexao.select_id('pessoa_estado', 'estado', self.estado)[0],
            self.conexao.select_id('pessoa_tipoendereco',
                                   'tipo_endereco', self.tipo_endereco)[0]
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla
        )

        comando_sql = 'SELECT id FROM pessoa_endereco ORDER BY id DESC LIMIT 1'
        # esse 0 indica que pegarei primeiro elemento da tupla
        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]


class Pessoa(PessoaUtil, object):
    def __init__(self, nome=None, sobrenome=None, data_nascimento=None,
                 genero=None, cpf=None, data_cadastro=None, endereco=None, estado_civil=None):
        super().__init__()
        self.restricao_pessoa()
        self.id = None
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.cpf = cpf
        self.data_cadastro = data_cadastro
        self.endereco = endereco
        self.estado_civil = estado_civil
        self.data_cadastro = datetime.now()


    def restricao_pessoa(self):
        print('ola')
        pass

    # def cria_usuario(self):
    #     print("Entrei no criar usuario")
    #     first_name = self.nome
    #     last_name = self.sobrenome
    #     username = f'{self.nome}{self.sobrenome}.aluno'.lower()
    #     email_inst = f'{self.nome}{self.sobrenome}@aluno.com'.lower()
    #     senha = f'{self.cpf}{self.sobrenome}'.lower()
    #     senha_cript = (hashlib.sha256(senha.encode()).hexdigest())
    #     print(senha)
    #     print(senha_cript)
    #
    #     comando_sql = "INSERT INTO auth_user (password, username, first_name, last_name, email, date_joined, is_staff, is_active, is_superuser)" \
    #                   "VALUES (%s, %s, %s, %s, %s, %s, 1, 1, 1)"
    #     tupla = (
    #         senha_cript,
    #         username,
    #         first_name,
    #         last_name,
    #         email_inst,
    #         self.data_cadastro
    #     )
    #
    #     self.conexao.executa_insert(
    #         comando_sql=comando_sql,
    #         tupla=tupla
    #     )

    def cadastrar_pessoa(self):
        self.endereco.cadastrar_endereco()

        self.endereco = self.endereco.id
        comando_sql = "INSERT INTO pessoa_pessoa (nome, sobrenome, data_nascimento, cpf, data_cadastro, estado_civil_id, endereco_id, genero_id) VALUES" \
                      "(%s, %s, %s, %s , %s, %s, %s, %s)"
        tupla = (
            self.nome,
            self.sobrenome,
            self.data_nascimento,
            self.cpf,
            self.data_cadastro,
            self.conexao.select_id('pessoa_estadocivil',
                                   'estado_civil', self.estado_civil)[0],
            self.endereco,
            self.conexao.select_id('pessoa_genero', 'genero', self.genero)[0]
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla
        )

    def retorna_ultima_pessoa(self):
        comando_sql = 'SELECT * FROM pessoa_pessoa ORDER BY id DESC LIMIT 1'
        result = self.conexao.executa_fetchone(comando_sql=comando_sql)
        self.id = result[0]
        self.nome = result[1]
        self.sobrenome = result[2]
        self.data_nascimento = result[3]
        self.cpf = result[4]
        self.data_cadastro = result[5]
        self.estado_civil = result[6]
        self.endereco = result[7]
        self.genero = result[8]


class Usuario(PessoaUtil, object):
    def __init__(self, pessoa=None, usuario=None, email=None, senha=None, tipo_perfil=None):
        super().__init__()
        self.id = None
        self.pessoa = pessoa
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.tipo_perfil = tipo_perfil

    def criptografa_senha(self):
        senha_criptografada = bcrypt.hashpw(
            str(self.senha).encode('utf-8'), bcrypt.gensalt())
        return senha_criptografada

    def cria_usuario(self):
        self.pessoa = Pessoa()
        self.pessoa.retorna_ultima_pessoa()
        self.usuario = f'{self.pessoa.nome}{self.pessoa.sobrenome}'
        self.email = f'{self.pessoa.nome}{self.pessoa.sobrenome}@educamais.com'
        self.senha = f'{self.pessoa.nome}@{self.pessoa.cpf}'

        comando_sql = "INSERT INTO pessoa_usuario (usuario, email, senha, pessoa_id, tipo_perfil_id) VALUES (%s, %s, %s, %s, %s)"

        tupla = (
            self.usuario,
            self.email,
            self.criptografa_senha(),
            self.pessoa.id,
            1
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla
        )
