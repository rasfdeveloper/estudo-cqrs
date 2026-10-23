# Transcricao — CQRS (Renato Augusto)

> Auto-legendas do YouTube (pt-orig), pontuacao aproximada.
> Video: https://www.youtube.com/watch?v=8Z8JAtEEan0

---

Desde muito cedo, quando a gente aprende a programar, uma das primeiras arquiteturas que a gente aprende a desenvolver é a boa e velha arquitetura tradicional, onde a gente tem o front-end da nossa aplicação, o back-end da nossa aplicação e um único banco de dados para você inserir os dados nele e

para você também consultar os dados nesse mesmo banco. Esse tipo de arquitetura é perfeita para boa parte das aplicações comuns do dia a dia e ainda mantém a simplicidade na hora do desenvolvimento. Só que o problema começa justamente nesse pequeno detalhezinho de você utilizar apenas um

único banco de dados tanto para escrita quanto para leitura. E dependendo do contexto que você está trabalhando ou do sistema que você está desenvolvendo, esse tipo de arquitetura pode ser um baita tiro no pé e ainda esconde uma série de problemas que você precisa saber resolver. E no vídeo de hoje eu

vou te mostrar todos esses problemas e também a solução para todos eles que está por trás do padrão arquitetural conhecido como CQRS ou Command Query Responsibility Segregation, que do português quer dizer segregação de responsabilidade de comando e de consulta. Então, para a gente não perder

mais tempo, vamos direto para tela porque tem muita coisa para a gente ver e muita coisa para eu te ensinar. Bora lá. Então vamos lá, vamos direto ao ponto aqui, vamos direto ao que interessa, porque como você bem já sabe, tem muita coisa para a gente ver. A primeira coisa que a gente vai começar

fazendo aqui é o seguinte, tá? Antes da gente entrar no que de fato é o CQRS, como que você implementa isso aqui no teu sistema, na tua arquitetura e por aí vai, a primeira coisa que a gente vai começar fazendo aqui é entendendo os problemas que vão nos levar até a utilização do CQRS como solução, porque

no final das contas, mais importante do que você saber implementar um padrão arquitetural é você saber quando que você tem que implementar isso aqui. Esse é o conhecimento que vale ouro, beleza? E aí vamos lá, qual que é o nosso ponto de partida aqui antes da gente chegar no CQRS? O ponto de partida aqui vai ser a

nossa arquitetura tradicional, arquitetura super básica aqui cliente-servidor, onde a gente tem aqui o cliente da nossa aplicação lá no front-end fazendo requisições HTTP lá pro nosso servidor, pra nossa API, pro nosso microsserviço, tanto faz. E esse nosso servidor aqui, por sua vez, vai se

comunicar com o nosso banco de dados, que pra fins didáticos eu tô utilizando um PostgreSQL aqui, beleza? E aí, a relação entre esses dois componentes aqui da nossa arquitetura vai gerar o que a gente chama de operações CRUD, que é o create, o read, o update e o delete lá no banco de dados. Fim de papo, super

simples, arquiteturazinha super básica, beleza? E aí, vamos lá, o que que a gente vai fazer aqui, tá? A gente vai simular que a gente tá trabalhando num e-commerce, tá? Vamos imaginar que a gente trabalha lá numa empresa lá de e-commerce, a gente dá manutenção na arquitetura, no sistema e por aí vai. E

aí, como tabelinhas do banco de dados do nosso e-commerce, a gente vai ter aqui, ó, uma tabelinha de orders, né, que são os pedidos, a gente vai ter a tabelinha de produtos, de estoque, de clientes, de pagamento, de envio, de notas fiscais e assim sucessivamente. E é agora que a gente vai começar a entrar nos primeiros

problemas que vão surgir em toda e qualquer arquitetura que precisar utilizar o CQRS. E você precisa conhecer esses problemas pra você conseguir implementar de maneira correta esse padrão arquitetural, beleza? E o primeiro desses problemas é o que a gente chama de assimetria entre escritas

e leitura. O que que é assimetria? Assimetria é basicamente uma desproporcionalidade, tá? Elas são desproporcionais. Às vezes o sistema ou tem muita escrita e pouca leitura, ou ele tem muita leitura e pouca escrita. No geral, o que você vai ver na vida real são sistemas com muita escrita e

menos leituras. Então, existe uma desproporção, é desbalanceado, e isso vai trazer uma série de problemas. Por quê? Vamos lá. Eu vou abrir aqui o Mercado Livre pra você entender mais ou menos do que que eu tô falando, e a ideia aqui é o seguinte, tá? Vamos pegar aqui o Mercado Livre e eu vou descer

