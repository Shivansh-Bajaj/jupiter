import nltk

def download_nltk_packages():
	"""Downloads packages used by nltk (http://www.nltk.org/data.html).
	Puts the downloaded files in $HOME/nltk_data/ directory [This location
	varies by operating systems - check the below link]:
	http://www.nltk.org/data.html#command-line-installation].
	"""
	# Define the packages to be downloaded here.
	packages = [
		'stopwords',
		'punkt',
		'averaged_perceptron_tagger'
	]

	print('START DOWNLOADING RESOURCES...')
	print('NOTE: May take a few minutes if connection is slow.')
	for package in packages:
		print('Downloading ', package, '...')
		nltk.download(package)
		print('... Done downloading ', package)
		print('----------------------------------------')

if __name__ == '__main__':
	download_nltk_packages()
