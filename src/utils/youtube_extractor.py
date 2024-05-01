from pytube import Playlist

def extrair_links_playlist(url_playlist):
    playlist = Playlist(url_playlist)
    playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"

    # Incluindo metadados e o nome da playlist
    playlist_nome = playlist.title
    videos_info = []

    for video in playlist.videos:
        video_info = {
            "titulo": video.title,
            "url": video.watch_url,
            "duração": video.length,
            "visualizações": video.views,
            "avaliação": video.rating,
            "data_publicação": video.publish_date  # Adicionando a data de publicação
        }
        videos_info.append(video_info)
    
    return playlist_nome, videos_info
