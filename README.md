
Este scraper recolhe a lista de cargos do 19º Governo (Passos Coelho) a partir do [site do Parlamento](http://www.parlamento.pt).

Método
------

Este scraper é muito simples, já que toda a informação que precisamos está na página do [Registo de interesses dos membros do Governo](http://www.parlamento.pt/RegistoInteresses/Paginas/RegistoInteressesMembros_XIX_Governo.aspx).

A partir daí, é analisar os conteúdos e extrair os dados sem grandes dores.

Como usar
---------

Para a ajuda dos comandos do script:

    python scraper-interessesgov.py --help

Para correr:

    python scraper-interessesgov.py

Para ter resultados em JSON em vez de CSV:

    python scraper-interessesgov.py --format json


Campos do CSV/JSON resultante
-------------------------

  * `name` -- Título da iniciativa (_Proposta de Lei 231/XII_)
  * `post` -- Sumário da iniciativa 
  * `start_date` -- Número de identificação do documento no Parlamento.pt (_38526_)
  * `end_date` -- Lista dos autores do documento


