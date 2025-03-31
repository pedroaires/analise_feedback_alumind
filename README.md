# analise_feedback_alumind
Sistema web para análise de feedbacks de usuários com uso de LLMs (Large Language Models), geração de métricas e envio automático de relatórios semanais.

---

## ✅ Recursos Principais
- Envio e análise automatizada de feedbacks.
- Extração de sentimentos e funcionalidades solicitadas via LLM.
- Detecção de SPAM via LLM.
- Geração de métricas agregadas dos feedbacks.
- Visualização de relatórios via web.
- Envio semanal de resumo de feedbacks por email para stakeholders.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**
- **SQLAlchemy**
- **LangChain + OpenAI**
- **APScheduler**
- **PostgreSQL**
- **Poetry** (gerenciador de dependências)

---

## Instalação
Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/alumind-feedback-analyzer.git
cd alumind-feedback-analyzer
poetry install
```

---

## Configuração
Crie um arquivo `.env` com suas chaves e configurações:

```env
OPENAI_API_KEY=sk-xxxxx
DATABASE_URL=postgresql+psycopg2://[usuario]:[senha]@localhost:5432/feedback_db

```

---

## ▶️ Execução da Aplicação

```bash
poetry run python run.py
```

A aplicação estará disponível em: `http://localhost:5000`

> O banco será populado automaticamente com exemplos contidos em `data/feedbacks.json`.

Para testar o envio de e-mails localmente, lembre-se de iniciar um servidor SMTP falso com:

```bash
python -m aiosmtpd -n -l localhost:1025
```
Isso permitirá visualizar os e-mails enviados diretamente no terminal, sem precisar de um provedor real de e-mail. No entanto, os e-mails estarão codificados.

---

## 🔌 APIs Disponíveis

### `POST /feedbacks`
Envia um novo feedback.

**Request:**
```json
{
  "id": "uuid-opcional",
  "feedback": "Gostaria de poder editar meu perfil."
}
```

**Response:**
```json
{
  "id": "...",
  "text": "...",
  "sentiment": "POSITIVO",
  "requested_features": [
    {
      "code": "EDITAR_PERFIL",
      "reason": "O usuário gostaria de editar seu perfil"
    }
  ]
}
```

### `GET /feedbacks`
Retorna todos os feedbacks processados.

### `GET /feedbacks/<id>`
Retorna um feedback específico por ID.

### `GET /feedbacks/metrics`
Retorna métricas agregadas dos feedbacks, incluindo:

- Total de feedbacks no período
- Quantidade de feedbacks por sentimento (positivo, neutro, negativo)
- Funcionalidades mais solicitadas no período

#### Parâmetros de consulta:

| Parâmetro    | Tipo     | Obrigatório | Descrição                                  |
|--------------|----------|-------------|--------------------------------------------|
| `start_date` | `string` | Não         | Data inicial no formato `YYYY-MM-DD`       |
| `end_date`   | `string` | Não         | Data final no formato `YYYY-MM-DD`         |

#### Exemplo:
```bash
GET /feedbacks/metrics?start_date=2025-03-01&end_date=2025-03-31
```
Se nenhum parâmetro for informado, o sistema retorna as métricas considerando todos os feedbacks disponíveis.


### `POST /feedbacks/send-email-report`

Dispara manualmente o envio do relatório semanal de feedbacks por e-mail.

> Este endpoint é destinado apenas para fins de teste.

#### Corpo da requisição:
Nenhum conteúdo necessário no corpo da requisição.

#### Resposta:
Retorna o conteúdo do e-mail gerado.

**Status 200 – Sucesso:**
```json
{
  "conteudo_email": "Resumo semanal gerado pela LLM..."
}
```

---

## ⏱️ Agendamento de Emails Semanais

O sistema envia automaticamente um resumo semanal dos feedbacks toda **sexta-feira às 17h**.
- % de feedbacks positivos e negativos
- Principais funcionalidades solicitadas
- Resumo gerado por LLM com linguagem natural
Você também pode executar via requisição, mais informações na seção **Execução da Aplicação**.
> Também é enviado assim que o programa inicia, para facilitar testes

## 🔒 Detecção de SPAM com LLM

Antes de processar qualquer feedback, o sistema consulta a LLM. Se a LLM retornar `"SIM"`, o feedback é rejeitado com erro 400.

---

## 🔮 Popular Banco com Exemplos

O banco é automaticamente preenchido com dados em `data/feedbacks.json` ao iniciar a aplicação com:

```bash
poetry run python run.py
```
