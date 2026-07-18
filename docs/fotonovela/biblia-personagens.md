# Fotonovela — "O Escritório dos Agentes" — Bíblia de Personagens e Roteiros

Recurso narrativo recorrente do curso "Engenharia de Software na Era dos
Agentes". Mesmo mecanismo já usado nos cursos IA e Git (ver
`[[garagem-fotonovela]]`): fotonovela = "vídeo interativo" no lugar do
player, 16:9, carrossel de quadros com balão HTML por cima da imagem
(nunca texto embutido na foto). Abre E fecha cada módulo, 8-12 quadros.

## 1. Título geral

**"O Escritório dos Agentes"**

## 2. Conceito narrativo

Quatro profissionais de uma empresa de tecnologia fictícia enfrentam, a cada
módulo, um desafio relacionado a agentes de IA — antes de aprenderem o
conteúdo (abertura, tudo dá errado de um jeito familiar) e depois de
aplicá-lo (fecho, a mesma situação é conduzida com método). Humor de
escritório + exagero de novela brasileira, sempre terminando em reflexão,
nunca em humilhação. Competência não é saber tudo — é saber investigar,
formular problemas, usar ferramentas com responsabilidade, pedir ajuda,
aprender e assumir responsabilidade pelas decisões.

### ⚠️ Regra estrutural (decidida com o Diego em 2026-07-18): arco CUMULATIVO, não reset

A cada módulo, o time enfrenta um problema **novo** que eles ainda **não
sabem resolver** — específico do conteúdo daquele módulo, que ainda não foi
ensinado. Isso NÃO muda: toda abertura de módulo tem um desafio genuinamente
desconhecido pra eles, senão a história perde a tensão dramática. O que
muda — e precisa ficar visível — é que **o aprendizado dos módulos
anteriores já grudou**: eles não repetem os erros básicos que já cometeram
antes, mesmo diante de um problema novo que ainda não sabem resolver.

Ou seja: a curva de "quantidade de gafe" cai a cada módulo, mesmo que a
curva de "desafio novo, ainda sem solução" permaneça alta em toda abertura.
Nunca resetar os personagens pra estaca zero — cada abertura já parte do
patamar de maturidade que o fecho do módulo anterior deixou.

**Exemplo concreto já aplicado** (abertura M1 → fecho M1 → abertura M2 →
fecho M2): na abertura do Módulo 1, ninguém questiona o pedido vago, Carol
já sai escrevendo "crie um chatbot inteligente" sem pensar, Rafa nem
tenta perguntar. No fecho do Módulo 1 (ainda não produzido — só a abertura e
o fecho do M2 existem hoje) essas falhas específicas de M1 (Human in the
Loop, orquestração, fundamentos) deveriam já aparecer corrigidas. Na
ABERTURA do Módulo 2, o problema é NOVO (mensagens livres em linguagem
natural — algo que M1 não ensinou), mas olhando o que produzimos pro FECHO
do M2, dava pra ver que Rafa já pergunta primeiro, Fernando já pensa em
fallback, Carol já se autocorrige antes de pedir "faça tudo" — prova de
que o aprendizado de M1 (e do próprio M2) gruda e comparece.

**Decisão 2026-07-18: o Módulo 8 NÃO pula a fotonovela.** Mesmo sendo o
estudo de caso anonimizado (sem branch de laboratório), a fotonovela é
narrativa/motivacional e independe de o módulo ter evolução real de código —
todos os módulos de 2 a 12 ganham fotonovela, sem exceção.

**Padrão de volume: TODO módulo (2 a 12) ganha ABERTURA e FECHO**, os dois
uma lesson Slides de 8 quadros cada — mesmo padrão do Módulo 1. A abertura
entra logo no início do módulo (depois da 1ª lesson conceitual), o fecho
entra como penúltima lesson (antes da prova/lesson final). Gap conhecido
corrigido em 2026-07-18: o Módulo 2 tinha só o FECHO publicado — faltava a
ABERTURA (o desafio "mensagens livres em linguagem natural" nunca foi
mostrado dando errado ANTES do conteúdo do módulo, só resolvido depois).

**Como aplicar em cada módulo futuro (3 a 12)**:
1. Definir o desafio NOVO do módulo (algo que só o conteúdo daquele módulo resolve).
2. Escrever a ABERTURA mostrando esse desafio novo confundindo o time — MAS
   sem reintroduzir erros que módulos anteriores já corrigiram (ex.: a
   partir do Módulo 2, Rafa não volta a ficar em silêncio total; a partir do
   Módulo 6, ninguém widget mais um pedido sem objetivo/restrição/critério).
3. Escrever o FECHO mostrando o desafio resolvido com o método do módulo,
   E deixando pistas de que os aprendizados anteriores continuam presentes
   (pequenos gestos, falas, hábitos que já viraram natural pro personagem).
4. Cada personagem tem seu PRÓPRIO arco de maturidade (seção "arco emocional"
   de cada fotonovela) que só cresce — nunca regride sem motivo dramático
   explícito.

## 3. Bíblia dos 4 personagens

### Personagem 1 — Fernando Costa Villela ("Fê")

