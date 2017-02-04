#code for torrent part
#needs to have libtorrent library
import libtorrent as lt
import time

#boths arguments are in string format, torrent has .torrent format and destination can be only . to save in folder with code
#torrent files needs to be in same directory as code
def downloadFile(torrentFile, destination):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    e = lt.bdecode(open(torrentFile, 'rb').read())
    info = lt.torrent_info(e)

    params = { 'save_path': destination, 'storage_mode': lt.storage_mode_t.storage_mode_sparse, 'ti': info }
    h = ses.add_torrent(params)

    s = h.status()
    while (not s.is_seeding):
            s = h.status()

            state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
            print s.state
            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state])

            time.sleep(1)
