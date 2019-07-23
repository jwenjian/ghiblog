from wordcloud import WordCloud


class WordCloudGenerator(object):
    def __init__(self, github_repo):
        self._repo = github_repo

    def generate(self) -> str:
        if self._repo is None:
            print('self._repo is None')
            return 'https://http.cat/500'

        frequencies = {}

        # get labels
        labels = self._repo.get_labels()

        for label in labels:
            issues_in_label = self._repo.get_issues(labels=(label,))
            frequencies[label.name] = issues_in_label.totalCount

        print(frequencies)
        # generate wordcount image to local dir

        # specify the font to support Chinese word
        wc = WordCloud(font_path='lib/fonts/wqy-microhei.ttc', width=1920, height=400)
        wc.generate_from_frequencies(frequencies=frequencies)
        wc.to_file('assets/wordcloud.png')

        print('wordcloud picture generated successfully!')

        return 'assets/wordcloud.png'
