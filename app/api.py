from threading import Thread, Event, Lock
from flask  import Flask, Blueprint, jsonify
import record, cut

duracao_video_principal = 60
recortar_ultimos_x_segundos = 5

api_bp = Flask(__name__)
gravacao_thread = None  # Variável para armazenar a thread de gravação atual
lastFullRecordName = ""

@api_bp.route('/ping', methods=['GET'])
def ping():
    # Coloque aqui a lógica para iniciar o processo de gravação de vídeo
    return jsonify({'message': 'pong'})

@api_bp.route('/gravar', methods=['POST'])
def gravar_video():
    global gravacao_thread
    global lastFullRecordName

    if gravacao_thread and gravacao_thread.is_alive():
        return jsonify({'error': 'Uma gravação já está em andamento'}), 400
    
    lastFullRecordName = record.buildFullRecordName()
    print(lastFullRecordName)

    gravacao_thread = Thread(target=record.gravar_video_principal, args=(lastFullRecordName, duracao_video_principal))
    gravacao_thread.start()
    
    return jsonify({'message': 'Iniciando gravação de vídeo...'})

@api_bp.route('/recortar', methods=['POST'])
def recortar_video():
    global gravacao_thread
    global lastFullRecordName
    if gravacao_thread and gravacao_thread.is_alive():
        record.parar_gravacao()
        gravacao_thread.join()

    cutName = cut.buildCutName()
    recorte_thread = Thread(target=cut.recortar_ultimos_x_segundos, args=(lastFullRecordName, cutName, recortar_ultimos_x_segundos))
    recorte_thread.start()
    recorte_thread.join()

    gravar_video()
    return jsonify({'message': 'Iniciando recorte de vídeo...'})

if __name__ == '__main__':
    api_bp.run(debug=True)

# Mudar a abordagem?
# Ao socilicitar o recorte, parar a gravacao e iniciar a proxima,
# liberando esse primeiro arquivo para recortar os ultimos x segundos