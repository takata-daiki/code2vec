import glob

from extractor import Extractor
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

SHOW_TOP_CONTEXTS = 0
MAX_PATH_LENGTH = 10**3
MAX_PATH_WIDTH = 10**3
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


class InteractivePredictor:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(
            config,
            jar_path=JAR_PATH,
            max_path_length=MAX_PATH_LENGTH,
            max_path_width=MAX_PATH_WIDTH)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def predict(self):
        print(
            'NOTICE: The cusomized version of predict() in interactive_predict.py was called !'
        )
        data_directory = './data/java-fmri/test/'  # set your own dataset directory to be converted into code vectors.
        input_filenames = sorted(glob.glob(data_directory + '*.java'))

        corpus = []
        vocab = {}
        for input_filename in input_filenames:
            print(input_filename)
            try:
                predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(
                    input_filename)

                ast_paths = ' '.join(hash_to_string_dict.keys())
                vocab.update(hash_to_string_dict)
                corpus.append(ast_paths)
                continue

            except ValueError as e:
                print(e)
                continue

        vectorizer = CountVectorizer(token_pattern='\S+')
        bag = vectorizer.fit_transform(corpus)
        # print(bag.toarray())

        print('\n====> Creating bag_of_paths.csv...')
        np.savetxt(
            './data/bag_of_paths.csv',
            bag.toarray().astype(int),
            delimiter=',',
            fmt='%d')

        print('\n====> Creating index.csv...')
        print('\nformat="{{hashed_path: num_of_cols}}"')
        pprint(vectorizer.vocabulary_, width=50)
        print('\nformat="{{hashed_path: context_path_str}}"')
        pprint(vocab, width=50)
        with open('./data/index.csv', mode='w') as f:
            for hashed_path in sorted(vectorizer.vocabulary_.keys()):
                f.write('{},{}\n'.format(hashed_path, vocab[hashed_path]))
