import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tournament_runner",
    version="0.0.1",
    author="Iurii Piurbeev",
    author_email="angry-yura@yandex.ru",
    description="A small app to run swiss tournaments and others",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yurap/tournament-runner",
    packages=setuptools.find_packages(),
    classifiers=[
        "swiss-system",
		"tournament-manager",
		"tournament-bracket",
    ],
)