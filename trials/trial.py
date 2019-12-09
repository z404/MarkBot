from alexa_client import AlexaClient
client = AlexaClient(
    client_id='amzn1.application-oa2-client.7759dfa8e60649bab3f53e86a8b1ffa2',
    secret='e3ce929b60a3ba00c1b65d5eb8e9f0d3f6f0e2f4d1ec958eb84877e163faeab6',
    refresh_token= 'Atzr|IwEBIOf0OdcsihKCtm727Vud0eNH_JmUMUVdbCLrkaXIXhTtfSR7eYAQcDaNyA5MsCfXClX4eZlNLkiy0JI3YdxgC7PMOvCYf0YOZ91_JJPyngKyenWgs9RB0aQQOpGDDCGJHOpyNAvoTJkUSqr-YwsiZAYWa3VwKK5ezirYBFzev42i18B36loCV_68nAlWcmyW9ZEPJsLq74n41si344t64ru1I1linIJ-qIO7S1bldheplswVy5nvRBHk-OKzMf3SJyvNpx79pKRizhwsOkQGKiGNhJ4EIKmt7QomIpt6XzOPEaMbk3GHCNrtE80MgjD6JZTxctjCfp3N90ihqaar8Pyfp1w0P3VeSeKO5sYA9zEbwQldifZeb4xpQHwZk2ArTPx5LfH_HnKGYd4bDsdqSdrWebdcnsZrglO_uEbpG_1VRHj1mfhykO0sAHI32-L6Xwo')

    
client.connect()  # authenticate and other handshaking steps
with open('outputlol.wav', 'rb') as f:
    #a = client.send_audio_file(f)
    for i, directive in enumerate(client.send_audio_file(f)):
        if directive.name in ['Speak', 'Play']:
            with open(f'./output_{i}.mp3', 'wb') as f:
                f.write(directive.audio_attachment)
