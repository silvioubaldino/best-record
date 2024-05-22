import cv2
from datetime import datetime

def recortar_ultimos_x_segundos(video_principal, output_file, recortar_ultimos_x_segundos):
    cap = cv2.VideoCapture(video_principal)

    # Verifica se o arquivo de vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o arquivo de vídeo")
        return

    # Obtenha a duração total do vídeo (em segundos)
    duracao_total_segundos = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS))

    # Calcule o tempo de início do recorte (em segundos)
    start_time = duracao_total_segundos - recortar_ultimos_x_segundos
    if start_time < 0:
        start_time = 0

    # Converta o tempo de início do recorte de segundos para frames
    start_frame = int(start_time * int(cap.get(cv2.CAP_PROP_FPS)))

    # Converta os tempos para frames
    end_frame = int(duracao_total_segundos * int(cap.get(cv2.CAP_PROP_FPS)))

    # Crie um objeto cv2.VideoWriter para gravar o vídeo recortado
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, codec, int(cap.get(cv2.CAP_PROP_FPS)), (frame_width, frame_height))

    # Avance para o frame inicial do recorte
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    print("start_frame:", start_frame)
    print("end_frame:", end_frame)

    # Leitura dos frames e gravação no arquivo de vídeo recortado
    while cap.isOpened() and start_frame < end_frame:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    # Libera os recursos
    cap.release()
    out.release()

    print("Vídeo recortado com sucesso")


def buildCutName(cameraName):
    timestamp_atual = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    name = "cut-camera" + str(cameraName) + "-" + timestamp_atual + ".mp4"
    return name
