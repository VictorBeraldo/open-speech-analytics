from pytube import Playlist
from tqdm import tqdm

def extrair_links_playlist(url_playlist):
    playlist = Playlist(url_playlist)
    playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"

    # Incluindo metadados e o nome da playlist
    playlist_nome = playlist.title
    videos_info = []

    for video in tqdm(playlist.videos):
        video_info = {
            "titulo": video.title,
            "url": video.watch_url,
            "duração": video.length,
            "visualizações": video.views,
            "avaliação": video.rating,
            "autor": video.author,
            "descrição": video.description,
            "data_publicação": video.publish_date,
            "curtidas": video.rating,  # Este campo parece estar duplicado ou mal atribuído
            "keywords": video.keywords  # Adicionando palavras-chave
        }
        # Tenta capturar dados adicionais que podem não estar disponíveis
        try:
            video_info.update({
                "número_curtidas": video.vid_info.get('like_count'),
                "número_descurtidas": video.vid_info.get('dislike_count')
            })
        except AttributeError:
            video_info.update({
                "número_curtidas": "Dados não disponíveis",
                "número_descurtidas": "Dados não disponíveis"
            })

        videos_info.append(video_info)
    
    return playlist_nome, videos_info

