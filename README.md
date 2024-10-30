# Dashboard de Mapeamento da Divulgação Científica

Este repositório contém o código para um dashboard interativo desenvolvido com Python e Plotly Dash, criado para visualizar os resultados do questionário de Mapeamento da Divulgação Científica da UFMG. Para mais informações sobre o questionário acesse [este link](https://www.ufmg.br/proex/noticia/participe-do-mapeamento-da-divulgacao-cientifica-na-ufmg/).

O dashboard permite filtrar os resultados por algumas variáveis selecionadas.

## Instalação e Execução

1. Clone este repositório em sua máquina local.
2. Certifique-se de ter o Docker instalado.
3. Construa a imagem Docker utilizando o Dockerfile fornecido:
   `docker build -t nome-da-imagem`
4. Execute o contêiner Docker, substituindo <PORT> pela porta que você deseja expor (por exemplo, 8050):
   `docker run -e PORT=<PORT> -p <PORT>:<PORT> nome-da-imagem`
5. Acesse o dashboard no navegador em http://localhost:<PORT>.


## Email para colaboração ou sugestões

Se você tiver alguma colaboração ou sugestão para o projeto, sinta-se à vontade para entrar em contato pelo email [mapereira@ufmg.br](mailto:mapereira@ufmg.br).

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
