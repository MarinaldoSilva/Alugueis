# API de Reservas de Imóveis 🏡

## Projeto
Projeto desenvolvido do forma autônoma, usando como base a documentação do Django Rest Framework e muita pesquisa.
O projeto em si consiste em uma API de Reservas/Alugueis de imóveis, para desenvolvimento usei os princípios S.O.L.I.D. mas tomei cuidado para não ser verboso, a simplicidade funcional foi o objetivo.
Com esse sistema é possível que um usuário se cadastre com a única rota liberada para acesso são sem precisar de validação de ``usuário/senha e Token``, após isso o user tem duas opções:

* Cadastrar uma casa para aluguel.
* Alugar um casa já cadastrada.

Para que isso seja possível as foram criadas funções e validações para evitar conflitos.

### Processo de criação
Esse foi o projeto com uma lógica simples, porém complexa que tem como o core central a sobreposição de datas, usando o ``Q`` do próprio django, foi possível estabelecer um parâmetro de cruzamento de datas, assim 
evitando que a data de entrada fosse inferior a data de saída de um usuário, evitando conflito de datas, o usuário é injetado pela view, quando um usuário autenticado faz a requisição, todo o processo de:
* calcular preço das diárias
* validação de dadas
* calular datas para as entradas e saidas
* verificar se é um self.instance para atualizações.

é feito quando o ``serializer.is_valid()`` é chamado, e após isso o meu ``data`` que é meu candidado a ``serializer.validated_data`` é validado e virá o meu ``validated``, com isso no ``serializer.save()``
os dados são persistidos no banco.
Caso aconteça algo nesse processo, uma mensagem do erro com o status vai ser fornecido para o cliente, assim facilitando a identificação do erro.

O projeto vai passar por melhorias futuras, tais como:
* Atualização para JWT
* Upload de imagens das casas
* Filtros e buscas

Com essas futuras implementações vamos ter um sistema bem mais robusto.

## Funções

### Alugueis
* Criação de usuários com ``Token`` de único vinculado ao ``username``
* Listagem de casas de um usuário (Dono das casas)
* Detalhes de um casas especificas
* Atualizar detalhes de uma casa (descrição, título, preço da diária e etc...)
* Injeção de user de forma automática (serializer)

### Casas
 * Criar novos alugueis para uma casa especifica
 * Validação de datas para evitar sobreposição(Q - formulas complexas)
 * Calcula automaticamente o valor do aluguel com base na quantidade dias que o usuário vai ficar
 * Casas que o usuário tem com alugueis ativos e inativos
 * Detalhes de um aluguel
 * Exclusão de alugueis

### Teste

Para testar é necessário ter o Python, minha versão é 3.12, clone o repositório do projeto.
```bash
https://github.com/MarinaldoSilva/Alugueis
```

Verifique os arquivos `urls.py` de `config`, `reservas` e `users` para os endpoints completos, lembrando do caminho base `api/v1/`.
* Crie seu usuário e anote o seu Token
* cadastre uma casa
* tente fazer o aluguel da casa

crie seu ambinete virtual:
```bash
  python -m venv venv
  .\venv\Scipts\activate
```

instale o arquivido de libs:

```bash
    pip install -r requirements.txt
```

Faça as migrações para o banco

```bash
    python manage.py makemigrations users
    python manage.py makemigrations reservas
    python manage.py migrate
```

Teste o serviço rodando o servidor próprio do Django.

 ```bash
    python manage.py runserver
 ```

Toda e qualquer sugestão é bem-vinda, meu email é ``marinaldo12@hotmail.com``, me escreve sua sugestão de melhoria e ideias, podemos construir isso juntos.
