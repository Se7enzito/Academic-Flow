import os
import sqlite3 as sql
from backend.libs.db.encryption import CriptografiaDados

encrypt = CriptografiaDados()

class Conexao:
    def __init__(self) -> None:
        self.database = os.path.join("backend", "libs", "db", "database.db")
        self.connection = None
        self.cursor = None
    
    def conectar(self) -> None:
        self.connection = sql.connect(self.database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        if self.connection:
            self.connection.close()
        
    def criarTabelas(self) -> None:
        self.conectar()
        
        # Tables
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula INTEGER NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
            );""")
        
        # Configs
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        
        self.connection.commit()
        self.desconectar()
        
    def registrarUser(self, matricula: int, user: str, email: str, senha: str) -> bool:
        self.conectar()
        
        senha_criptografada = encrypt.criptografar(senha)
        
        try:
            self.cursor.execute(
                "INSERT INTO users (matricula, nome, email, senha) VALUES (?, ?, ?, ?);", 
                (matricula, user, email, senha_criptografada)
            )
            self.connection.commit()
            sucesso = True
        except sql.IntegrityError:
            sucesso = False
        
        self.desconectar()
        return sucesso
    
    def loginUser(self, matricula: int, senha: str) -> bool:
        self.conectar()
        
        self.cursor.execute("SELECT senha FROM users WHERE matricula = ?;", (matricula,))
        resultado = self.cursor.fetchone()
        
        if not resultado:
            self.desconectar()
            return False
        
        senha_criptografada = resultado[0]
        senha_real = encrypt.descriptografar(senha_criptografada)
        
        self.desconectar()
        return senha_real == senha
    
    def getIdUser(self, email: str) -> int:
        self.conectar()
        
        resultado = self.cursor.execute("SELECT id FROM users WHERE email = ?;", (email,)).fetchone()
        
        self.desconectar()
        return resultado[0] if resultado else -1
    
    def checkSenhaUser(self, id: int, senha: str) -> bool:
        self.conectar()
        
        self.cursor.execute("SELECT senha FROM users WHERE id = ?;", (id,))
        resultado = self.cursor.fetchone()
        
        if not resultado:
            self.desconectar()
            return False
        
        senha_criptografada = resultado[0]
        senha_real = encrypt.descriptografar(senha_criptografada)
        
        self.desconectar()
        return senha_real == senha

if __name__ == "__main__":
    pass