- **Idade**: ~52 anos
- **Função**: Engenheiro de Software Sênior
- **Experiência**: 25 anos — sistemas legados, produção, incidentes, arquitetura
- **Personalidade**: técnico, cético, direto, orgulhoso do próprio ofício
- **Insegurança principal**: medo de que agentes tornem sua experiência irrelevante
- **Qualidade principal**: profundidade técnica real, faro pra risco e ponto cego que ninguém mais vê
- **Defeito/ponto cego**: critica a IA antes de testar; usa cautela excessiva pra esconder insegurança
- **Forma de falar**: frases curtas, sarcasmo seco, referências a "no meu tempo"
- **Bordão**: "Isso aí já quebrou produção uma vez. Confia em mim."
- **Relação com os outros**: implica com a Duda... digo, com a Carol (personagem 2), mas a respeita; é quem o Rafa (personagem 4) mais teme decepcionar
- **Arco**: percebe que sua experiência vira ainda mais valiosa quando ele orienta e revisa agentes em vez de competir com eles
- **Aparência física**: homem branco, 1,75m, compleição robusta, óculos de leitura pendurados no pescoço
- **Cabelo**: grisalho, curto, levemente ralo no topo
- **Roupas**: camisa polo azul-marinho SEMPRE (cor fixa), calça social cinza, crachá antigo e surrado
- **Acessórios**: caneca de café surrada com a frase "Funciona na minha máquina" (elemento recorrente #1)
- **Postura corporal**: braços cruzados, apoiado na mesa
- **Expressões frequentes**: sobrancelha erguida, olhar de dúvida
- **Paleta visual**: tons frios — azul-marinho, cinza, branco
- **Nunca muda**: polo azul-marinho + óculos no pescoço + caneca "Funciona na minha máquina"

### Personagem 2 — Carolina "Carol" Mendes Prado

- **Idade**: ~27 anos
- **Função**: Desenvolvedora Pleno
- **Experiência**: 4 anos, entusiasta de ferramentas novas
- **Personalidade**: energética, curiosa, iniciativa acima da média
- **Insegurança principal**: confunde velocidade com qualidade; confia demais na primeira resposta do agente
- **Qualidade principal**: aprende rápido, não tem medo de experimentar
- **Defeito/ponto cego**: aceita a primeira resposta do agente sem revisar
- **Forma de falar**: rápida, cheia de gírias de tech, fala "bora" toda hora
- **Bordão**: "Já tá pronto! ...pronto pronto? Ou pronto-pronto-mesmo?"
- **Relação com os outros**: provoca o Fernando com carinho; é próxima do Rafa (o ajuda sem fazer ele se sentir mal)
- **Arco**: aprende a dar contexto, limites, pedir plano, testes e revisão humana antes de comemorar
- **Aparência física**: mulher parda, 1,65m, cabelo cacheado castanho-escuro na altura dos ombros, brincos grandes de argola
- **Cabelo**: cacheado, castanho-escuro, sempre na altura dos ombros — nunca liso, nunca outra cor
- **Roupas**: moletom verde-oliva SEMPRE (cor fixa) com estampa geométrica discreta, tênis colorido
- **Acessórios**: adesivo de laptop com um raio estilizado (elemento recorrente #2 — o notebook dela)
- **Postura corporal**: sempre inclinada pra frente, digitando ou apontando pra tela
- **Expressões frequentes**: sorriso largo, olhos arregalados de empolgação
- **Paleta visual**: tons quentes — verde-oliva, laranja, mostarda
- **Nunca muda**: moletom verde-oliva + cabelo cacheado castanho-escuro + adesivo de raio no laptop

### Personagem 3 — Marcelo "Marcelo" Andrade Tanaka

- **Idade**: ~38 anos
- **Função**: Líder Técnico (Tech Lead)
- **Experiência**: 14 anos, equilibra prazo, qualidade, segurança e expectativa de negócio
- **Personalidade**: conciliador, organizado, carrega peso além da conta
- **Insegurança principal**: acredita que deveria ter todas as respostas
- **Qualidade principal**: visão de conjunto, sabe priorizar
- **Defeito/ponto cego**: busca atalhos sob pressão; centraliza decisão demais
- **Forma de falar**: tom calmo que esconde estresse; usa listas mentais em voz alta ("primeiro... segundo...")
- **Bordão**: "Deixa comigo que eu resolvo." (dito segurando uma xícara tremendo)
- **Relação com os outros**: mediador entre Fernando e Carol; cobra prazo mas protege o Rafa de pressão excessiva
- **Arco**: aprende a orquestrar pessoas, agentes, ferramentas e processos sem concentrar toda decisão nele
- **Aparência física**: homem asiático-brasileiro, 1,70m, magro, sempre com leve olheira
- **Cabelo**: preto, curto, bem penteado (o único sinal de "controle" que ele mantém)
- **Roupas**: camisa social azul-clara de manga arregaçada SEMPRE, sem gravata
- **Acessórios**: um Post-it colado na testa em momentos de crise (elemento recorrente #3 — piada visual recorrente)
- **Postura corporal**: mãos na cintura ou gesticulando contando nos dedos
- **Expressões frequentes**: sorriso tenso, olhar pro relógio
- **Paleta visual**: tons neutros com um azul-claro de destaque
- **Nunca muda**: camisa azul-clara manga arregaçada + cabelo preto bem penteado

### Personagem 4 — Rafael "Rafa" Souza Lima

- **Idade**: ~23 anos
- **Função**: Desenvolvedor Júnior (em transição de carreira — ex-suporte técnico)
- **Experiência**: 8 meses de empresa
- **Personalidade**: observador, inteligente, quieto
- **Insegurança principal**: medo de perguntar e revelar que não entende algo; acha que todo mundo ao redor sabe mais
- **Qualidade principal**: faz perguntas certeiras quando finalmente pergunta
- **Defeito/ponto cego**: interpreta a confiança alheia como competência absoluta
- **Forma de falar**: hesitante, começa frases e recua ("Ah, deixa quieto", "Acho que... não, esquece")
- **Bordão**: "Só eu que não sabia disso?" (sempre dito baixinho, quase pra si mesmo)
- **Relação com os outros**: teme decepcionar o Fernando; a Carol é quem o incentiva a falar
- **Arco**: percebe que os mais experientes também têm dúvidas, e que formular boas perguntas é capacidade de engenharia
- **Aparência física**: homem negro, 1,80m, magro, postura levemente encurvada
- **Cabelo**: black power curto, bem aparado
- **Roupas**: camiseta cinza-mescla lisa SEMPRE, mochila surrada nunca tirada das costas
- **Acessórios**: um caderninho de notas físico que ele nunca mostra a ninguém (elemento recorrente — mas sozinho não conta como um dos 3 oficiais)
- **Postura corporal**: ombros pra dentro, olha de lado antes de falar
- **Expressões frequentes**: sobrancelhas franzidas de dúvida, olhar baixo
- **Paleta visual**: tons dessaturados — cinza, bege
- **Nunca muda**: camiseta cinza-mescla + mochila nas costas + black power curto

## 4. Mapa das relações

```
Fernando (sênior cético) ──implica com──> Carol (entusiasta)
Fernando ──intimida sem querer──> Rafa (júnior)
Carol ──incentiva──> Rafa
Marcelo (líder) ──media──> Fernando x Carol
Marcelo ──protege da pressão──> Rafa
Rafa ──teme decepcionar──> Fernando
Todos ──se reportam informalmente a──> Marcelo
```

## 5. Regras de continuidade visual (OBRIGATÓRIO em todo prompt de quadro)

Persona canônica a colar em TODO prompt que contiver o personagem:

- **Fernando**: `Fernando (SEMPRE O MESMO HOMEM: branco, 52 anos, robusto, óculos de leitura pendurados no pescoço por um cordão, cabelo grisalho curto e ralo no topo, polo azul-marinho, calça social cinza, segurando ou perto de uma caneca branca surrada com os dizeres "Funciona na minha máquina")`
- **Carol**: `Carol (SEMPRE A MESMA MULHER: parda, 27 anos, cabelo CACHEADO castanho-escuro na altura dos ombros — nunca liso, nunca outra cor —, brincos de argola grandes, moletom verde-oliva com estampa geométrica discreta, notebook com adesivo de raio estilizado)`
- **Marcelo**: `Marcelo (SEMPRE O MESMO HOMEM: asiático-brasileiro, 38 anos, magro, olheiras leves, cabelo preto curto bem penteado, camisa social azul-clara de manga arregaçada, sem gravata)`
- **Rafa**: `Rafa (SEMPRE O MESMO HOMEM: negro, 23 anos, magro, alto, cabelo black power curto e aparado, camiseta cinza-mescla lisa, mochila surrada sempre nas costas, postura de ombros levemente encurvados)`

Guard de anatomia (colar em todo prompt com pessoa):
`ANATOMIA HUMANA CORRETA: exatamente dois braços, duas mãos e cinco dedos por mão, sem membros/mãos/dedos extras/duplicados/deformados. TELAS sempre viradas pra pessoa (nunca a traseira/tampa pra frente).`

Regra de balão (aplicada depois, no editor — não no prompt de imagem):
balão SEMPRE no canto oposto ao rosto do personagem que fala; cauda aponta de
volta pra quem fala. Nenhum balão pode ser desenhado dentro da imagem pelo
Gemini — se sair desenhado, regenerar o quadro.

Regra de ambiente: empresa e sistemas 100% fictícios — nenhuma marca, cliente,
produto, código, nome interno ou dado real. Nada de estética infantil, nada
de super-herói, nada de caricatura deformada. Fotorrealista/HQ contemporânea
com atores reais.

## 6. Elementos recorrentes (mínimo 3, aparecem todo módulo)

1. **A caneca do Fernando** — "Funciona na minha máquina" (o texto na caneca é
   fixo; muda de contexto/piada em torno dela, nunca o objeto).
2. **O adesivo de raio no notebook da Carol.**
3. **O Post-it na testa do Marcelo** — aparece só em momentos de pico de
   estresse/crise, como piada visual recorrente.
4. (bônus, não conta como 1 dos 3 oficiais) **A planta murcha do escritório**,
   que piora visivelmente a cada incidente — termômetro cômico de quão mal a
   semana está indo.

## 7. Roteiro completo — Abertura do Módulo 1

**Tema**: "O Engenheiro na Era dos Agentes"
**Situação**: pedido vago de "colocar IA no atendimento ao cliente"; a
proposta do agente é exagerada; a equipe se impressiona com o volume antes de
perceber que ninguém definiu nada. Termina ANTES da solução, em pergunta
reflexiva.

### Quadro 1
- **Cenário**: sala de reunião, TV com um e-mail aberto projetado (sem texto
  legível, só um bloco de texto borrado simulando parágrafo).
- **Personagens**: Marcelo, Fernando, Carol, Rafa — todos sentados à mesa.
- **Enquadramento**: plano geral, Marcelo de pé apontando pra TV.
- **Ação**: Marcelo acabou de ler o pedido do "cliente" em voz alta.
- **Expressões**: Marcelo tenso sorrindo; Fernando já de braços cruzados;
  Carol com os olhos brilhando; Rafa olhando pros outros pra entender a reação certa.
- **Narração**: "Segunda-feira. Um pedido de duas linhas vira o problema da semana."
- **Diálogo (Marcelo)**: "'Colocar inteligência artificial no atendimento.' Só isso. Prazo: ontem."
- **Intenção de humor**: o contraste do pedido vago com o prazo impossível.
- **Ideia pedagógica**: pedidos vagos não têm objetivo nem critério de aceite.
- **Prompt visual completo**: `Sala de reunião de escritório de tecnologia fictício, luz de escritório comum, uma TV na parede mostrando um e-mail com texto borrado ilegível. Fernando (SEMPRE O MESMO HOMEM: branco, 52 anos, robusto, óculos de leitura pendurados no pescoço por um cordão, cabelo grisalho curto e ralo no topo, polo azul-marinho, calça social cinza) sentado de braços cruzados com expressão cética. Carol (SEMPRE A MESMA MULHER: parda, 27 anos, cabelo CACHEADO castanho-escuro na altura dos ombros, brincos de argola grandes, moletom verde-oliva com estampa geométrica discreta) sentada com olhos brilhando de empolgação. Rafa (SEMPRE O MESMO HOMEM: negro, 23 anos, magro, alto, cabelo black power curto, camiseta cinza-mescla, mochila nas costas mesmo sentado) olhando de lado pros colegas, incerto. Marcelo (SEMPRE O MESMO HOMEM: asiático-brasileiro, 38 anos, magro, olheiras leves, cabelo preto curto bem penteado, camisa social azul-clara manga arregaçada) de pé apontando pra TV com sorriso tenso. Still fotográfico realista estilo fotonovela/HQ contemporânea, enquadramento cinematográfico horizontal 16:9, sem texto legível na imagem além do bloco borrado na TV. ANATOMIA HUMANA CORRETA: exatamente dois braços, duas mãos e cinco dedos por mão, sem membros extras ou deformados. Espaço livre nas bordas superior e inferior pra balões de fala.`
- **Continuidade**: primeira aparição do grupo — estabelecer roupas/cores fixas aqui.

### Quadro 2
- **Cenário**: mesmo, plano fechado em Fernando.
- **Personagens**: Fernando (foco), Carol ao fundo desfocada abrindo o notebook.
- **Enquadramento**: close-up dramático (zoom de novela) no rosto de Fernando.
- **Ação**: Fernando já critica antes de qualquer coisa acontecer.
- **Expressões**: sobrancelha erguida, desconfiança máxima.
- **Diálogo (Fernando)**: "Isso aí vai virar sopa de tecnologia. Sinto no ar."
- **Intenção de humor**: exagero de "sexto sentido" de novela + o clichê do sênior cético.
- **Ideia pedagógica**: criticar sem propor alternativa estruturada não ajuda.
- **Prompt visual completo**: `Close-up dramático estilo novela, zoom em Fernando (SEMPRE O MESMO HOMEM: branco, 52 anos, robusto, óculos de leitura pendurados no pescoço, cabelo grisalho curto e ralo no topo, polo azul-marinho) com sobrancelha erguida e expressão de desconfiança extrema, luz levemente dramática vinda de lado. Ao fundo desfocado, Carol (cabelo cacheado castanho-escuro, moletom verde-oliva) abrindo um notebook com adesivo de raio estilizado na tampa. Still fotográfico realista estilo fotonovela/HQ, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão. Espaço livre nas bordas pra balão de fala.`
- **Continuidade**: reforça o adesivo de raio da Carol.

### Quadro 3
- **Cenário**: mesmo, Carol de frente pro notebook.
- **Personagens**: Carol (foco).
- **Enquadramento**: plano médio, tela do notebook virada pra ela (nunca a tampa).
- **Ação**: Carol já está digitando no agente de código.
- **Expressões**: sorriso confiante, dedos rápidos no teclado.
- **Diálogo (Carol)**: "Relaxa! Eu já mandei pro agente: 'crie um chatbot inteligente'. Bora ver o que sai!"
- **Intenção de humor**: a velocidade dela contrastando com a vagueza do próprio pedido.
- **Ideia pedagógica**: pedido vago pro agente reproduz o pedido vago do cliente.
- **Prompt visual completo**: `Plano médio de escritório fictício, Carol (SEMPRE A MESMA MULHER: parda, 27 anos, cabelo CACHEADO castanho-escuro na altura dos ombros, brincos de argola grandes, moletom verde-oliva com estampa geométrica discreta) sentada de frente pro notebook com adesivo de raio na tampa, tela virada pra ela mostrando uma interface de chat genérica com texto borrado ilegível, sorriso confiante, dedos em movimento sobre o teclado. Still fotográfico realista estilo fotonovela/HQ, 16:9, sem texto legível de verdade na tela. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão. TELA sempre virada pra pessoa. Espaço livre pra balão de fala.`
- **Continuidade**: notebook = mesmo adesivo de raio sempre.

### Quadro 4
- **Cenário**: mesmo, Rafa isolado num canto.
- **Personagens**: Rafa (foco).
- **Enquadramento**: plano fechado, Rafa olhando de lado pros outros.
- **Ação**: Rafa não entendeu o pedido mas não vai perguntar.
- **Expressões**: sobrancelhas franzidas, olhar baixo.
- **Narração**: "Rafa também não entendeu. Mas será que só ele?"
- **Diálogo (pensamento, Rafa)**: "Será que eu devia saber isso...?"
- **Intenção de humor/reflexão**: o silêncio dele é o ponto emocional da cena.
- **Ideia pedagógica**: medo de perguntar impede aprendizado.
- **Prompt visual completo**: `Plano fechado de escritório fictício, Rafa (SEMPRE O MESMO HOMEM: negro, 23 anos, magro, alto, cabelo black power curto e aparado, camiseta cinza-mescla lisa, mochila surrada nas costas) sentado num canto da mesa, ombros levemente encurvados, olhando de lado com sobrancelhas franzidas de dúvida, olhar baixo. Still fotográfico realista estilo fotonovela/HQ, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão. Espaço livre pra balão de pensamento.`
- **Continuidade**: mochila sempre nas costas, mesmo sentado.

### Quadro 5
- **Cenário**: mesmo, todos olhando pra tela da Carol agora projetada na TV.
- **Personagens**: os 4.
- **Enquadramento**: plano geral, zoom dramático de novela na TV.
- **Ação**: a resposta do agente aparece — um diagrama de arquitetura absurdamente grande e cheio de caixas.
- **Expressões**: todos de boca aberta, impressionados.
- **Narração**: "O agente respondeu. E respondeu... bastante."
- **Onomatopeia**: "TAN TAN TAN!" (efeito de revelação dramática)
- **Intenção de humor**: exagero de novela — música imaginária de suspense na cena.
- **Ideia pedagógica**: volume de saída não é sinal de qualidade.
- **Prompt visual completo**: `Sala de reunião fictícia, TV na parede mostrando um diagrama de arquitetura de sistema extremamente denso e exagerado, cheio de caixas e setas coloridas, sem texto legível real (formas e blocos genéricos simulando complexidade). Fernando, Carol, Marcelo e Rafa (mesma aparência de sempre de cada um) todos olhando pra TV com expressão de espanto, boca ligeiramente aberta, luz da tela iluminando os rostos, ângulo levemente baixo estilo revelação dramática de novela. Still fotográfico realista estilo fotonovela/HQ, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão para cada personagem. Espaço livre no topo pra caixa de narração.`
- **Continuidade**: reforça roupas/cores fixas dos 4 juntos.

### Quadro 6
- **Cenário**: mesmo, Marcelo derrama café.
- **Personagens**: Marcelo (foco), Fernando ao lado.
- **Enquadramento**: plano médio, café caindo em câmera de novela (leve slow motion sugerido pela pose).
- **Ação**: Marcelo ouve a palavra "produção" e derruba o café.
- **Expressões**: Marcelo em pânico contido; Fernando revirando os olhos.
- **Diálogo (Fernando)**: "Calma, ninguém falou em subir isso pra produção ainda."
- **Diálogo (Marcelo)**: "EU SEI. MAS E SE ALGUÉM FALAR?"
- **Intenção de humor**: exagero físico clássico de comédia de escritório.
- **Ideia pedagógica**: ansiedade antecipando decisões que ainda nem foram tomadas.
- **Prompt visual completo**: `Plano médio de escritório fictício, Marcelo (SEMPRE O MESMO HOMEM: asiático-brasileiro, 38 anos, magro, olheiras leves, cabelo preto curto bem penteado, camisa social azul-clara manga arregaçada) com uma xícara branca caindo da mão, café derramando no ar, expressão de pânico contido, boca entreaberta. Fernando (mesma aparência de sempre: polo azul-marinho, óculos no pescoço, cabelo grisalho) ao lado revirando os olhos com uma leve meia-risada. Still fotográfico realista estilo fotonovela/HQ, leve efeito de câmera lenta na queda do café, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão. Espaço livre pra dois balões de fala.`
- **Continuidade**: xícara branca genérica do Marcelo (não confundir com a caneca do Fernando).

### Quadro 7
- **Cenário**: mesmo, Rafa finalmente reage.
- **Personagens**: Rafa (foco), Carol ao lado incentivando.
- **Enquadramento**: plano fechado, Carol com a mão no ombro de Rafa.
- **Ação**: Rafa quase pergunta algo, mas recua.
- **Expressões**: Rafa hesitante; Carol sorrindo, incentivando com o olhar.
- **Diálogo (Rafa)**: "Gente, eu só queria entender uma coisa... ah, deixa quieto."
- **Diálogo (Carol)**: "Pergunta! Sério."
- **Intenção de humor/reflexão**: o momento mais humano da cena — vulnerabilidade real sem punchline.
- **Ideia pedagógica**: colegas que incentivam perguntas mudam a cultura do time.
- **Prompt visual completo**: `Plano fechado de escritório fictício, Rafa (SEMPRE O MESMO HOMEM: negro, 23 anos, magro, alto, cabelo black power curto, camiseta cinza-mescla, mochila nas costas) com expressão hesitante, começando a falar e recuando, olhar baixo. Carol (SEMPRE A MESMA MULHER: cabelo cacheado castanho-escuro, moletom verde-oliva) ao lado com a mão no ombro dele, sorriso caloroso e incentivador. Still fotográfico realista estilo fotonovela/HQ, luz mais suave e íntima que os quadros anteriores, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão. Espaço livre pra dois balões de fala.`
- **Continuidade**: primeiro momento de conexão Carol-Rafa — reaparece em módulos futuros.

### Quadro 8
- **Cenário**: mesmo, plano geral final, todos olhando pra câmera.
- **Personagens**: os 4.
- **Enquadramento**: plano geral, os 4 olhando diretamente pra câmera (quebra a quarta parede, estilo novela).
- **Ação**: congelamento da cena — ninguém decidiu nada ainda.
- **Expressões**: mistura de dúvida e expectativa nos 4 rostos.
- **Narração**: "Ninguém definiu o problema. Ninguém definiu o comportamento esperado. Ninguém decidiu quem aprovaria isso."
- **Narração (pergunta final)**: "Quando o agente entrega muita coisa, isso significa que a equipe avançou — ou que agora existem mais decisões não examinadas?"
- **Intenção de humor**: nenhum — fecho reflexivo, sem punchline.
- **Ideia pedagógica**: gancho direto pra tese do Módulo 1 (o curso não é sobre ferramentas; agentes ampliam capacidade, não removem responsabilidade).
- **Prompt visual completo**: `Plano geral de escritório fictício, Fernando, Carol, Marcelo e Rafa (mesma aparência de sempre de cada um) lado a lado olhando diretamente pra câmera, expressões misturando dúvida e expectativa, luz neutra de fim de cena, leve profundidade de campo. Still fotográfico realista estilo fotonovela/HQ, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão para cada um dos quatro. Espaço livre no topo e na base pra caixas de narração.`
- **Continuidade**: pose de "grupo" de referência pra futuras aberturas/fechos do módulo 1.

## 7-bis. ✅ PUBLICADO — texto final dos balões (corrigido em 2026-07-17)

O roteiro acima (seção 7) é o PLANO original. Na publicação real, o Diego
apontou que a sequência de diálogos ficava "sem pé nem cabeça" ao ler os
balões isolados — porque cada quadro só comporta 1 balão, e algumas falas do
plano dependiam de uma fala de OUTRO personagem no mesmo quadro (cortada) pra
fazer sentido (ex.: a reação do Marcelo "EU SEI. MAS E SE ALGUÉM FALAR?" só
fazia sentido depois da fala do Fernando sobre produção, que não coube no
balão). O texto final publicado troca essas falas por versões autocontidas —
cada balão precisa fazer sentido sozinho, sem depender de uma fala cortada de
outro quadro:

| Quadro | Tipo | Texto final publicado |
|---|---|---|
| 1 | narr | "Segunda-feira de manhã. Chega um pedido de duas linhas: \"coloca inteligência artificial no atendimento ao cliente\". Só isso — sem mais nenhum detalhe." |
| 2 | fala (Fernando) | "Pedido vago desses sempre vira dor de cabeça depois. Marca minhas palavras." |
| 3 | fala (Carol) | "Relaxa, Fernando! Já mandei pro agente: \"crie um chatbot inteligente\". Vamos ver o que ele traz!" |
| 4 | pensamento (Rafa) | "\"Chatbot inteligente\"... inteligente como, exatamente? Será que só eu fiquei em dúvida?" |
| 5 | narr | "Minutos depois, o agente devolveu uma proposta enorme: banco de dados, vários agentes especialistas, autenticação, integrações — tudo que ninguém tinha pedido." |
| 6 | narr (era fala do Marcelo) | "Alguém mencionou a palavra \"produção\". O café de Marcelo não teve a mesma sorte." |
| 7 | fala (Carol) | "Pergunta, Rafa. Sério — ninguém aqui sabe tudo." |
| 8 | narr | "Ninguém definiu o problema. Ninguém decidiu o que era determinístico ou generativo. Ninguém combinou quem aprovaria a solução. Quando o agente entrega muita coisa, isso significa que a equipe avançou — ou que agora existem só mais decisões sem revisão?" |

**Lição pro roteiro do fecho do Módulo 2 (e módulos futuros)**: escrever cada
balão como uma unidade narrativa completa desde o início — nunca dividir uma
troca de diálogo em duas falas que só fazem sentido juntas, já que cada
quadro só tem 1 balão. Preferir narração pra conectar contexto entre quadros
quando uma piada depender de uma fala anterior que não vai caber.

Também corrigido: posição do balão nos quadros 1 e 5 (estavam sobre rosto de
personagem — canto `tr`/`tl` em cima de gente em pé/sentada perto da borda;
movidos pra `br`/`bl`, na área da mesa).

## 8. Prompts visuais mestre — 1 por personagem (uso em still solo/thumbnail)

- **Fernando (mestre)**: `Retrato de still fotográfico realista de Fernando (SEMPRE O MESMO HOMEM: branco, 52 anos, robusto, óculos de leitura pendurados no pescoço por um cordão, cabelo grisalho curto e ralo no topo, polo azul-marinho, calça social cinza), segurando uma caneca branca surrada com os dizeres "Funciona na minha máquina", braços cruzados, expressão cética, ambiente de escritório de tecnologia fictício desfocado ao fundo, 16:9, sem texto legível além da caneca. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão.`
- **Carol (mestre)**: `Retrato de still fotográfico realista de Carol (SEMPRE A MESMA MULHER: parda, 27 anos, cabelo CACHEADO castanho-escuro na altura dos ombros, brincos de argola grandes, moletom verde-oliva com estampa geométrica discreta), sorriso largo, segurando um notebook com adesivo de raio estilizado na tampa virado pra ela, ambiente de escritório fictício desfocado ao fundo, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão.`
- **Marcelo (mestre)**: `Retrato de still fotográfico realista de Marcelo (SEMPRE O MESMO HOMEM: asiático-brasileiro, 38 anos, magro, olheiras leves, cabelo preto curto bem penteado, camisa social azul-clara manga arregaçada), mãos na cintura, sorriso tenso, ambiente de escritório fictício desfocado ao fundo, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão.`
- **Rafa (mestre)**: `Retrato de still fotográfico realista de Rafa (SEMPRE O MESMO HOMEM: negro, 23 anos, magro, alto, cabelo black power curto e aparado, camiseta cinza-mescla lisa, mochila surrada nas costas), ombros levemente encurvados, olhar de lado, ambiente de escritório fictício desfocado ao fundo, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: dois braços, duas mãos, cinco dedos por mão.`

## 9. Prompt de grupo (os 4 juntos, referência de continuidade)

`Plano geral de escritório de tecnologia fictício, os quatro personagens lado a lado: Fernando (branco, 52 anos, robusto, óculos no pescoço, polo azul-marinho, cabelo grisalho), Carol (parda, 27 anos, cabelo cacheado castanho-escuro nos ombros, moletom verde-oliva, brincos de argola), Marcelo (asiático-brasileiro, 38 anos, magro, camisa azul-clara manga arregaçada, cabelo preto bem penteado) e Rafa (negro, 23 anos, magro, alto, camiseta cinza-mescla, mochila nas costas, cabelo black power curto). Still fotográfico realista estilo fotonovela/HQ contemporânea, luz de escritório natural, 16:9, sem texto legível. ANATOMIA HUMANA CORRETA: exatamente dois braços, duas mãos e cinco dedos por mão para cada um dos quatro personagens, sem membros extras ou deformados.`

## 10. Checklist de continuidade (verificar ANTES de gerar qualquer capítulo futuro)

- [ ] Fernando: polo azul-marinho + óculos no pescoço + caneca "Funciona na minha máquina" + cabelo grisalho ralo no topo?
- [ ] Carol: moletom verde-oliva + cabelo CACHEADO castanho-escuro nos ombros + brincos de argola + adesivo de raio no notebook?
- [ ] Marcelo: camisa azul-clara manga arregaçada + cabelo preto bem penteado + (Post-it na testa só em cena de crise)?
- [ ] Rafa: camiseta cinza-mescla + mochila nas costas + cabelo black power curto?
- [ ] Nenhum personagem com anatomia deformada (2 braços, 2 mãos, 5 dedos)?
- [ ] Nenhuma tela de notebook/celular virada de costas pra câmera?
- [ ] Nenhum balão desenhado DENTRO da imagem pelo Gemini?
- [ ] Nenhum texto legível de verdade na imagem (só blocos borrados quando necessário)?
- [ ] Nenhuma marca, cliente, produto ou dado real citado?
- [ ] Ambiente sempre o mesmo escritório fictício (mesma paleta arquitetônica)?
- [ ] Após gerar: varredura de posição de balão (canto oposto ao rosto) feita quadro a quadro?

## 11. Arco emocional (Módulo 1)

- **Fernando**: começa cético e fechado; termina sem solução, mas o ceticismo
  dele já plantou a dúvida certa pro grupo (ainda não resolvida — arco continua).
- **Carol**: começa confiante e rápida; termina impressionada mas ainda sem
  perceber o próprio ponto cego (confundir volume com qualidade).
- **Marcelo**: começa sob pressão, tenta segurar tudo sozinho; termina em
  pânico contido, sem conseguir organizar a equipe ainda.
- **Rafa**: começa em silêncio, quase pergunta e recua; termina com uma
  primeira fresta de coragem (a Carol o incentivou), mas ainda não perguntou de verdade.

## 11-bis. ✅ PUBLICADO — Abertura do Módulo 2 (gap corrigido em 2026-07-18)

Lesson `9a23a332-dc07-4470-84d8-522806d2dd42`, inserida logo após "O que
realmente existe por trás de um chat" (1ª lesson do Módulo 2). Faltava desde
a produção original — só o fecho do M2 existia. Desafio novo: mensagens
livres do cliente em linguagem natural. Aplica o arco cumulativo: Rafa já
pergunta antes de agir (aprendizado do M1), Fernando já se preocupa antes de
reclamar, Marcelo já puxa o checklist do módulo anterior — mas nenhum deles
ainda sabe o que fazer com histórico de conversa, papéis de mensagem ou
janela de contexto (conteúdo específico do M2, ainda não ensinado). Termina
em pergunta aberta, sem resolver — resolve no fecho já publicado (seção 12).

Texto final dos 8 balões:

| Quadro | Tipo | Texto |
|---|---|---|
| 1 | narr | "Nova solicitação chega: o chatbot precisa entender mensagens livres do cliente, não só números de menu. Desta vez, ninguém corre pro código sem perguntar antes — mas as perguntas certas ainda não são óbvias." |
| 2 | fala (Rafa) | "Peraí — o agente vai lembrar de tudo que o cliente já disse na conversa, ou só da última mensagem? Isso muda a resposta, né?" |
| 3 | narr | "Ninguém sabia responder. Carol resolveu na marra: colar a conversa inteira, palavra por palavra, em cada nova pergunta pro modelo." |
| 4 | fala (Fernando) | "E se a conversa for longa? A gente vai mandar isso tudo pro modelo pra sempre? Tem limite nisso, ou não?" |
| 5 | narr | "Marcelo puxou o checklist do módulo passado — objetivo, restrições, aprovação. Ajudou. Mas nenhuma pergunta dali explicava o que fazer com o histórico da conversa." |
| 6 | fala (Carol) | "A gente já sabe separar o que é regra fixa do que é o modelo decidindo. Só não sabe onde a conversa mora entre uma mensagem e outra." |
| 7 | fala (Rafa) | "Será que existe um jeito de guardar só o que importa da conversa, em vez de tudo?" |
| 8 | narr | "O time já sabia perguntar antes de agir. Mas uma conversa com um modelo tem peças que ninguém tinha aberto ainda: papéis, memória, limite de contexto. Por onde começar?" |

**Lição nova desta rodada**: 2 dos 8 quadros (q1, q3) precisaram de uma 2ª
geração — o Gemini desenhou texto REALMENTE legível numa TV/tela na 1ª
tentativa mesmo com o guard padrão, e o notebook da Carol saiu sem o
adesivo de raio e com a tela virada pra câmera em vez de pra ela. Fix:
reforçar o guard de texto pra ser explícito sobre "BORRADO E ILEGÍVEL, nunca
palavras reais" (não só "sem texto legível"), e no prompt do notebook da
Carol, dizer explicitamente "adesivo de raio bem visível na TAMPA de trás,
voltada pra câmera" em vez de confiar só na persona canônica genérica.

## 12. ✅ PUBLICADO — Fecho do Módulo 2

Lesson `745421e7-ed23-4342-abbe-851434451c88` ("Fotonovela: O Escritório dos
Agentes (fecho)"), inserida no fim do Módulo 2 (depois de "Primeira evolução
generativa"). Situação: chega um pedido parecido com o da abertura do
Módulo 1 ("o chatbot precisa entender mensagens livres dos clientes"), mas
agora conduzido com método — Rafa é o primeiro a perguntar o que continua
determinístico x generativo; Fernando identifica risco de fallback; Carol
quase escreve "faça tudo" pro agente e se autocorrige; Marcelo revela um
checklist (objetivo, critérios de aceite, riscos, testes, evidências,
aprovação); o agente devolve um plano pequeno e testável; a equipe celebra
clareza, não volume de código.

Texto final dos 8 balões (já escritos autocontidos desde o início, aplicando
a lição da abertura do Módulo 1):

| Quadro | Tipo | Texto |
|---|---|---|
| 1 | narr | "Nova solicitação chega: \"o chatbot precisa entender mensagens livres dos clientes\". Desta vez, ninguém corre pro código primeiro." |
| 2 | fala (Rafa) | "Antes de mexer em qualquer coisa: o que precisa continuar determinístico, e o que já pode ser gerado pelo modelo?" |
| 3 | fala (Fernando) | "Boa pergunta. E o que acontece quando o modelo não tiver confiança na resposta? Precisamos de um fallback certo." |
| 4 | narr | "Carol quase digitou \"faça tudo\" pro agente. Parou. Apagou. Recomeçou com objetivo, contexto e limites." |
| 5 | fala (Marcelo) | "Objetivo, critérios de aceite, riscos, testes, evidências, ponto de aprovação. Ninguém entra em produção sem isso." |
| 6 | narr | "Juntos, mapearam o que pertence à sessão, o que pertence ao usuário, quando resumir a conversa e como sempre voltar pro menu determinístico se o modelo falhar." |
| 7 | fala (Carol) | "O agente devolveu um plano pequeno, claro e testável. Nem parece a mesma Carol de duas aulas atrás, hein?" |
| 8 | narr | "Ninguém comemorou o tanto de código. Comemoraram o comportamento ficar compreensível, limitado e testável. Entender uma conversa não serve só pra conversar melhor com uma LLM — serve pra projetar sistemas em que contexto, estado, regras e geração têm responsabilidades claras." |

### ⚠️ Problema recorrente encontrado nesta rodada: elenco "derrapa" em cenas de grupo

Ao gerar quadros com os 4 personagens juntos (ou pares menos comuns, como
Fernando+Rafa), o Gemini com frequência **ignora a persona canônica e insere
gente genérica** — aconteceu em 3 dos 8 quadros desta fotonovela (q3, q5,
q6/q8 nas primeiras tentativas). Sintoma: cenas de grupo/prompt mais longo
"diluem" a atenção do modelo às descrições de cada personagem.

**Mitigação que funcionou**: no PROMPT de qualquer quadro com 2+
personagens, repetir a descrição completa (`SEMPRE O MESMO HOMEM/A MESMA
MULHER: ...`) de CADA personagem presente, mesmo que pareça redundante —
nunca abreviar pra só o nome ou "mesma aparência de sempre" depois da
primeira menção em quadros de grupo. Frames com 1 pessoa só raramente têm
esse problema; quanto mais gente no quadro, maior o risco — vale gerar e
CONFERIR cada quadro de grupo antes de seguir, e regenerar sem economia de
prompt se sair errado (aconteceu 3x nesta rodada, todas resolvidas na
2ª tentativa com o prompt completo).

## 13. Lições consolidadas pra próximos módulos

1. Cada balão precisa fazer sentido sozinho (seção 7-bis).
2. Balão não pode ser desenhado dentro da imagem pelo Gemini — reforçar
   explicitamente "NÃO desenhe balão/nuvem/texto" no prompt sempre, não só
   quando der errado.
3. Em quadros de grupo (2+ personagens), sempre repetir a descrição
   completa de cada um no prompt — nunca abreviar.
4. Conferir TODOS os quadros de grupo visualmente antes de subir — a taxa
   de erro em cenas de grupo é alta o suficiente (nesta rodada: 3/8) pra
   nunca pular essa checagem.
5. Posição de balão: corners de TOPO (`tl`/`tr`) frequentemente cobrem rosto
   quando os personagens estão em pé (cabeça chega perto da borda superior
   do quadro 16:9). Preferir corners de BAIXO (`bl`/`br`, área de mesa/chão)
   como ponto de partida — regenerar/reposicionar visualmente depois se
   ainda cobrir algo.

## 14. ✅ PUBLICADO — Fecho do Módulo 1

Lesson `a8b94eac-8a4e-473e-972f-f45f6b07b90f` ("Fotonovela: O Escritório dos
Agentes (fecho)"), inserida no fim do Módulo 1 (antes de "Prova e reflexão do
módulo"). Resolve exatamente a cena em aberto na abertura do M1: o mesmo
pedido vago volta à mesa, mas agora conduzido com método — Marcelo organiza
objetivo/restrições/aprovação, Fernando revisa o plano antes de qualquer
código (construtivo, não mais só cético), Rafa finalmente faz a pergunta que
não fez na abertura ("o que exatamente esse chatbot precisa resolver?"),
silêncio reflexivo quando percebem que ninguém tinha respondido isso antes,
Carol pede a menor mudança com contexto/limite/plano em vez de "crie um
chatbot inteligente", o agente devolve algo pequeno e revisável, o time
aprova sabendo o que está aprovando. Fecha com a tese de HITL: não é
desconfiar do agente, é saber onde a decisão continua sendo humana.

Todos os 8 quadros saíram corretos na primeira tentativa (validação da lição
#3 acima — repetir a descrição completa de cada personagem em toda cena de
grupo eliminou o problema de elenco genérico que apareceu 3x no fecho do
Módulo 2). Balões todos posicionados em cantos inferiores (`bl`/`br`) desde
o início — nenhuma correção de posição necessária (validação da lição #5).

Com isso, a base narrativa do Módulo 1 e do Módulo 2 está completa (abertura
+ fecho dos dois). Próximo: Módulo 3 (Spec Driven Development) em diante,
seguindo a regra do arco cumulativo (seção 2).

## 15. ✅ PUBLICADO — Fotonovela do Módulo 3 (Spec Driven Development)

**Desafio novo do módulo**: até aqui o time já aprendeu a perguntar antes de
agir (M1) e a separar determinístico de generativo (M2) — mas ninguém ainda
guarda a intenção aprovada em lugar nenhum. Cada prompt nasce, funciona uma
vez, e some. Sem versionamento, sem reprodutibilidade, sem contexto em
camadas.

Texto final dos 8 balões:

| Quadro | Tipo | Texto |
|---|---|---|
| 1 | narr | "Um card de tarefa chega: \"implementar handoff pro atendimento humano quando o cliente pede\". Desta vez, o time já pergunta o que é determinístico e o que é generativo antes de tocar em código." |
| 2 | fala (Fernando) | "Beleza, mas cadê o texto que a gente aprovou pro agente executar ontem? Porque hoje ninguém lembra por quê funcionou." |
| 3 | narr | "Carol procura o prompt de ontem. Encontra três versões diferentes, escritas direto no chat — nenhuma salva em lugar nenhum." |
| 4 | fala (Marcelo) | "A gente aprendeu a perguntar a coisa certa. Mas não aprendeu a guardar a resposta. Isso não escala." |
| 5 | narr | "Foi aí que pararam de reescrever o pedido do zero toda vez — e começaram a tratar a intenção aprovada como um artefato: uma Spec." |
| 6 | fala (Rafa) | "Se a spec fica versionada junto com o código, da próxima vez a gente sabe exatamente o que mudou e por quê." |
| 7 | narr | "No lugar de um prompt gigante e solto, entraram camadas: regra do domínio primeiro, restrição do sistema depois, e só então o pedido específico da tarefa." |
| 8 | narr | "A spec não deixou o trabalho mais lento. Deixou reproduzível — a próxima pessoa, ou o próximo agente, não precisa mais adivinhar o que já tinha sido decidido." |

Lesson `5ed7355c-9326-4821-9b3c-4e2a7fceff9f`, inserida como penúltima do
Módulo 3 (antes de "Prova e laboratório do módulo"). Todos os 8 quadros
saíram corretos na primeira tentativa (elenco reconhecível em todas as
cenas de grupo, sem balão desenhado, sem anatomia deformada). Balões
alternando `br`/`bl` desde o início — nenhuma correção de posição
necessária.

**⚠️ Bug de upload descoberto nesta rodada**: ao fazer upload em lote dos 8
slides via `curl -F "caption=$cap"` num loop bash, a legenda do PRIMEIRO
quadro (cuja legenda continha aspas duplas escapadas, ex.:
`"implementar handoff..."`) chegou vazia no servidor, e todas as legendas
seguintes ficaram **deslocadas uma posição pra trás** (a legenda do quadro N
foi parar no quadro N+1). Causa: aspas duplas dentro do valor de `-F`
quebram o parsing do multipart nalgum ponto do pipeline curl→gateway. Fix
usado: gravar cada payload de correção em arquivo JSON separado
(`--data-binary @payload.json`) e corrigir quadro a quadro via `PUT
.../slides/{id}` depois do upload, em vez de confiar no valor de `caption`
enviado inline no upload multipart quando o texto contém aspas. Também
notado: chamadas via Python `urllib` tomam **403 Cloudflare (error 1010,
bloqueio de WAF por assinatura de user-agent)** neste domínio — usar sempre
`curl` pra chamadas à API de produção, nunca `urllib`/`requests` puro.
