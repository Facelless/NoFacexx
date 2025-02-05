# 🖥️ RemoteView - Monitoramento Remoto de Tela

O **RemoteView** é um sistema de monitoramento remoto desenvolvido em Python, que utiliza **sockets** para permitir a captura e transmissão da tela de um computador em tempo real para outro dispositivo.

## 📌 Recursos

- 🎥 **Transmissão em Tempo Real** – Visualize a tela do dispositivo monitorado sem atrasos significativos.
- 🔄 **Comunicação via Sockets** – Conexão eficiente entre cliente e servidor.
- 🖥️ **Fácil Integração** – Pode ser adaptado para diferentes usos, como suporte remoto e vigilância.
- 🛠️ **Código Personalizável** – Modifique e expanda conforme necessário.

## 🛠 Instalação & Uso

### 🔹 Requisitos

- 🐍 **Python 3.6+**
- 📦 **Bibliotecas Necessárias**: `socket`, `opencv-python`, `numpy`, `pyautogui`

### 🚀 Como Executar

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/Facelless/Remote-View.git
cd Remote-View
pip install -r requirements.txt
```

### 🖥️ Iniciando o Servidor

```bash
python main.py
```

### 💻 Iniciando o Cliente

```bash
python server.py
```

## 📖 Como Funciona

- O **servidor** captura e transmite a tela para os clientes conectados.
- O **cliente** recebe e exibe a transmissão em tempo real.
- Comunicação baseada em **sockets** para garantir eficiência e estabilidade.



## 📜 Licença

Este projeto está licenciado sob a **MIT License**.

---

🚀 Aproveite e torne o monitoramento remoto mais eficiente com **RemoteView**!

