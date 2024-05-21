from threading import Thread
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS

import cut
import record

duracao_video_principal = 60
recortar_ultimos_x_segundos = 5

api_bp = Flask(__name__)
CORS(api_bp)

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

@api_bp.route('/rec/start', methods=['POST'])
def start_record():
    global recordGroup

    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            return jsonify({'error': f'Uma gravação já está em andamento para a câmera {camera["camera"]}'}), 400
        
        camera['lastFullName'] = record.buildFullRecordName(camera['camera'])
        camera['gravacao_thread'] = Thread(target=record.gravar_video_principal,
                                           args=(camera['camera'], camera['lastFullName'], duracao_video_principal))
        camera['gravacao_thread'].start()

    return jsonify({'message': 'Iniciando gravação de vídeo para todas as câmeras...'})


@api_bp.route('/cut', methods=['POST'])
def recortar_video():
    global recordGroup
    cutNames = []
    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            record.parar_gravacao()
            camera['gravacao_thread'].join()

        cutName = cut.buildCutName(camera['camera'])
        cutNames.append(cutName)
        recorte_thread = Thread(target=cut.recortar_ultimos_x_segundos,
                                args=(camera['lastFullName'], cutName, recortar_ultimos_x_segundos))
        recorte_thread.start()
        recorte_thread.join()

    start_record()

    video_path = '../'
    print(cutNames[0])
    return send_from_directory(video_path, cutNames[0])

@api_bp.route('/rec/stop', methods=['POST'])
def parar_gravacao():
    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            record.parar_gravacao()
            camera['gravacao_thread'].join()
            return jsonify({'message': 'Parando gravação de vídeo...'})


@api_bp.route('/isrecording', methods=['GET'])
def has_recording():
    for camera in recordGroup['cameraGroup']:
        if camera['gravacao_thread'] and camera['gravacao_thread'].is_alive():
            return jsonify({
                "isRecording": True,
                'message': 'group: ' + recordGroup['name'] + ' is recording'})
        return jsonify({
            'message': 'no group recording',
            "isRecording": False})

@api_bp.route('/home')
def home():
    return render_template('html.html')


if __name__ == '__main__':
    api_bp.run(host='0.0.0.0', debug=True)
