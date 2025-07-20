from app.process import main
from pathlib import Path

if __name__ == "__main__":

    main(
        img_path=Path("./public/piano.jpg"),
        partition_path=Path("public\midi\Vivaldi_-_Winter_Rousseau_Version_Original.mid"),
        height=1312,
        width=738,
        output_dir=Path("./output"),
        fps=30,
        sf2_path=Path("public\sf2\MuseScore_General.sf2"),
        #sf2_path=Path("public\sf2\piano.sf2"),
    )