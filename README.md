# Álgebra Linear - APS 3 - 2024.1 [Insper](https://www.insper.edu.br/pt/home)

## Autores do Projeto
- [Ian Cordibello Desponds](https://github.com/iancdesponds)
- [Gustavo Barroso Cruz](https://github.com/Gubscruz)

# [Transformações Matriciais Instantâneas na Câmera](https://github.com/iancdesponds/algebra-linear-transformacoes-matriciais-camera)

## Como rodar o programa:
1. Clone o repositório no diretório desejado
2. Rode o comando `python3 demo.py` na pasta do repositório
3. Pressione f para aumentar a velodicade de rotação no sentido anti-horário e s para aumentar no sentido horario. Pressione i para dar zoom in e o para dar zoom out. Pressione q para sair do programa.

## O modelo:

### Matiz de índices dos pixels:
A função `criar_indices` gera uma matriz de coordenadas de cada pixel na imagem original, para que depois possamos aplicar as tranformações desejadas.

### Matrizes de transformação:
#### Tranlação:
A matriz de translação tem o formato:

$$
T =\begin{bmatrix}
1 & 0 & -\frac{width}{2} \\
0 & 1 & -\frac{height}{2} \\
0 & 0 & 1
\end{bmatrix}
$$

Essa matriz é usada para mover o centro da imagem para a origem (0, 0) antes de aplicar a rotação e escala. Isso é feito para garantir que essas transformações sejam aplicadas ao centro da imagem, e não a um canto.

Há também a matriz inversa de translação, que "desfaz" a translação, devolvendo o centro da imagem para a posição original.

#### Rotação:
A matriz de rotação tem o formato:

$$
R =\begin{bmatrix} 
cos(\theta) & -\sin(\theta) & 0 \\
sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 1 \end{bmatrix}
$$

Essa matriz é usada para rotacionar a imagem em torno da origem (0, 0). Ela recebe como parâmetro o ângulo de rotação $\theta$, que determina a quantidade de rotação que será aplicada. Isso permite que controlemos a velocidade e direção da rotação.

#### Escala:
A matriz de escala (zoom) tem o formato:

$$
S =\begin{bmatrix}
zoom & 0 & 0 \\
0 & zoom & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

Essa matriz é usada para aumentar ou diminuir o tamanho da imagem. Ela recebe como parâmetro o fator de escala `zoom`, que determina a quantidade de zoom que será aplicada.


### Aplicação das transformações:
Para aplicar todas as tranformações desejadas ao mesmo tempo e na ordem correta, multiplicamos as matrizes de transformação na ordem inversa em que queremos que elas sejam aplicadas. Para isso, criamos uma matriz que é o resultado da multiplicação das matrizes de translação, rotação e escala, na ordem certa, para que ela realize todas as transformações desejadas. Essa matriz A é dada por:

$$
A = T^{-1} \cdot S \cdot R \cdot T
$$

Primeiro aplicamos a translação, movendo o centro da imagem para a origem, depois aplicamos a rotação desejada, depois aplicamos o zoom desejado, e, por fim, aplicamos a inversa da translação, devolvendo o centro da imagem para a posição original.

Para mapear os pixels da imagem original para a imagem transformada, multiplicamos a matriz de índices dos pixels pelo inverso da matriz A ($A^{-1}$). Usamos o inverso de A porque quando ela é aplicada para cada posição da imagem transformada, ela devolve a posição correspondente na imagem original, indicando qual pixel deve ser copiado para aquela posição.

Para garantir que nenhum pixel da imagem transformada esteja fora dos limites da imagem original, usamos um filtro que só copia os pixels que estão dentro dos limites da imagem original.
