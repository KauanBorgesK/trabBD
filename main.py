import sqlite3
from datetime import date

# Conectar ao banco de dados
conn = sqlite3.connect("gestao_academica.db")
cursor = conn.cursor()

# Função para criar tabelas
def criar_tabelas():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estudante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            curso TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Curso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            carga_horaria INTEGER NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matricula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_estudante INTEGER NOT NULL,
            id_curso INTEGER NOT NULL,
            data_matricula DATE NOT NULL,
            FOREIGN KEY (id_estudante) REFERENCES Estudante(id),
            FOREIGN KEY (id_curso) REFERENCES Curso(id)
        )
        """)
        conn.commit()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print("Erro ao criar tabelas:", e)

# CRUD para Estudante
def criar_estudante():
    nome = input("Digite o nome do estudante: ")
    email = input("Digite o email do estudante: ")
    curso = input("Digite o curso do estudante: ")
    try:
        cursor.execute("""
        INSERT INTO Estudante (nome, email, curso)
        VALUES (?, ?, ?)
        """, (nome, email, curso))
        conn.commit()
        print(f"Estudante '{nome}' criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: O e-mail fornecido já está cadastrado!")
    except Exception as e:
        print("Erro ao criar estudante:", e)

def listar_estudantes():
    try:
        cursor.execute("SELECT * FROM Estudante")
        estudantes = cursor.fetchall()
        if estudantes:
            print("Estudantes cadastrados:")
            for estudante in estudantes:
                print(estudante)
        else:
            print("Nenhum estudante encontrado.")
    except Exception as e:
        print("Erro ao listar estudantes:", e)

def atualizar_estudante():
    id = input("Digite o ID do estudante que deseja atualizar: ")
    nome = input("Novo nome (deixe em branco para não alterar): ")
    email = input("Novo email (deixe em branco para não alterar): ")
    curso = input("Novo curso (deixe em branco para não alterar): ")
    try:
        if nome:
            cursor.execute("UPDATE Estudante SET nome = ? WHERE id = ?", (nome, id))
        if email:
            cursor.execute("UPDATE Estudante SET email = ? WHERE id = ?", (email, id))
        if curso:
            cursor.execute("UPDATE Estudante SET curso = ? WHERE id = ?", (curso, id))
        conn.commit()
        print(f"Estudante ID {id} atualizado com sucesso!")
    except Exception as e:
        print("Erro ao atualizar estudante:", e)

def deletar_estudante():
    id = input("Digite o ID do estudante que deseja deletar: ")
    try:
        cursor.execute("DELETE FROM Estudante WHERE id = ?", (id,))
        conn.commit()
        print(f"Estudante ID {id} deletado com sucesso!")
    except Exception as e:
        print("Erro ao deletar estudante:", e)

# CRUD para Curso
def criar_curso():
    nome = input("Digite o nome do curso: ")
    carga_horaria = input("Digite a carga horária do curso: ")
    try:
        cursor.execute("""
        INSERT INTO Curso (nome, carga_horaria)
        VALUES (?, ?)
        """, (nome, carga_horaria))
        conn.commit()
        print(f"Curso '{nome}' criado com sucesso!")
    except Exception as e:
        print("Erro ao criar curso:", e)

def listar_cursos():
    try:
        cursor.execute("SELECT * FROM Curso")
        cursos = cursor.fetchall()
        if cursos:
            print("Cursos cadastrados:")
            for curso in cursos:
                print(curso)
        else:
            print("Nenhum curso encontrado.")
    except Exception as e:
        print("Erro ao listar cursos:", e)

def deletar_curso():
    id = input("Digite o ID do curso que deseja deletar: ")
    try:
        cursor.execute("DELETE FROM Curso WHERE id = ?", (id,))
        conn.commit()
        print(f"Curso ID {id} deletado com sucesso!")
    except Exception as e:
        print("Erro ao deletar curso:", e)

# CRUD para Matrícula
def criar_matricula():
    id_estudante = input("Digite o ID do estudante: ")
    id_curso = input("Digite o ID do curso: ")
    try:
        data_matricula = date.today().isoformat()
        cursor.execute("""
        INSERT INTO Matricula (id_estudante, id_curso, data_matricula)
        VALUES (?, ?, ?)
        """, (id_estudante, id_curso, data_matricula))
        conn.commit()
        print(f"Matrícula criada com sucesso para estudante ID {id_estudante} no curso ID {id_curso}!")
    except Exception as e:
        print("Erro ao criar matrícula:", e)

def listar_matriculas():
    try:
        cursor.execute("""
        SELECT Matricula.id, Estudante.nome, Curso.nome, Matricula.data_matricula
        FROM Matricula
        JOIN Estudante ON Matricula.id_estudante = Estudante.id
        JOIN Curso ON Matricula.id_curso = Curso.id
        """)
        matriculas = cursor.fetchall()
        if matriculas:
            print("Matrículas registradas:")
            for matricula in matriculas:
                print(matricula)
        else:
            print("Nenhuma matrícula encontrada.")
    except Exception as e:
        print("Erro ao listar matrículas:", e)

def deletar_matricula():
    id = input("Digite o ID da matrícula que deseja deletar: ")
    try:
        cursor.execute("DELETE FROM Matricula WHERE id = ?", (id,))
        conn.commit()
        print(f"Matrícula ID {id} deletada com sucesso!")
    except Exception as e:
        print("Erro ao deletar matrícula:", e)

# Menu principal
def menu():
    while True:
        print("\n--- Sistema de Gestão Acadêmica ---")
        print("1. Criar estudante")
        print("2. Listar estudantes")
        print("3. Atualizar estudante")
        print("4. Deletar estudante")
        print("5. Criar curso")
        print("6. Listar cursos")
        print("7. Deletar curso")
        print("8. Criar matrícula")
        print("9. Listar matrículas")
        print("10. Deletar matrícula")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_estudante()
        elif opcao == "2":
            listar_estudantes()
        elif opcao == "3":
            atualizar_estudante()
        elif opcao == "4":
            deletar_estudante()
        elif opcao == "5":
            criar_curso()
        elif opcao == "6":
            listar_cursos()
        elif opcao == "7":
            deletar_curso()
        elif opcao == "8":
            criar_matricula()
        elif opcao == "9":
            listar_matriculas()
        elif opcao == "10":
            deletar_matricula()
        elif opcao == "0":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar programa
if __name__ == "__main__":
    criar_tabelas()
    menu()
