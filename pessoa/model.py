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

    def atualiza_endereco(self, endereco_id):
        self.estado = self.conexao.select_id('pessoa_estado', 'estado', self.estado)[0]
        self.tipo_endereco = self.conexao.select_id('pessoa_tipoendereco', 'tipo_endereco', self.tipo_endereco)[0]

        parcela = ''

        if self.rua:
            parcela += f"rua='{self.rua}', "
        if self.numero:
            parcela += f"numero='{self.numero}', '"
        if self.bairro:
            parcela += f"bairro='{self.bairro}', "
        if self.cep:
            parcela += f"cep='{self.cep}', "
        if self.cidade:
            parcela += f"cidade='{self.cidade}', "

        parcela += f"estado_id={self.estado}, tipo_endereco_id={self.tipo_endereco}"

        comando_sql = f"UPDATE pessoa_endereco SET {parcela} WHERE id={endereco_id}"
        # comando_sql = f"UPDATE pessoa_endereco SET rua='{self.rua}', numero='{self.numero}', bairro='{self.bairro}', " \
        #               f"cep='{self.cep}', cidade='{self.cidade}', estado_id={self.estado}, tipo_endereco_id={self.tipo_endereco} " \
        #               f"WHERE id={endereco_id}"
        print(comando_sql)
        self.conexao.executa_update(comando_sql=comando_sql)


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
        # self.cadastrar_pessoa()

    def restricao_pessoa(self):
        print('ola')
        pass

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

        comando_sql = 'SELECT id FROM pessoa_pessoa ORDER BY id DESC LIMIT 1'
        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

    def atualiza_pessoa(self, id=None, nome=None, sobrenome=None, data_nascimento=None,
                        genero=None, endereco=None, estado_civil=None):
        print(id)
        print(self.id)
        if self.id and not id:
            id = self.id

        comando_sql = f'SELECT endereco_id FROM pessoa_pessoa WHERE id={id}'
        endereco_id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

        parcela = ''

        if nome:
            parcela += f"nome='{nome}', "
        if sobrenome:
            parcela += f"sobrenome='{sobrenome}', "
        if data_nascimento:
            parcela += f"data_nascimento='{data_nascimento}', "
        if genero:
            parcela += f"genero_id={self.conexao.select_id('pessoa_genero', 'genero', genero)[0]}, "
        if endereco:
            endereco.atualiza_endereco(endereco_id=endereco_id)
            parcela += f"endereco_id={endereco_id}, "
        if estado_civil:
            parcela += f"estado_civil_id={self.conexao.select_id('pessoa_estadocivil', 'estado_civil', estado_civil)[0]}"

        comando_sql = f"UPDATE pessoa_pessoa SET {parcela} WHERE id={id}"
        print(comando_sql)
        self.conexao.executa_update(comando_sql=comando_sql)


class Usuario(PessoaUtil, object):
    def __init__(self, pessoa=None, usuario=None, email=None, senha=None, tipo_usuario=None):
        super().__init__()
        self.id = None
        self.pessoa = pessoa
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.tipo_usuario = tipo_usuario
        # self.cadastrar_usuario()

    def criptografa_senha(self):
        senha_criptografada = bcrypt.hashpw(
            str(self.senha).encode('utf-8'), bcrypt.gensalt())
        return senha_criptografada

    def cadastrar_usuario(self):
        self.usuario = f'{self.pessoa.nome}{self.pessoa.sobrenome}'
        self.email = f'{self.pessoa.nome}{self.pessoa.sobrenome}@educamais.com'
        self.senha = f'{self.pessoa.nome}@{self.pessoa.cpf}'

        comando_sql = "INSERT INTO pessoa_usuario (usuario, email, senha, pessoa_id, tipo_usuario_id) VALUES (%s, %s, %s, %s, %s)"

        tupla = (
            self.usuario,
            self.email,
            self.criptografa_senha(),
            self.pessoa.id,
            self.tipo_usuario,
        )
        print(tupla)

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla
        )

        comando_sql = 'SELECT id FROM pessoa_usuario ORDER BY id DESC LIMIT 1'
        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

    def atualiza_senha(self, senha_nova=None):
        self.senha = senha_nova
        comando_sql = f"UPDATE pessoa_usuario SET senha='{str(self.criptografa_senha())[2:-1]}' WHERE id={self.id}"
        self.conexao.executa_update(comando_sql=comando_sql)