aqui embaixo aqui, vou escolher aqui qualquer categoria, vamos pegar aqui os celulares e telefones. Se eu descer mais um pouquinho aqui, eu vou pegar um celular aleatório aqui e vou abrir, e repara o seguinte, tá? A ideia que eu quero que você entenda aqui, dessa questão da desproporção, né, do

desbalanceamento, da assimetria entre escritas e leituras é o seguinte: você, enquanto usuário de um e-commerce, de um marketplace ou de qualquer site por aí que venda alguma coisa, no geral, as leituras no banco de dados vão ser muito maiores do que a escrita, por quê? Porque a cada clique que você dá em

qualquer lugar aqui, o sistema tem que ir lá no banco, trazer informações, na verdade, ele tem que ir no banco, agregar um monte de informações e trazer isso de volta pra tela. Por quê? Porque se a gente reparar bem aqui, olha os dados que tão na minha tela aqui. A gente tem aqui, ó, o nome, né, a

descrição, o título aqui do anúncio, a gente tem o preço, a gente tem aqui as questões de envio, né, até o cálculo do tempo de envio, a gente tem dados aqui, ó, de quem é o vendedor desse produto, a gente vai ter as fotos aqui também, a gente tem uma descrição aqui das características, a gente tem produtos

relacionados, que também é uma busca que é realizada, além disso, a gente vai ter aqui embaixo também as características gerais também do produto, algumas fotos, a gente vai ter a descrição do anúncio também, a gente vai ter perguntas, né, as perguntas que os usuários fazem ali pra tirar a dúvida ali sobre o produto,

a gente tem as avaliações também. Então, imagina assim, no geral, enquanto você tá trafegando, além de ter, tá gerando, né, a cada clique que você dá na tela ali, você tá gerando muitas consultas ao banco de dados desse sistema, essas consultas também são consultas extremamente pesadas que precisam

agregar muitos dados. Então, essa assimetria é que é o problema. Por quê? Porque no geral, você só vai escrever alguma coisa aqui nesse sistema quando eu de fato for comprar, ou quando eu for comprar, ou quando eu fizer alguma pergunta aqui, que eu vier aqui digitar uma pergunta aqui, aí beleza, eu vou

perguntar e vai gerar uma escrita, vai ter que armazenar essa pergunta em algum lugar, quando eu fizer uma avaliação. Então, assim, a cada clique que eu dou por aqui, eu tô gerando muitas leituras e pra eu gerar uma escrita, geralmente é só quando eu compro alguma coisa ou quando eu clico ali numa pergunta ou

faço uma avaliação. Esse é o ponto aqui. E aí, vamos voltar aqui pro nosso diagrama, que a ideia aqui é o seguinte: essa assimetria geralmente é um problema. Por quê? Porque não é só pelo fato de ser assimétrico. O problema é essa desproporção também no custo. Por quê? Porque para eu gerar uma pergunta,

eu vou acertar uma ou duas tabelas. Para eu criar ali um review do produto, também é a tabelinha de review ali que está vinculada ao produto e só. Para eu, de repente, vir aqui, ó, e gerar um cadastro lá do produto, eu sou um vendedor, quero cadastrar meu produto, beleza, eu vou dar um insert lá na

tabela de produtos, vou atualizar um estoque, de repente, vou inserir aqui o preço na tabelinha de preço e fim de papo. Agora, olha o que que acontece quando a gente tenta ler um produto. Ele tem que dar um select no produto, ele tem que fazer join com o estoque, com sellers ali que são os vendedores, os

reviews aqui também, o custo de envio, as categorias, o preço, o product ads aqui também, a questão dos pedidos, né, daquele produto, quantos foram vendidos, né, quantos produtos que também aparece aquela informação. A gente tem as perguntas, a gente tem aqui as taxas, né, os impostos e mais uma infinidade

que interminável de outras tabelas que precisam ser agrupadas e agregadas aqui dentro. Então, repara que o custo de uma leitura é muito maior do que o custo de uma escrita e, além disso, elas também são desproporcionais porque eu tenho muitas leituras porque tem gente clicando em tudo quanto é lugar o tempo

todo e quanto às escritas, elas só acontecem ali periodicamente quando você compra ou quando você efetiva alguma operação, algum comando. Daqui a pouco a gente vai chegar nisso, tá? Isso aqui são comandos, comandos de escrita. Então, esse é o primeiro detalhe. Eu estou usando esse exemplo aqui do

e-commerce, mas no geral, boa parte dos sistemas tem essa essa assimetria. Os sistemas, geralmente, eles têm muito mais leituras do que escritas. Isso, normalmente, não é o problema. O problema é quando você tem a assimetria e, ao mesmo tempo, você tem uma desproporcionalidade aqui na questão do

