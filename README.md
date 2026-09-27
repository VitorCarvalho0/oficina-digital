# 🚗 Oficina Digital - Sistema de Checklist e Gestão

> Sistema web desenvolvido em **Python (Django)** para modernizar e otimizar o fluxo de atendimento em oficinas mecânicas, evitando prejuízos com reclamações injustas e agilizando o processo de vistoria veicular.

---

## 💡 A História do Projeto
Este projeto nasceu de uma dor real: após um cliente relatar (sem provas) um arranhão em uma roda e a oficina precisar arcar com um custo de R$ 2.000, surgiu a necessidade de digitalizar o antigo checklist de papel. 

A **Oficina Digital** resolve isso permitindo que o mecânico cadastre o veículo, registre observações, capture fotos dos ângulos essenciais e mantenha um histórico transparente e acessível.

---

## 🛠️ Tecnologias Utilizadas
* **Python** 🐍
* **Django** (MVT, Sistema de Autenticação e ORM)
* **HTML5 / CSS3**
* **SQLite** (Banco de dados para desenvolvimento)

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o projeto na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.scom/VitorCarvalho0/oficina-digital.git
   cd oficina-digital

## Crie e ative um ambiente virtual:

Bash
python -m venv venv
## No Windows (PowerShell):
.\venv\Scripts\Activate
## No Mac/Linux:
source venv/bin/activate
Instale as dependências:

Bash
pip install django
Execute as migrações do banco de dados:

Bash
python manage.py migrate
Inicie o servidor de desenvolvimento:

Bash
python manage.py runserver
Acesse no navegador: http://127.0.0.1:8000/

## 🚀 Próximas Funcionalidades
[ ] Cadastro completo de veículos e clientes associados.

[ ] Módulo de upload de fotos por ângulos (Frente, Traseira, Laterais).

[ ] Painel de status de manutenção (Recebido, Em Andamento, Finalizado).

[ ] Assinatura digital do cliente na tela.

Feito com 💻 por Vitor Gabriel como parte da jornada de especialização em Python e Django.
