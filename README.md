# MediaFire Downloader

Um script simples construido em Python para download de pastas e arquivos
recursivamente do MediaFira sem a interferência de um usuário.


## Instalação e uso

Instale as depedências usando o seguinte comando dentro da pasta do projeto:

```bash
python3 -m pip install -r requirements.txt
```

Agora você pode copiar o `mdl.py` para `~/.local/bin/mdl` e dar permissão de
execução para poder usa-lo, para isso execute os seguintes comandos:

```bash
cp mdl.py ~/.local/bin/mdl
chmod a+x ~/.local/bin/mdl
```

Agora você só precisa executar o mdl passando o ID da pasta que deseja baixar,
o ID é aquele código que fica depois de `folder/` no link da página e antes da
primeira barra(`/`) que contiver no endereço.