custo porque o custo da leitura é muito maior do que o custo da escrita. Então, o que que isso acaba provocando? Isso vai acabar provocando aqui o gargalo no nosso banco de dados. Por quê? Porque isso é custoso demais, e vai acabar impactando também nas escritas, porque essas queries aqui, elas estão

competindo por recurso, ela vai estar competindo por memória RAM lá do servidor do banco de dados, ela vai estar competindo por processamento, ela vai estar competindo também pelo pool de conexões, por IO e assim sucessivamente. Então, esse tipo de problema aqui, essa assimetria, vai gerar um gargalo pesado

no banco de dados. E aí você deve estar imaginando assim: "Pô, Renato, pera aí. Então, se as minhas queries de leitura, elas vão acabar impactando na escrita, porque vai competir com por recurso ali, por hardware e tudo mais, o que é que eu posso fazer?" Eu posso simplesmente escalar verticalmente o meu banco de

dados. Eu posso ir lá e adicionar CPU, eu posso adicionar memória RAM, posso adicionar mais armazenamento dentro dele e vai dar tudo certo. Por quê? Porque agora eu tenho mais hardware. E se eu tenho mais hardware, eu, logicamente, vou conseguir processar aqui tanto as escritas quanto as leituras de maneira

concorrente, de maneira paralela, vai ter um pool melhor de conexões ali e vai dar tudo certo. Beleza, essa daqui é uma ótima saída para início de conversa. Só que aí, qual que é o detalhe? O detalhe é que isso aqui vai até funcionar até certo ponto, mas tem um problema que talvez você não tenha reparado, que é o

seguinte: isso aqui vai permitir que a gente consiga executar as queries ali com mais facilidade, porque agora a gente tem mais espaço, a gente tem mais hardware ali disponível para a gente poder utilizar. Beleza, só que qual que é o problema? O problema é que quando a gente fala de aplicações de grande

porte, de um e-commerce ou de aplicações que precisam de performance, as queries aqui de leitura, tanto as de leitura quanto as de escrita, elas precisam ser rápidas. Então, não adianta somente eu adicionar mais poder computacional aqui, mais memória RAM, mais CPU no meu servidor de banco de dados, se a query,

por natureza, é lenta. Isso aqui é quase a mesma coisa que você pegar, por exemplo, uma rodovia, imagina que você pega uma rodovia, você ampliou várias faixas na lateral ali e agora consegue passar muito mais carros, muito mais caminhões, só que qual que é o detalhe? O detalhe é que os seus caminhões, os

seus carros, tanto faz, eles são caminhões que só conseguem andar a 80 km/h. Então, não adianta, você conseguiu paralelizar, você conseguiu abrir mais espaço para todo mundo passar, só que os caminhões não vão correr mais rápido por causa disso. Então, as queries aqui, por si só, elas são extremamente custosas e

extremamente lentas. E quando a gente fala de uma aplicação que precisa de performance, a gente precisa dar um jeito de tornar isso aqui em buscas muito mais rápidas e muito mais eficiente. E aí, qual que é a próxima saída que você, logicamente, vai pensar e que você tem que pensar e que você tem

que utilizar? É o quê? É o seguinte, vamos criar índices. Eu sei que você pensou no índice aí. Então, vamos criar índice lá no customer ID, no product ID, no created at, vamos criar índice em tudo, vamos indexar tudo. Por quê? Porque agora as minhas consultas aqui, elas vão ficar muito mais eficientes,

porque agora está tudo indexado. Show de bola, a gente consegue trabalhar com isso. Só que qual que é o problema? O problema é que, como eu sempre falo em todo o vídeo de arquitetura aqui do canal, a arquitetura de software é trade-off, não adianta. Não existe solução perfeita, não existe bala de

prata. Tudo que você escolhe, você vai pagar por outra coisa. Então, por exemplo, se a gente adicionar índices aqui, se a gente entupir as tabelinhas ali, se a gente criar índice para tudo, a gente vai melhorar um pouco a performance de leitura, só que, ao mesmo tempo, a gente vai começar a prejudicar

a escrita. Por quê? Por que que a gente vai prejudicar as escritas aqui? Porque é o seguinte, se você criou lá os índices no banco de dados e agora ele controla esses índices, ele consegue buscar de maneira muito mais eficiente, a cada nova inserção que você fizer, cada novo registro que você armazenar, o

banco agora precisa ficar reorganizando esses índices lá dentro. Então, por natureza, os índices, eles aliviam a leitura, mas eles começam a prejudicar as escritas. Então, é um trade-off. E aí eu te falo, será que faz sentido a gente tornar a escrita lenta? Será que faz sentido, na hora que o cara for comprar

