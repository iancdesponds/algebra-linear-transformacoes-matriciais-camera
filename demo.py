import numpy as np
import cv2 as cv
import itertools


def criar_indices(min_i, max_i, min_j, max_j):
    # Cria uma lista de todos os pares possíveis de índices (i, j)
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    # Separa os índices i e j em dois arrays numpy
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    # Empilha os arrays de índices i e j verticalmente
    idx = np.vstack((idx_i, idx_j))
    return idx


def run():
    cap = cv.VideoCapture(0)
    width = 400
    height = 400
    tetha = 0
    vel = 0
    zoom = 1.0

    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não consegui capturar frame!")
            break

        frame = cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)
        # Converte o frame para o formato float e normaliza os valores dos pixels
        image = np.array(frame).astype(float) / 255
        newimage = np.zeros_like(image)

        # Cria índices para todos os pixels da imagem
        Xd = criar_indices(0, width, 0, height)
        # Adiciona uma terceira linha de uns para possibilitar a aplicação de transformações homogêneas
        Xd = np.vstack((Xd, np.ones(Xd.shape[1])))


        key = cv.waitKey(1)
        # Ajusta a velocidade de rotação
        if key == ord('f'):
            vel += 1
        if key == ord('s'):
            vel -= 1
        # Ajusta o nível de zoom 
        if key == ord('i'):  # Aumenta o zoom
            zoom *= 1.1
        if key == ord('o'):  # Diminui o zoom
            zoom /= 1.1

        # Atualiza o ângulo de rotação
        tetha += 1 + vel
        # Converte o ângulo de rotação para radianos
        tetha_radians = np.radians(tetha)

        # Matrizes de transformação
        T = np.array([[1, 0, -width / 2],
                      [0, 1, -height / 2],
                      [0, 0, 1]])  # Translação para o centro
        R = np.array([[np.cos(tetha_radians), -np.sin(tetha_radians), 0],
                      [np.sin(tetha_radians),  np.cos(tetha_radians), 0],
                      [0, 0, 1]])  # Rotação
        S = np.array([[zoom, 0, 0],
                      [0, zoom, 0],
                      [0, 0, 1]])  # Escala

        T2 = np.linalg.inv(T)  # Translação inversa

        # Combina as transformações para formar a matriz de transformação final
        A = T2 @ S @ R @ T

        # Aplica a transformação inversa aos índices dos pixels
        B = np.linalg.inv(A) @ Xd

        Xd = Xd.astype(int)
        B = B.astype(int)

        # Filtra os índices para manter apenas aqueles que estão dentro das dimensões da imagem
        filtro = (B[0, :] >= 0) & (B[0, :] < width) & (B[1, :] >= 0) & (B[1, :] < height)

        # Aplica o filtro aos índices
        Xd = Xd[:, filtro]
        B = B[:, filtro]

        # Atribui os valores dos pixels transformados à nova imagem
        newimage[Xd[0, :], Xd[1, :], :] = image[B[0, :], B[1, :], :]
        # Exibe a imagem transformada
        cv.imshow('Imagem do Ian e do Gubs!', newimage)

        if key == ord('q') or cv.getWindowProperty('Imagem do Ian e do Gubs!', cv.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    run()
