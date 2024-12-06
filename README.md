# Nome do Jogo: Music Fight

O build já foi feito e o executável está pronto para uso na pasta principal.

## Gerar o Build e Executável

Para gerar o build e gerar o executável, execute o seguinte comando:

```bash
python -m PyInstaller --onefile --windowed --add-data "assets\;assets" --add-data "music\;music" --add-data "musica_easy\;musica_easy" --add-data "Sprites\;Sprites" --add-data "telaFimJogo\;telaFimJogo" --add-data "telaInicial\;telaInicial" --add-data "Telas\;Telas" main.py
