# Organizador Inteligente de E-mails com IA — SECOMPP 📧🤖

> **Projeto desenvolvido durante a SECOMPP (Semana da Computação da UNESP — Presidente Prudente).**

---

## 📚 Contexto do Projeto

Aplicação web desenvolvida em **Python (Django)** e **JavaScript** voltada para a leitura automatizada de caixas de entrada via protocolo **IMAP** e classificação inteligente de e-mails em categorias/marcadores personalizados com o auxílio de Inteligência Artificial Generativa (**Google Gemini API — `gemini-1.5-flash`**).

---

## ✨ Funcionalidades Principais

* **Conexão IMAP (`imapclient` & `BeautifulSoup`):** Sincronização direta com servidores de e-mail (ex.: Gmail) para extração e limpeza de mensagens HTML/texto.
* **Classificação Automática com LLM (`google-generativeai`):** Análise semântica do assunto e corpo dos e-mails recebidos para atribuir automaticamente os marcadores (*Markers*) criados pelo usuário.
* **Gestão de Marcadores e Filtros (`organizadorEmail/`):** Interface web para criação de categorias, visualização de e-mails agrupados por marcador e filtragem de mensagens do dia.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Django, `imapclient`, `beautifulsoup4`, `google-generativeai` (Gemini 1.5 Flash)
* **Frontend:** HTML5, CSS3, JavaScript
* **Banco de Dados:** SQLite (Django ORM)
