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
    print(duracao_total_segundos)

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

def recortar_ultimos_x_segundos_from_buffer(frame_buffer, output_file, recortar_ultimos_x_segundos):
    # Verifica se há frames no buffer
    if not frame_buffer:
        print("Nenhum frame disponível no buffer")
        return

    print("Frames no buffer:", len(frame_buffer))
    # Obtém o FPS do vídeo a partir do primeiro frame no buffer
    fps = frame_buffer[0]["fps"]

    # Calcula o tempo de início do recorte (em segundos)
    duracao_total_segundos = len(frame_buffer) / fps
    start_time = duracao_total_segundos - recortar_ultimos_x_segundos
    if start_time < 0:
        start_time = 0

    # Calcula os frames correspondentes ao tempo de início e término do recorte
    start_frame = int(start_time * fps)
    end_frame = start_frame + int(recortar_ultimos_x_segundos * fps)

    # Cria um objeto cv2.VideoWriter para gravar o vídeo recortado
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = frame_buffer[0]["frame_width"]
    frame_height = frame_buffer[0]["frame_height"]
    out = cv2.VideoWriter(output_file, codec, fps, (frame_width, frame_height))

    print("start_frame:", start_frame)
    print("end_frame:", end_frame)

    # Escreve os frames do buffer no arquivo de vídeo recortado
    for i in range(start_frame, end_frame):
        frame = frame_buffer[i]["frame"]
        out.write(frame)

    # Libera os recursos
    out.release()

    print("Vídeo recortado com sucesso")

def buildCutName():
    timestamp_atual = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    name = "cut" + timestamp_atual + ".mp4"
    return name