um produto, na hora de ele botar um produto ali no carrinho, aquilo ficar demorando, ficar lento e tudo mais e ou até crachar a aplicação porque está demorando demais? É lógico que não faz sentido, porque nesse nosso caso aqui, tanto a leitura quanto a escrita são processos críticos. A leitura para poder

trazer a informação para o cliente e navegar de maneira rápida, logicamente, porque todo o cliente quer navegar num sistema que é fluido. E ao mesmo tempo, a escrita é extremamente crítico, por quê? Porque se tiver lentidão, o cara abandona o carrinho e vai embora. Então, o cara tem que conseguir efetuar compra,

ele tem que conseguir fazer uma pergunta, ele tem que conseguir fazer o review do produto que ele comprou. Então, nós temos operações críticas. Então, o índice e ele, por um lado, vai melhorar a consulta, mas pelo outro, ele vai prejudicar e muito a nossa escrita, beleza? E aí, vamos lá. Eu sei que nesse

exato momento, você já deve tá pensando em algumas outras soluções aí, mas eu quero te trazer mais um problema para piorar mais ainda um cenário. Por quê? E por que que eu escolhi essa questão do e-commerce? Porque, cara, dá para fazer N coisas aqui, que logicamente refletem na vida real. Como, por exemplo, a gente

pode ter o pessoal lá de negócio, o pessoal de produto e o pessoal de BI também, precisando montar um dashboard para diretoria. E os dados da nossa aplicação, da nossa arquitetura, eles estão dentro do nosso banco de dados. Então, imagina, por exemplo, que o pessoal de negócios pediu lá, né, um

dashboard que tivesse, por exemplo, as seguintes informações: o faturamento por cidade, por categoria, nos últimos 90 dias, agrupado por semana, comparado ao ano anterior, somente pedidos entregues e excluindo o chargeback. Aí eu te pergunto, cara, tu imagina, tu consegue imaginar a query monstruosa que vai ser

para montar isso aqui, cara? Você consegue imaginar o que que vai acontecer? Logicamente, isso aqui vai travar toda a aplicação. Por quê? Porque uma query dessa, ela vai consumir praticamente todo o recurso disponível do banco de dados. Então, todo mundo que tiver querendo ler alguma informação ou

inserir alguma informação, vai travar e provavelmente a aplicação vai cair. Então, cara, não faz sentido. A gente tá com alguns problemas aqui, que eu espero que você já esteja começando a entender. Daqui a pouco vai ficar mais claro essa questão do modelo de comando, do modelo de escrita para o modelo de leitura.

Daqui a pouco isso vai ficar mais claro, mas por hora, eu quero que você consiga imaginar aqui todos esses problemas acontecendo. E aí vamos lá. Eu sei que nesse exato momento, se tu é um cara um pouco mais avançado, deve estar pensando assim: "Pô, Renato, então o seguinte, já que a minha leitura e a minha escrita

estão conflitando, tá dando esse problema, a gente tem a questão também da performance, precisa ser um pouco mais rápido ali e tudo mais. Cara, de repente, talvez seja melhor a gente trabalhar com read replica". Então, como que funciona essa questão do read replica aqui? Basicamente, isso aqui é

você separar a escrita da leitura lá no banco de dados. Só que tem um ponto de atenção aqui. Isso aqui muita gente confunde isso aqui com CQRS, isso aqui não é CQRS. Isso aqui, logicamente, é a porta de entrada, mas não é o padrão arquitetural. Isso aqui, o que você tá fazendo é separando escrita de leitura

apenas a nível de acesso a dados, apenas no nível do banco de dados. Quando a gente fala de CQRS, a gente vai ter que envolver a arquitetura como um todo, beleza? Essa é a diferença. Então, esse aqui é o padrãozinho aqui read replica, é a porta de entrada, beleza? Como que isso aqui funciona, tá? Isso aqui,

basicamente, vai funcionar da seguinte forma. A gente tem o nosso servidor e aí toda escrita, né, todo o create, todo o update ou todo delete no banco de dados vai ser roteado para esse banco principal aqui, que vai ser o nosso banco master. E aí eu sei que você vai fazer piadinha nos comentários por causa

do banco master, mas tá tudo certo. E agora, as leituras, o nosso servidor vai rotear para essas réplicas aqui, que são réplicas fiéis, tá, que contém os mesmos dados do banco principal. Então, isso aqui, basicamente, serve para quê? Isso aqui vai servir para a gente separar a escrita da leitura e elas pararem de

ficar se conflitando e ao mesmo tempo, como a gente tem uma assimetria, né, de leituras ali para escritas, onde as leituras são muito maiores do que a escrita, a gente consegue criar N réplicas do nosso banco principal e disponibilizar essas réplicas aqui, né, essa escalabilidade horizontal do banco,

