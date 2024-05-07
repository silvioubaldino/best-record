from threading import Thread, Event, Lock
from flask  import Flask, Blueprint, jsonify
import record, cut

duracao_video_principal = 60
recortar_ultimos_x_segundos = 5

api_bp = Flask(__name__)

# Estrutura do objeto recordGroup
recordGroup = {
    "name": "Via A",
    "cameraGroup": [
        {
            "camera": 0,
            "gravacao_thread": None,
            "lastFullName": ""
        },
        {
            "camera": 1,
            "gravacao_thread": None,
            "lastFullName": ""
        }
    ]
}

@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

@api_bp.route('/gravar', methods=['POST'])
def gravar_video():
    global recordGroup

    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            return jsonify({'error': f'Uma gravação já está em andamento para a câmera {camera["camera"]}'}), 400
        
        camera['lastFullName'] = record.buildFullRecordName(camera['camera'])
        camera['gravacao_thread'] = Thread(target=record.gravar_video_principal, args=(camera['camera'], camera['lastFullName'], duracao_video_principal))
        camera['gravacao_thread'].start()
    
    return jsonify({'message': 'Iniciando gravação de vídeo para todas as câmeras...'})

@api_bp.route('/recortar', methods=['POST'])
def recortar_video():
    global recordGroup

    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            record.parar_gravacao()
            camera['gravacao_thread'].join()

        cutName = cut.buildCutName(camera['camera'])
        recorte_thread = Thread(target=cut.recortar_ultimos_x_segundos, args=(camera['lastFullName'], cutName, recortar_ultimos_x_segundos))
        recorte_thread.start()
        recorte_thread.join()

    gravar_video()
    return jsonify({'message': 'Iniciando recorte de vídeo para todas as câmeras...'})

if __name__ == '__main__':
    api_bp.run(debug=True)
