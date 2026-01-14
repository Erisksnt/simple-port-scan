# 🔍 PortInspector

Um **scanner de portas TCP** desenvolvido em Python, com foco em performance, organização de código e boas práticas profissionais.\
Projeto pensado para demonstrar habilidades em **redes, segurança, threading, design modular e uso real de CLI**.

---

## 🚀 Visão Geral

Esta ferramenta permite escanear portas TCP de um host, identificando portas abertas de forma **rápida e eficiente**, com suporte a:

- 🔹 Threading (scan paralelo)
- 🔹 Timeout configurável
- 🔹 Modo verbose
- 🔹 Exportação de resultados (JSON / CSV)
- 🔹 Estrutura modular (CLI + Library)

O projeto foi desenvolvido com uma arquitetura que separa claramente **interface**, **lógica de negócio** e **utilitários**, facilitando manutenção e reutilização.

---

## 🧠 Arquitetura do Projeto

```
Erisksnt/
├── scanner/
│   ├── cli.py                # Interface de linha de comando
│   ├── banner_grabber.py     # Captura de banners (opcional)
│   ├── port_scan.py          # Scan individual de portas
│   ├── report.py             # Exportação de relatórios
│   ├── core/
│   │   └── scanner.py        # Biblioteca com threading
├── scans/                    # Resultados gerados
├── json_to_csv.py            # Conversor auxiliar
├── README.md
```

📌 **Destaque**: o threading está totalmente encapsulado na **biblioteca**, mantendo a CLI simples e limpa.

---

## ⚙️ Tecnologias e Conceitos Utilizados

- Python 3
- `argparse` (CLI profissional)
- `socket` (networking)
- `concurrent.futures.ThreadPoolExecutor`
- Threading e paralelismo
- Design modular
- Versionamento semântico de commits

---

## 🖥️ Uso da Ferramenta

### Execução básica

```bash
python -m scanner.cli 127.0.0.1 -p 1-1000
```

### Com timeout customizado

```bash
python -m scanner.cli 127.0.0.1 -p 1-1000 --timeout 1
```

### Modo verbose

```bash
python -m scanner.cli 127.0.0.1 -p 1-1000 -v
```

### Exportação de resultados

```bash
# JSON
python -m scanner.cli scanme.nmap.org -p 1-1000 --json

# CSV
python -m scanner.cli scanme.nmap.org -p 1-1000 --csv
```

📁 Os arquivos são salvos automaticamente na pasta `scans/`.

---

## ⚡ Performance

O scanner utiliza **threading** para testar múltiplas portas simultaneamente.

Exemplo:

- Range: `1-1000`
- Threads: `50`

Resultado:

- Scan sequencial: vários minutos
- Scan com threading: **segundos**

Isso demonstra entendimento prático de **concorrência aplicada a redes**.

---

## 🔐 Contexto de Segurança

Este projeto foi desenvolvido com foco educacional e defensivo, simulando ferramentas utilizadas em:

- Diagnóstico de rede
- Auditorias básicas
- Estudos de segurança
- Troubleshooting

Não deve ser utilizado para atividades não autorizadas.

---

## 👤 Autor

Desenvolvido por **Erick**\
Formado em **Segurança da Informação**, com foco em **Redes e Cybersecurity**.

---

## ✅ Conclusão

Este projeto demonstra:

- Capacidade de estruturar código profissional
- Entendimento real de redes e segurança
- Uso eficiente de threading
- Boas práticas de CLI e versionamento