para quê? Para conseguir paralelizar aquela alta volumetria aqui, ó, das leituras. Então, a escrita, né, o cadastro de um produto novo, uma pergunta que você fez, um review do produto, vai ser enviado para o banco principal. Beleza. E as leituras, né? Essas leituras aqui com aquele monte de

join e tudo mais, as leituras lá para montar dashboard de faturamento, dashboard lá de informações para diretoria, a gente vai mandar para essas réplicas aqui. E, logicamente, quanto mais réplicas nós tivermos, mais poder de processamento a gente tem e a gente consegue trabalhar ali paralelizando

essas leituras, né? Isso consegue trazer uma vazão muito maior. Só que, qual que é o problema e por que que isso aqui não vai resolver todos os nossos problemas. Isso aqui, logicamente, resolve boa parte do problema porque a gente separou escrita de leitura e eles param de se conflitar. Só que, como eu falei para

você, isso aqui é a mesma coisa que você pegar a rodovia e alargar ela ao máximo, porém não adianta você alargar a rodovia se o caminhão precisa voar 200 km/h. Se o caminhão só consegue ir a 80, então por mais que você entupa a rodovia de caminhões, eles só vão andar a 80 km/h. Então, isso aí é o reflexo dessas

queries aqui. Por mais que a gente tenha N réplicas aqui, no final das contas a gente vai ter o prejuízo de que elas são lentas por natureza. Então, isso aqui é o verdadeiro problema, é o tempo de espera. E numa aplicação de grande porte, numa aplicação que lida com a experiência do usuário de maneira

extremamente importante, a gente não pode ter lentidão, a gente não pode ter sistemas travando. Então, esse aqui é o verdadeiro problema. Read replica vai resolver parte do problema, mas ainda não resolve o todo. Então, eu quero que você comece a perceber, mais uma vez, que o pro blema talvez esteja, no

nosso modelo de dados, no nosso modelo de consulta. A gente tá precisando, fazer força para consultar dado, para montar página lá no front-end. Isso aqui, literalmente, é força bruta. A gente tá fazendo uma força desnecessária, uma força colossal, agregando um monte de dados, tentando

forçar o banco de dados a nos entregar algo que talvez a gente conseguisse de uma outra maneira. Inclusive, tem um exemplo aqui também que eu separei para você, para você conseguir, para isso ficar um pouco mais claro para você, que é esse exemplo aqui, ó, do like, do uso do like. Por quê? Pensa da seguinte

forma, se a gente vier aqui no Mercado Livre aqui e pesquisar aqui em cima por alguma coisa, se você estiver usando um Postgre, você vai ter que utilizar o like. Só que se você já assistiu o vídeo aqui no canal sobre Full Text Search e por que que você não deveria utilizar o like para fazer pesquisas, né, lá no seu

banco de dados, você já tá ligeiro quanto a isso aqui, você já sabe o que que você tem que fazer e que não é o like que vai resolver. Porém, mesmo utilizando o Full Text Search para poder fazer pesquisas inteligentes aqui, para você criar esses mecanismos e o Full Text Search, logicamente, eu te mostrei

funcionando tanto no Postgre quanto no MySQL, mesmo você utilizando o Full Text Search, ele tem limitações, vai chegar um momento que você não vai conseguir personalizar algumas coisas e aí talvez fizesse mais sentido a gente, de repente, utilizar um Elastic Search, de repente, utilizar algum mecanismo muito

mais inteligente para poder trazer esses resultados mais relevantes, de acordo, logicamente, com o que o usuário tá pesquisando. Então, eu trouxe esse exemplo aqui, logicamente, mais uma vez para te mostrar que o modelo de pesquisa, o modelo de consulta tá esquisito. E é exatamente isso que nos

leva para o CQRS, que é a segregação de responsabilidade de comando e de consulta. Então, repara que de lá até aqui nós tivemos o quê? Problemas de assimetria, ou seja, leituras muito maiores do que a escrita. Esse é o primeiro cheiro, tá? Esse é o primeiro faro que você tem que ter, você olhou

ali, cara, é desproporcional? Vamos dar uma analisada no custo dessas queries para ver se tem esse esse desbalanceamento, essa desproporcionalidade. E se tiver, já é mais um sinal de que talvez você tenha que começar a pensar num CQRS. Então, a gente veio da assimetria, a gente teve o

custo ali, a questão do custo muito alto para poder buscar dados no banco, a gente teve a questão do conflito entre queries de leitura ali com queries de escrita, então isso também é um problema muito sério. A gente viu que, mesmo aumentando o hardware do nosso sistema, da nossa arquitetura, ainda

