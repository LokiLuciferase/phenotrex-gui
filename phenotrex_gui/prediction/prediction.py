from typing import List, Tuple
from pathlib import Path

import pandas as pd
import numpy as np

from phenotrex.io.flat import load_genotype_file, DEFAULT_TRAIT_SIGN_MAPPING
from phenotrex.io.serialization import load_classifier
from phenotrex.ml.shap_handler import ShapHandler
from phenotrex.transforms import fastas_to_grs


VALID_FASTA_FILE_EXTENSIONS = {
    '.fna',
    '.fna.gz',
    '.faa',
    '.faa.gz',
    '.fasta',
    '.fasta.gz'
}
VALID_GENOTYPE_EXTENSIONS = {
    '.genotype'
}

def _determine_file_types(input_files: List[str]) -> Tuple[List[str], List[str]]:
    fasta_files = []
    genotype_files = []
    for f in input_files:
        if any(f.endswith(x) for x in VALID_FASTA_FILE_EXTENSIONS):
            fasta_files.append(f)
        elif any(f.endswith(x) for x in VALID_GENOTYPE_EXTENSIONS):
            genotype_files.append(f)
        else:
            raise ValueError('Invalid file type supplied.')
    return fasta_files, genotype_files


def predict(input_files: List[str], classifier: str, min_proba=0.0, verb=True) -> pd.DataFrame:
    if not len(input_files):
        raise RuntimeError('Must supply input file(s) for prediction.')
    fasta_files, genotype_files = _determine_file_types(input_files)
    gr = []
    if fasta_files:
        gr += fastas_to_grs(fasta_files, n_threads=None, verb=verb)
    for f in genotype_files:
        gr += load_genotype_file(f)
    model = load_classifier(filename=classifier, verb=verb)
    preds, probas = model.predict(X=gr)
    translate_output = {
        trait_id: trait_sign for trait_sign, trait_id in DEFAULT_TRAIT_SIGN_MAPPING.items()
    }
    out = {}
    for record, result, probability in zip(gr, preds, probas):
        if probability[result] < min_proba:
            result_disp = np.nan
        else:
            result_disp = translate_output[result]
        out[record.identifier] = {
            'Trait Present': result_disp,
            'Confidence':str(round(probability[result], 4))
        }

    df = pd.DataFrame.from_dict(out).T
    df.index.name = 'Genome'
    df = df.reset_index()
    df['Trait Name'] = model.trait_name
    df['Feature Type'] = model.feature_type
    df['Model File'] = Path(classifier).name
    df = df[[
        'Genome',
        'Model File',
        'Feature Type',
        'Trait Name',
        'Trait Present',
        'Confidence'
    ]]
    return df
