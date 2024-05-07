import cv2
from datetime import datetime

# Variável de controle para parar a gravação
_gravacao_ativa = True

def gravar_video_principal(camera, video_filename, duracao_video_principal):
    global _gravacao_ativa
    _gravacao_ativa = True
    cap = cv2.VideoCapture(camera)  # Abre a câmera padrão

    # Verifica se a captura foi iniciada corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return

    codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec de vídeo
    fps = 30
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(video_filename, codec, fps, (frame_width, frame_height))  # Inicia a gravação

    # Inicializa o contador de frames
    num_frames = 0

    while cap.isOpened() and _gravacao_ativa:
        ret, frame = cap.read()  # Captura um frame

        if ret:
            out.write(frame)  # Grava o frame no vídeo
            num_frames += 1

            # Verifica se a duração máxima foi atingida
            if num_frames / fps >= duracao_video_principal:
                break
        else:
            break

    # Libera os recursos
    cap.release()
    out.release()

    print("Gravação concluída")

def parar_gravacao():
    global _gravacao_ativa
    _gravacao_ativa = False

def buildFullRecordName(cameraName):
    timestamp_atual = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    name = "fullRecord-camera" + str(cameraName) + "-" + timestamp_atual + ".avi"
    return name