assim as nossas queries continuariam lentas, porque elas são lentas por natureza. Então, o problema talvez não seja o hardware. O problema talvez seja que a gente esteja tentando resolver com hardware um problema que é relacionado ao acesso, ao modelo dos dados na nossa arquitetura. E é aqui que entra essa

segregação da responsabilidade de comando, ou seja, das escritas no banco de dados das consultas. Então, é agora que a gente entra no CQRS. E aí, CQRS, cara, é super simples, você vai sair daqui entendido. E a ideia aqui começa do seguinte ponto, tá? A gente tem a nossa arquitetura tradicional e a gente

vai parar com essa arquitetura tradicional. A gente tem o nosso cliente aqui, o nosso front-end, a gente vai ter o nosso servidor e o nosso banco de dados. A gente não vai trabalhar dessa forma mais, ou seja, a gente vai separar a escrita da leitura, só que não a nível de banco, a nível da arquitetura como um

todo. Como que a gente vai fazer isso? A gente vai, primeiramente, dividir o nosso servidor, o nosso microserviço, a nossa API, tanto faz. Então, a nossa API, aqui o código aqui, o nosso microserviço, tanto faz, ele vai ter os comandos, ou seja, o a escrita no banco de dados, que a gente vai escrever aqui

no nosso Postgres, ou seja, o cara cadastrou um produto, o cara foi lá, criou uma opinião no produto, ele fez uma pergunta, fez qualquer outra coisa, beleza, a gente vai escrever no nosso Postgres. Show de bola, o Postgres está perfeito para a gente fazer a escrita. E as consultas, como é que a gente vai

fazer? A gente vai utilizar um outro microserviço, uma outra API, que vai cuidar de acessar o banco de dados para fazer leituras. Só que esse banco de dados aqui é aonde está o segredo, é aqui que mora o segredo. Por quê? Antes de eu entrar nesse detalhe aqui desse banco, eu quero te mostrar esse elemento

aqui que eu ainda não falei, que é o API Gateway. Esse API Gateway aqui é basicamente o seguinte, esse cara aqui vai funcionar como um roteador. Ele é o portão de entrada da nossa arquitetura. Então, toda requisição HTTP que vier com um GET, a gente vai direcionar para o nosso Read Service, ou seja, para

buscar, para leitura. O GET, método GET, é para leitura, então a gente direciona para esse servidor. E todos eles que vierem com um POST, um patch ou um delete, a gente manda para esse nosso servidor aqui e fim de papo. O AppGate é só para isso, é só para fazer esse roteamento e para isso aqui ficar um

pouco mais completo aí para você entender como é que funciona, beleza? E aí, ó, esses dois carinhas vão escrever e ler nos seus respectivos bancos de dados. E aí, ó, como eu falei, a gente tem o post aqui, a gente pode manter ele, pode botar um MySQL, tanto faz, ou qualquer outro banco que você quiser, só

que o de leitura, repara aqui, o de leitura é o seguinte, como a gente tem aquele modelo problemático de leitura, a gente tem que ficar fazendo join toda hora e, tem algum problema com o nosso modelo de leitura. Esse é o último problema que bate o martelo e fala, cara, vai para o CQRS, porque CQRS é o

que vai resolver o problema. Então, quando a gente tem esse problema, o que que a gente pode fazer? A gente pode trocar o banco de dados. Eu posso utilizar um, de repente, um modelo desnormalizado, talvez eu não precise de todos aqueles relacionamentos, talvez eu precise dos meus relacionamentos aqui,

ó, na fonte da verdade, ou seja, a fonte da verdade da minha arquitetura vai ser o meu banco de escrita. Esse banco aqui, e é assim que a gente chama mesmo de fonte da verdade, é o banco mais importante da nossa arquitetura, porque é aqui que a gente vai armazenar tudo o que a gente precisa, todos os registros,

todas as escritas. Beleza. E quanto à leitura, a gente pode utilizar o banco que a gente quiser. A gente pode utilizar um MongoDB, a gente pode utilizar um ElasticSearch, como eu mencionei, né, a gente, pode ter dados ali, montar telas e tudo mais e tal, talvez seja muito melhor fazer

buscas lá no ElasticSearch ou talvez no MongoDB com os dados desnormalizados, talvez para montar a tela, eu não precise, cara, ficar criando relacionamentos e fazendo join. Trazer dados desnormalizados é muito mais rápido. Ah, Renato, mas, dado desnormalizado, sem relacionamento, a

