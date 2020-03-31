# Simple-kube

This project was created to simplify python kubernetes-client library.

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

```sh
python setup.py develop
```

```sh
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/simplekube-0.0.9* -u __token__ -p <token>
```

```sh
pip install --index-url https://test.pypi.org/simple/ --no-deps simplekube
```
