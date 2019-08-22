# PLN-Project
Projeto para a disciplina de PLN-2019.Q2

## Instruções
Para a execução desse código, é necessário executar o servidor local do CoreNLP da universidade de Stanford

- Baixe o código em: https://stanfordnlp.github.io/CoreNLP/
- Descompacte os arquivos
- Na pasta raiz dos arquivos execute o seguinte comando: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
- Agora basta executar o seguinte comando na pasta raiz: python3 ./emotions.py ../res/isear.csv