gente vai ter dados duplicados, a gente vai ter muita duplicata no banco. Não tem problema, como eu falei, tudo é um trade-off em arquitetura de software, você precisa entender isso, senão, você vai passar uma vida inteira buscando a solução milimetricamente perfeita e não existe essa solução. Então, trazer dados

desnormalizados, você vai vai que pagar com dados duplicados e tá tudo bem. O mais importante é que eu resolva o requisito. Qual que é o requisito? Queries rápidas, buscas rápidas, montar a tela de maneira rápida. Então, é assim que funciona. Então, aqui, cara, no banco de leitura, a gente poderia usar

um Cassandra da vida, de repente um ScyllaDB, um Cockroach aqui, ou o próprio Redis também. Não importa. Como eu falei, o nosso banco, a nossa fonte da verdade é o banco de escrita. Então, esse banco eu escrevo, tá? E aí eu sei que você já deve estar na dúvida. Tá, mas se eu vou cadastrar um produto aqui,

como que eu vou ler esse produto aqui por esse cara? Como que esse produto vai chegar aqui? Esse produto vai chegar aqui através de uma coisa que a gente chama de CDC, que é Change Data Capture, ou seja, é um mecanismo que vai ficar buscando atualizações aqui de dados novos que chegaram, e ele vai jogar

essas atualizações aqui pro banco de leitura no formato em que ele aceita. Então, ele vai pegar os dados do Postgre aqui no formato do Postgre, e cadastrar eles aqui no banco de leitura no formato que a gente escolher aqui, de repente um Elasticsearch, um MongoDB, um Redis, tanto faz. E aí, esse mecanismo, ele

funciona como, tá? Eu já ensinei isso aqui no vídeo do Ticketmaster, vou deixar um card aqui em cima o link na descrição, dá um confere aí depois. Então, isso aqui funciona basicamente da seguinte forma, a gente tem aqui uma fermentinha chamada de Debezium, que ele fica lendo os arquivinhos de log do

Postgre, então ele vai ficar lá lendo o tempo todo. Toda vez que for inserido um novo registro, o que que a gente pode fazer? A gente pode configurar o Debezium para postar uma mensagem no Kafka, que é uma fila de mensageria, e aí a gente pode configurar um worker aqui para poder consumir essa fila, e

esse worker aqui vai ter o código lá específico para poder pegar esses dados e inserir esses dados aqui nesse nosso banco de leitura no formato em que ele aceitar, seja no formato do Cassandra, no formato do Elasticsearch, e assim sucessivamente. E é assim que a gente faz essa sincronia. E aí, por que que eu

te falei que o banco de escrita é o banco, é a nossa fonte da verdade? Porque, cara, eu posso deletar o meu banco de leitura, eu posso apagar ele, eu posso trocar o meu banco de leitura, não importa, eu posso fazer o que eu quiser, porque o mais importante é o meu banco de escrita, porque é aqui que está

o ouro, é aqui que estão todas as informações pertinentes ao respeito do nosso sistema. Então, é aqui que tá o segredo da coisa, beleza? E aí, ó, a gente faz esse mecanismo aqui, a gente faz essas atualizações e é assim que funciona o CQRS, porque repara, nós separamos a escrita da consulta e a

consulta a gente pode utilizar o modelo que a gente quiser, não importa, a gente pode escolher trabalhar com um mecanismo que a gente quiser, seja ele mais rápido, seja ele desnormalizado, tanto faz, é assim que funciona. E aí tem mais um detalhe, eu sei que aqui, ó, esse mecanismo aqui que eu tô utilizando, que

é o CDC, existem outras formas, como por exemplo, a gente poderia, ao invés de pegar aqui o Debezium, usar o Kafka, botar um worker aqui, tá, um job ali pra ficar consumindo ali da fila, a gente poderia simplesmente vir aqui, ó, e fazer o seguinte, eu poderia escrever no meu banco de escrita e depois publicar

num Kafka e aí a gente pega o workerzinho aqui, que vai consumir as mensagens do Kafka e escrever no nosso banco de leitura e fim de papo. Isso aqui, logicamente, se você assistiu o vídeo de Dual Write, você sabe que aqui tem um problema gravíssimo de dupla escrita, né? Você sabe que isso aqui vai

dar problema e que você resolve com o padrão conhecido como Transactional Outbox Pattern. Aí você resolve esse problema de dupla escrita aqui e dá pra utilizar essa arquitetura aqui, você escreve no banco de escrita, publica uma mensagem no Kafka com esses dados, o worker vai ler esses dados e vai inserir

no banco de leitura, fim de papo. Isso aqui, mais uma vez, te ensinei naquele vídeo lá de Dual Write, eu vou deixar um card aqui em cima e o link na descrição, então dá um confere aí depois e eu também vou deixar o link na descrição do mapa do arquiteto, um guia de carreira completasso pra eu te conduzir do zero,

