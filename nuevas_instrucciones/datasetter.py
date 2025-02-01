#cambiar las rutas

#/content/MEDIAR/train_tools/data_utils/custom/modalities.pkl

if relabel:
        for elem in data_dicts:
            cell_idx = int(elem["label"].split("_label.tiff")[0].split("_")[-1])
            if cell_idx in range(340, 499):
                new_label = elem["label"].replace(
                    "/content/dataset/train/labels/",
                    "/content/dataset/",
                )
                elem["label"] = new_label