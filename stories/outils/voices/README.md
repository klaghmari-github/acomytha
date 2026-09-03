Voix Piper (fichiers `.onnx` gitignorés, ~60–75 Mo chacun).

| Fichier | Rôle |
| --- | --- |
| `fr_FR-tom-medium` | narrateur ; héros garçon (pitch +) |
| `fr_FR-siwis-medium` | maman ; héroïne (pitch +) ; grand-mère (pitch −) |
| `fr_FR-upmc-medium` | papa (speaker `pierre`=1) ; maîtresse (`jessica`=0) ; copains |
| `fr_FR-gilles-low` | grand-père ; directeur |

```
base=https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR
curl -L -o fr_FR-siwis-medium.onnx $base/siwis/medium/fr_FR-siwis-medium.onnx
curl -L -o fr_FR-tom-medium.onnx $base/tom/medium/fr_FR-tom-medium.onnx
curl -L -o fr_FR-upmc-medium.onnx $base/upmc/medium/fr_FR-upmc-medium.onnx
curl -L -o fr_FR-gilles-low.onnx $base/gilles/low/fr_FR-gilles-low.onnx
```

(et les `.onnx.json` correspondants)