passando pelo júnior, pelo pleno e pelo sênior, até você se tornar um arquiteto de software e um arquiteto de soluções com conhecimentos práticos pra vida real. E lá dentro eu te entrego não só esses padrões aqui, como CQRS, Event Sourcing, padrões de microserviços, mas todos os padrões e todos os conceitos

que você precisa pra você sair de onde você tiver na sua carreira e se tornar um arquiteto de software, seja você um iniciante, seja você um programador júnior, um programador pleno, um programador sênior, já calejado de batalha, não importa, o mapa do arquiteto é para você. E lá dentro você

vai ter acesso à minha pessoa, vai poder me consultar, vai poder tirar suas dúvidas, eu vou te ajudando, vou te orientando, vou te guiar ao longo do percurso e ainda te entrego um roadmap completo que vai conduzir, guiar a tua carreira. Então, eu vou deixar o link na descrição, dá um confere aí depois e

vamos voltando aqui para o nosso diagrama porque ainda tem alguns pontos aqui a se considerar a respeito do CQRS, beleza? Isso daqui é a implementação mais genuína do CQRS, beleza? Esse é o ponto que você precisa entender. Agora, tem alguns poréns aqui que você precisa considerar na hora de implementar isso

aqui e o primeiro que você precisa considerar é que a gente vai lidar com algo chamado consistência eventual, ou seja, os nossos dados, por algum tempo, por algum período curto de tempo, eles vão estar inconsistentes. Isso não é um problema dependendo do tipo de sistema que você tá projetando. Então, por

exemplo, vamos imaginar aqui o seguinte, tá? A gente acabou de cadastrar aqui um produto no nosso write service. Então, o usuário foi lá, o usuário não, né, o vendedor foi lá, cadastrou lá o iPhone novo que ele tá querendo vender. Beleza, então, requisição veio aqui do nosso front-end, chegou aqui no nosso API

Gateway, passou lá para o nosso write service e aí o nosso servidor aqui escreveu lá no nosso postgre, beleza? Ele cadastrou lá o nosso iPhone novo lá que o vendedor tá vendendo. Show de bola, mistério nenhum. Só que aí ele inseriu esse cara aqui dentro e agora ele precisa aparecer no banco de

leitura. Então, para para pensar o seguinte, no momento em que o vendedor cadastrou esse cara e esse iPhone chegou aqui nesse banco, ele ainda não existe no banco de leitura. Então, se algum usuário atualizar a página, esse iPhone ainda não vai estar disponível e, olhando para esse contexto, tá tudo bem,

não tem problema nenhum ter um atraso. Por quê? Porque vai levar alguns milissegundos aqui ou até mesmo alguns segundos para que esse cara publique a mensagem no Kafka, para que esse worker leia a mensagem do Kafka e escreva nesse banco aqui. Essa, esse delay, esse atraso entre uma replicação do dado de

um lugar para o outro é o que a gente chama de consistência eventual. Esse é o primeiro ponto e tá tudo bem dependendo do tipo de sistema ou da parte do sistema que você tá projetando. Inclusive, esse é o segundo ponto de atenção. Isso aqui não precisa ser o teu sistema inteiro. Você pode trabalhar com

CQRS, dependendo ali do sistema, você pode isolar uma partezinha do sistema, de repente uma parte ali, justamente de cadastro ou de alguma coisa do tipo ali, que você queira isolar. Você trabalha com CQRS e a outra parte do sistema tá trabalhando ali, de repente com monolito modular, uma arquitetura de

microserviços sem CQRS e tá tudo bem. Isso aqui, como eu falei, é para resolver problemas de assimetria de leitura e escrita, problema de custos muito maiores entre um lado e o outro, a performance das queries, o modelo, na verdade, de consulta ali dos dados. Então, tudo isso você tem que analisar e

você tem que saber o momento exato para aplicar isso aqui. Isso aqui também você não precisa implementar na arquitetura toda. Isso aqui é para resolver problemas pontuais, beleza? Esse é o ponto que eu quero que você entenda e agora eu tenho certeza que você tá muito mais preparado para lidar com isso aqui

na vida real e também para encarar isso aqui nas entrevistas porque aparece e muito, beleza? Então, esse é o vídeo de hoje, espero que tenha te ajudado. Se te ajudou, deixa teu like aí, se inscreve no canal e ativa o sininho da vaquinha para tu não perder nenhuma notificação. Se ficou qualquer dúvida, deixa nos

comentários abaixo que eu prometo que eu tiro um tempo para te responder. Por fim, eu vou ficando por aqui. Um forte abraço para você e nos vemos em breve.