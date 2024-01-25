## Notificador de Rastreamento dos Correios

### Pré-requisitos

```bash
sudo apt install libgirepository1.0-dev
pip3 install -r requirements.txt -U
```

### Execução

#### Executando no terminal

```bash
DEBUGMODE=1 ./main.py -c NM000000000BR
```

#### Executando em um cronjob

```bash
crontab -e
```

```
*/5 * * * * DISPLAY=:0 DEBUGMODE=1 /home/user/src/notificacao-correios/main.py -c NM000000000BR -l
```
